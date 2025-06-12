import logging
import json
from typing import Optional, List, Dict
from director.agents.base import BaseAgent, AgentResponse, AgentStatus
from director.core.session import Session, TextContent, MsgStatus, ContextMessage, RoleTypes
from director.tools.videodb_tool import VideoDBTool
from director.llm import get_default_llm

logger = logging.getLogger(__name__)

VIRAL_ANALYSIS_PARAMETERS = {
    "type": "object",
    "properties": {
        "video_ids": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of video IDs to analyze for viral patterns"
        },
        "collection_id": {
            "type": "string",
            "description": "Collection containing the videos"
        },
        "revenue_data": {
            "type": "object",
            "description": "Optional revenue/conversion data associated with videos",
            "properties": {
                "video_revenue_mapping": {
                    "type": "object",
                    "description": "Mapping of video_id to revenue/conversion metrics"
                }
            }
        }
    },
    "required": ["video_ids", "collection_id"]
}

class ViralPatternAnalysisAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "viral_pattern_analysis"
        self.description = "Analyzes TikTok videos to identify viral patterns, engagement triggers, and conversion elements that drive views and sales"
        self.parameters = VIRAL_ANALYSIS_PARAMETERS
        self.llm = get_default_llm()
        super().__init__(session=session, **kwargs)

    def run(self, video_ids: List[str], collection_id: str, 
            revenue_data: Optional[Dict] = None, *args, **kwargs) -> AgentResponse:
        """
        Analyze TikTok videos for viral patterns and conversion triggers
        """
        try:
            self.videodb_tool = VideoDBTool(collection_id=collection_id)
            
            self.output_message.actions.append(f"Analyzing {len(video_ids)} videos for viral patterns...")
            self.output_message.push_update()
            
            analysis_results = {
                "viral_elements": [],
                "engagement_triggers": [],
                "conversion_patterns": [],
                "hook_patterns": [],
                "optimal_timing": {},
                "trending_elements": []
            }
            
            video_analyses = []
            
            for i, video_id in enumerate(video_ids):
                self.output_message.actions.append(f"Analyzing video {i+1}/{len(video_ids)}: {video_id}")
                self.output_message.push_update()
                
                try:
                    # Get video details
                    video_info = self.videodb_tool.get_video(video_id)
                    
                    # Get transcript if available
                    try:
                        transcript = self.videodb_tool.get_transcript(video_id)
                    except:
                        self.output_message.actions.append(f"Indexing spoken words for video {video_id}")
                        self.output_message.push_update()
                        self.videodb_tool.index_spoken_words(video_id)
                        transcript = self.videodb_tool.get_transcript(video_id)
                    
                    # Get revenue data for this video if available
                    video_revenue = "N/A"
                    if revenue_data and revenue_data.get("video_revenue_mapping"):
                        video_revenue = revenue_data["video_revenue_mapping"].get(video_id, "N/A")
                    
                    # Analyze viral patterns using LLM
                    viral_analysis_prompt = f"""
                    Analyze this TikTok video for viral patterns and engagement triggers:
                    
                    Video Title: {video_info.get('name', 'Unknown')}
                    Duration: {video_info.get('length', 0)} seconds
                    Transcript: {transcript[:2000]}...
                    Revenue/Performance Data: {video_revenue}
                    
                    Identify and categorize:
                    
                    1. HOOK PATTERNS (first 3 seconds):
                       - Visual hooks (transitions, movements, reveals)
                       - Audio hooks (voice patterns, music, sounds)
                       - Text hooks (questions, statements, promises)
                    
                    2. ENGAGEMENT TRIGGERS:
                       - Emotional peaks (surprise, humor, relatability)
                       - Interactive elements (questions, challenges)
                       - Curiosity gaps (incomplete information, cliffhangers)
                    
                    3. CONVERSION ELEMENTS:
                       - Product placement timing and method
                       - Trust signals (testimonials, demonstrations)
                       - Call-to-action effectiveness and placement
                    
                    4. VIRAL MECHANICS:
                       - Trending phrases or keywords
                       - Shareability factors
                       - Comment-driving elements
                    
                    5. TIMING ANALYSIS:
                       - When attention peaks occur
                       - Optimal moments for key information
                       - Drop-off points to avoid
                    
                    Return analysis as structured JSON with specific examples and quantified insights.
                    Format: {{"hook_patterns": [], "engagement_triggers": [], "conversion_elements": [], "viral_mechanics": [], "timing_insights": {{}}}}
                    """
                    
                    analysis_message = ContextMessage(content=viral_analysis_prompt, role=RoleTypes.user)
                    llm_response = self.llm.chat_completions(
                        [analysis_message.to_llm_msg()], 
                        response_format={"type": "json_object"}
                    )
                    
                    try:
                        video_analysis = json.loads(llm_response.content)
                        video_analysis["video_id"] = video_id
                        video_analysis["video_name"] = video_info.get('name', 'Unknown')
                        video_analysis["revenue_data"] = video_revenue
                        video_analyses.append(video_analysis)
                        
                        # Aggregate patterns
                        if "hook_patterns" in video_analysis:
                            analysis_results["viral_elements"].extend(video_analysis["hook_patterns"])
                        if "engagement_triggers" in video_analysis:
                            analysis_results["engagement_triggers"].extend(video_analysis["engagement_triggers"])
                        if "conversion_elements" in video_analysis:
                            analysis_results["conversion_patterns"].extend(video_analysis["conversion_elements"])
                            
                    except json.JSONDecodeError:
                        logger.warning(f"Could not parse LLM response for video {video_id}")
                        continue
                        
                except Exception as e:
                    logger.warning(f"Could not analyze video {video_id}: {e}")
                    continue
            
            # Generate comprehensive insights
            self.output_message.actions.append("Generating viral pattern insights...")
            self.output_message.push_update()
            
            insights_prompt = f"""
            Based on the analysis of {len(video_analyses)} TikTok videos, identify the most effective viral patterns:
            
            Video Analyses: {json.dumps(video_analyses, indent=2)}
            
            Generate actionable insights:
            1. Top 5 most effective hook patterns with examples
            2. Best engagement triggers that drive completion rates
            3. Optimal timing for product placement and CTAs
            4. Most viral elements that increase shareability
            5. Common patterns in high-revenue videos
            
            Provide specific, actionable recommendations for creating viral TikTok content.
            """
            
            insights_message = ContextMessage(content=insights_prompt, role=RoleTypes.user)
            insights_response = self.llm.chat_completions([insights_message.to_llm_msg()])
            
            # Create comprehensive report
            text_content = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.success,
                status_message="Viral pattern analysis complete",
                text=f"""
                📊 **Viral Pattern Analysis Complete**
                
                **Videos Analyzed:** {len(video_analyses)}/{len(video_ids)}
                
                **Key Insights:**
                {insights_response.content}
                
                **Pattern Summary:**
                • {len(analysis_results['viral_elements'])} viral elements identified
                • {len(analysis_results['engagement_triggers'])} engagement triggers found
                • {len(analysis_results['conversion_patterns'])} conversion patterns analyzed
                
                Use these insights to optimize your next TikTok videos for maximum viral potential and conversion rates.
                """
            )
            
            self.output_message.content.append(text_content)
            self.output_message.publish()
            
            return AgentResponse(
                status=AgentStatus.SUCCESS,
                message="Viral pattern analysis completed successfully",
                data={
                    "analysis_results": analysis_results,
                    "video_analyses": video_analyses,
                    "insights": insights_response.content
                }
            )
            
        except Exception as e:
            logger.exception(f"Error in {self.agent_name}")
            text_content = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.error,
                status_message="Failed to analyze viral patterns"
            )
            self.output_message.content.append(text_content)
            self.output_message.publish()
            return AgentResponse(status=AgentStatus.ERROR, message=str(e))
        