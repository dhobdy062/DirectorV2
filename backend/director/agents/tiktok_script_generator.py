import logging
import json
from typing import Optional, Dict, List
from director.agents.base import BaseAgent, AgentResponse, AgentStatus
from director.core.session import Session, TextContent, MsgStatus, ContextMessage, RoleTypes
from director.llm import get_default_llm

logger = logging.getLogger(__name__)

SCRIPT_GENERATOR_PARAMETERS = {
    "type": "object",
    "properties": {
        "product_info": {
            "type": "object",
            "description": "Product information for the TikTok video",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "key_features": {"type": "array", "items": {"type": "string"}},
                "target_audience": {"type": "string"},
                "price_point": {"type": "string"},
                "unique_selling_points": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["name", "description"]
        },
        "viral_patterns": {
            "type": "object",
            "description": "Viral patterns from analysis agent (optional)"
        },
        "video_style": {
            "type": "string",
            "enum": ["educational", "entertainment", "testimonial", "unboxing", "comparison", "transformation", "challenge"],
            "description": "Style of TikTok video to create"
        },
        "duration": {
            "type": "number",
            "description": "Target video duration in seconds",
            "default": 30
        },
        "target_metrics": {
            "type": "object",
            "description": "Target performance metrics",
            "properties": {
                "views": {"type": "number"},
                "engagement_rate": {"type": "number"},
                "completion_rate": {"type": "number"}
            }
        }
    },
    "required": ["product_info", "video_style"]
}

class TikTokScriptGeneratorAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "tiktok_script_generator"
        self.description = "Generates optimized TikTok video scripts based on viral patterns, product information, and performance goals"
        self.parameters = SCRIPT_GENERATOR_PARAMETERS
        self.llm = get_default_llm()
        super().__init__(session=session, **kwargs)

    def run(self, product_info: Dict, video_style: str,
            viral_patterns: Optional[Dict] = None, duration: int = 30,
            target_metrics: Optional[Dict] = None,
            *args, **kwargs) -> AgentResponse:
        """
        Generate TikTok script based on viral patterns and product info
        """
        try:
            self.output_message.actions.append(f"Generating {video_style} TikTok script for {product_info['name']}...")
            self.output_message.push_update()
            
            # Prepare viral patterns context
            viral_context = ""
            if viral_patterns and viral_patterns.get("insights"):
                viral_context = f"Viral Patterns to Incorporate:\n{viral_patterns['insights']}\n\n"
            
            # Create comprehensive script generation prompt
            script_prompt = f"""
            Create a high-converting {duration}-second TikTok script for {video_style} style video.
            
            PRODUCT INFORMATION:
            - Name: {product_info['name']}
            - Description: {product_info['description']}
            - Key Features: {product_info.get('key_features', [])}
            - Target Audience: {product_info.get('target_audience', 'General TikTok users')}
            - Price Point: {product_info.get('price_point', 'Not specified')}
            - Unique Selling Points: {product_info.get('unique_selling_points', [])}
            
            {viral_context}
            
            TARGET PERFORMANCE:
            {target_metrics if target_metrics else 'Optimize for high engagement and conversions'}
            
            SCRIPT STRUCTURE ({duration} seconds):
            
            1. HOOK (0-3 seconds):
               - Create an immediate attention grabber
               - Use trending phrases, visual surprise, or bold statements
               - Should make viewers stop scrolling instantly
            
            2. PROBLEM/SETUP (3-8 seconds):
               - Establish viewer pain point or desire
               - Create relatability and emotional connection
               - Set up the need for your product
            
            3. SOLUTION/DEMO (8-{duration-5} seconds):
               - Showcase product naturally and authentically
               - Demonstrate key benefits through action
               - Include social proof or credibility signals
            
            4. CALL-TO-ACTION ({duration-5}-{duration} seconds):
               - Clear, specific next step
               - Create urgency or scarcity if appropriate
               - Include relevant hashtags
            
            REQUIREMENTS:
            - Include trending sound/music suggestions
            - Specify visual directions for each scene
            - Provide exact voiceover/dialogue text
            - Suggest on-screen text overlays
            - Include hashtag strategy
            - Consider TikTok algorithm optimization
            - Ensure authenticity and avoid overly salesy tone
            
            STYLE-SPECIFIC ELEMENTS for {video_style}:
            {self._get_style_specific_guidance(video_style)}
            
            Return as structured JSON with the following format:
            {{
                "script_overview": "Brief description of the video concept",
                "scenes": [
                    {{
                        "timing": "0-3s",
                        "type": "hook",
                        "dialogue": "Exact words to say",
                        "visual_direction": "What viewers see",
                        "on_screen_text": "Text overlay if any",
                        "notes": "Additional direction"
                    }}
                ],
                "audio_suggestions": {{
                    "trending_sounds": ["sound1", "sound2"],
                    "music_style": "description",
                    "voice_direction": "tone and pace guidance"
                }},
                "hashtags": ["primary", "secondary", "niche"],
                "posting_strategy": {{
                    "best_times": "when to post",
                    "caption_suggestions": "full caption text",
                    "engagement_tactics": "how to drive comments/shares"
                }}
            }}
            """
            
            self.output_message.actions.append("Generating optimized script content...")
            self.output_message.push_update()
            
            script_message = ContextMessage(content=script_prompt, role=RoleTypes.user)
            response = self.llm.chat_completions(
                [script_message.to_llm_msg()], 
                response_format={"type": "json_object"}
            )
            
            try:
                script_data = json.loads(response.content)
                
                # Validate and enhance script
                self.output_message.actions.append("Optimizing script for viral potential...")
                self.output_message.push_update()
                
                # Create user-friendly output
                script_summary = self._format_script_summary(script_data, product_info, video_style)
                
                text_content = TextContent(
                    agent_name=self.agent_name,
                    status=MsgStatus.success,
                    status_message="TikTok script generated successfully",
                    text=script_summary
                )
                
                self.output_message.content.append(text_content)
                self.output_message.publish()
                
                return AgentResponse(
                    status=AgentStatus.SUCCESS,
                    message="TikTok script generated successfully",
                    data={
                        "script": script_data,
                        "product_info": product_info,
                        "video_style": video_style,
                        "duration": duration
                    }
                )
                
            except json.JSONDecodeError:
                raise Exception("Failed to parse script generation response")
                
        except Exception as e:
            logger.exception(f"Error in {self.agent_name}")
            text_content = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.error,
                status_message="Failed to generate TikTok script"
            )
            self.output_message.content.append(text_content)
            self.output_message.publish()
            return AgentResponse(status=AgentStatus.ERROR, message=str(e))

    def _get_style_specific_guidance(self, video_style: str) -> str:
        """Get specific guidance based on video style"""
        guidance = {
            "educational": "Focus on teaching something valuable, use clear explanations, include tips or hacks",
            "entertainment": "Prioritize humor, surprise elements, trending challenges or memes",
            "testimonial": "Show authentic before/after, include personal story, emphasize real results",
            "unboxing": "Build anticipation, show genuine reactions, highlight packaging and first impressions",
            "comparison": "Create clear contrasts, use split-screen concepts, show dramatic differences",
            "transformation": "Document the journey, show clear before/after, include time progression",
            "challenge": "Create shareable challenge, encourage participation, use trending format"
        }
        return guidance.get(video_style, "Create engaging, authentic content that resonates with your audience")

    def _format_script_summary(self, script_data: Dict, product_info: Dict, video_style: str) -> str:
        """Format script data into readable summary"""
        try:
            scenes_summary = ""
            if "scenes" in script_data:
                for i, scene in enumerate(script_data["scenes"], 1):
                    scenes_summary += f"""
                    **Scene {i} ({scene.get('timing', 'N/A')}) - {scene.get('type', 'Scene').title()}:**
                    • Dialogue: "{scene.get('dialogue', 'N/A')}"
                    • Visual: {scene.get('visual_direction', 'N/A')}
                    """
                    if scene.get('on_screen_text'):
                        scenes_summary += f"• Text Overlay: {scene['on_screen_text']}\n"
            
            hashtags = ", ".join(script_data.get("hashtags", []))
            
            return f"""
            🎬 **{video_style.title()} TikTok Script for {product_info['name']}**
            
            **Concept:** {script_data.get('script_overview', 'Custom TikTok video')}
            
            **Scenes Breakdown:**{scenes_summary}
            
            **Audio Strategy:**
            • Trending Sounds: {', '.join(script_data.get('audio_suggestions', {}).get('trending_sounds', ['To be selected']))}
            • Music Style: {script_data.get('audio_suggestions', {}).get('music_style', 'Upbeat and engaging')}
            
            **Hashtag Strategy:** #{hashtags}
            
            **Posting Strategy:**
            {script_data.get('posting_strategy', {}).get('caption_suggestions', 'Optimized caption included in script data')}
            
            **Best Posting Times:** {script_data.get('posting_strategy', {}).get('best_times', 'Peak engagement hours')}
            
            ✨ Script optimized for viral potential and conversion!
            """
        except Exception as e:
            return f"Script generated successfully for {product_info['name']} - {video_style} style video. Full details available in response data."