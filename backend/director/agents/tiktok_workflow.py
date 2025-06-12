import logging
from typing import Dict, List, Optional
from director.agents.base import BaseAgent, AgentResponse, AgentStatus
from director.core.session import Session, TextContent, MsgStatus
from director.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)

TIKTOK_WORKFLOW_PARAMETERS = {
    "type": "object",
    "properties": {
        "workflow_type": {
            "type": "string",
            "enum": ["analyze_and_create", "viral_analysis_only", "script_generation_only", "full_production"],
            "description": "Type of TikTok workflow to execute"
        },
        "input_videos": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Video IDs for viral analysis"
        },
        "product_info": {
            "type": "object",
            "description": "Product information for new video creation",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "key_features": {"type": "array", "items": {"type": "string"}},
                "target_audience": {"type": "string"},
                "price_point": {"type": "string"}
            }
        },
        "collection_id": {
            "type": "string",
            "description": "VideoDB collection ID"
        },
        "video_style": {
            "type": "string",
            "enum": ["educational", "entertainment", "testimonial", "unboxing", "comparison"],
            "description": "Style of TikTok video to create",
            "default": "entertainment"
        },
        "auto_upload": {
            "type": "boolean",
            "description": "Whether to automatically upload to TikTok",
            "default": False
        }
    },
    "required": ["workflow_type", "collection_id"]
}

class TikTokMarketingWorkflow(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "tiktok_marketing_workflow"
        self.description = "Orchestrates complete TikTok marketing workflow from viral analysis to video creation and upload"
        self.parameters = TIKTOK_WORKFLOW_PARAMETERS
        super().__init__(session=session, **kwargs)

    def run(self, workflow_type: str, collection_id: str,
            input_videos: Optional[List[str]] = None,
            product_info: Optional[Dict] = None,
            video_style: str = "entertainment",
            auto_upload: bool = False,
            *args, **kwargs) -> AgentResponse:
        """
        Execute complete TikTok marketing workflow
        """
        try:
            self.output_message.actions.append(f"Starting {workflow_type} TikTok workflow...")
            self.output_message.push_update()
            
            if workflow_type == "analyze_and_create":
                return self._execute_analyze_and_create_workflow(
                    input_videos, product_info, collection_id, video_style, auto_upload
                )
            elif workflow_type == "viral_analysis_only":
                return self._execute_viral_analysis_only(input_videos, collection_id)
            elif workflow_type == "script_generation_only":
                return self._execute_script_generation_only(product_info, video_style)
            elif workflow_type == "full_production":
                return self._execute_full_production_workflow(
                    input_videos, product_info, collection_id, video_style, auto_upload
                )
            else:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
                
        except Exception as e:
            logger.exception(f"Error in {self.agent_name}")
            return AgentResponse(status=AgentStatus.ERROR, message=str(e))

    def _execute_analyze_and_create_workflow(self, input_videos: List[str], 
                                           product_info: Dict, collection_id: str,
                                           video_style: str, auto_upload: bool):
        """
        Complete workflow: Analyze → Generate Script → Create Video → (Optional Upload)
        """
        workflow_results = {}
        
        try:
            # Step 1: Viral Pattern Analysis
            if input_videos:
                self.output_message.actions.append("🔍 Step 1: Analyzing viral patterns...")
                self.output_message.push_update()
                
                from director.agents.tiktok_viral_analysis import ViralPatternAnalysisAgent
                viral_agent = ViralPatternAnalysisAgent(session=self.session)
                viral_response = viral_agent.run(
                    video_ids=input_videos,
                    collection_id=collection_id
                )
                
                if viral_response.status == AgentStatus.SUCCESS:
                    workflow_results["viral_analysis"] = viral_response.data
                    self.output_message.actions.append("✅ Viral patterns identified!")
                else:
                    self.output_message.actions.append("⚠️ Viral analysis had issues, continuing...")
                    workflow_results["viral_analysis"] = {}
            else:
                workflow_results["viral_analysis"] = {}
            
            # Step 2: Script Generation
            self.output_message.actions.append("📝 Step 2: Generating optimized TikTok script...")
            self.output_message.push_update()
            
            from director.agents.tiktok_script_generator import TikTokScriptGeneratorAgent
            script_agent = TikTokScriptGeneratorAgent(session=self.session)
            script_response = script_agent.run(
                product_info=product_info,
                video_style=video_style,
                viral_patterns=workflow_results.get("viral_analysis", {})
            )
            
            if script_response.status != AgentStatus.SUCCESS:
                raise Exception("Script generation failed")
            
            workflow_results["script"] = script_response.data
            self.output_message.actions.append("✅ Script generated successfully!")
            
            # Step 3: Video Creation
            self.output_message.actions.append("🎬 Step 3: Creating TikTok video...")
            self.output_message.push_update()
            
            # Use the existing TextToMovieAgent for video creation
            from director.agents.text_to_movie import TextToMovieAgent
            video_agent = TextToMovieAgent(session=self.session)
            
            # Convert script to storyline for TextToMovieAgent
            script_data = script_response.data.get("script", {})
            storyline = self._convert_script_to_storyline(script_data, product_info)
            
            video_response = video_agent.run(
                collection_id=collection_id,
                engine="videodb",
                job_type="text_to_movie",
                text_to_movie={
                    "storyline": storyline,
                    "sound_effects_description": f"Upbeat TikTok-style music for {product_info['name']} commercial"
                }
            )
            
            if video_response.status != AgentStatus.SUCCESS:
                raise Exception("Video creation failed")
            
            workflow_results["video_creation"] = video_response.data
            self.output_message.actions.append("✅ Video created successfully!")
            
            # Step 4: Optional Upload to TikTok
            if auto_upload:
                self.output_message.actions.append("📱 Step 4: Uploading to TikTok...")
                self.output_message.push_update()
                
                from director.agents.tiktok_upload import TikTokUploadAgent
                upload_agent = TikTokUploadAgent(session=self.session)
                
                # Get caption and hashtags from script
                caption = self._generate_caption_from_script(script_data, product_info)
                hashtags = script_data.get("hashtags", ["fyp", "viral", "musthave"])
                
                upload_response = upload_agent.run(
                    video_stream_url=video_response.data.get("video_url"),
                    caption=caption,
                    hashtags=hashtags
                )
                
                workflow_results["upload"] = upload_response.data
                self.output_message.actions.append("✅ Upload completed!")
            
            # Generate comprehensive summary
            text_content = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.success,
                status_message="TikTok marketing workflow completed successfully",
                text=self._generate_workflow_summary(workflow_results, product_info, auto_upload)
            )
            
            self.output_message.content.append(text_content)
            self.output_message.publish()
            
            return AgentResponse(
                status=AgentStatus.SUCCESS,
                message="TikTok marketing workflow completed successfully",
                data={"workflow_results": workflow_results}
            )
            
        except Exception as e:
            error_text = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.error,
                status_message="TikTok workflow failed",
                text=f"Workflow failed at step: {str(e)}"
            )
            self.output_message.content.append(error_text)
            self.output_message.publish()
            raise e

    def _convert_script_to_storyline(self, script_data: Dict, product_info: Dict) -> str:
        """Convert TikTok script to storyline for TextToMovieAgent"""
        scenes = script_data.get("scenes", [])
        storyline_parts = []
        
        for scene in scenes:
            timing = scene.get("timing", "")
            dialogue = scene.get("dialogue", "")
            visual = scene.get("visual_direction", "")
            scene_type = scene.get("type", "")
            
            storyline_parts.append(f"{scene_type.title()} ({timing}): {dialogue} - Visual: {visual}")
        
        storyline = f"""
        Create a {len(scenes)*5}-second TikTok-style video for {product_info['name']}:
        
        {' '.join(storyline_parts)}
        
        Style: Fast-paced, engaging, mobile-optimized vertical video with trending visual elements.
        """
        
        return storyline

    def _generate_caption_from_script(self, script_data: Dict, product_info: Dict) -> str:
        """Generate TikTok caption from script data"""
        posting_strategy = script_data.get("posting_strategy", {})
        caption_suggestion = posting_strategy.get("caption_suggestions", "")
        
        if caption_suggestion:
            return caption_suggestion
        
        # Fallback caption
        return f"Check out {product_info['name']}! 🔥 You won't believe what happened... #fyp #viral"

    def _generate_workflow_summary(self, workflow_results: Dict, product_info: Dict, auto_upload: bool) -> str:
        """Generate comprehensive workflow summary"""
        summary = f"""
        🎉 **TikTok Marketing Workflow Complete!**
        
        **Product:** {product_info['name']}
        
        **Results:**
        """
        
        if "viral_analysis" in workflow_results:
            viral_data = workflow_results["viral_analysis"]
            video_count = len(viral_data.get("video_analyses", []))
            summary += f"📊 Analyzed {video_count} videos for viral patterns\n"
        
        if "script" in workflow_results:
            script_data = workflow_results["script"].get("script", {})
            scene_count = len(script_data.get("scenes", []))
            summary += f"📝 Generated {scene_count}-scene optimized script\n"
        
        if "video_creation" in workflow_results:
            summary += f"🎬 Created professional TikTok video\n"
        
        if auto_upload and "upload" in workflow_results:
            upload_data = workflow_results["upload"].get("upload_result", {})
            if upload_data.get("simulation"):
                summary += f"📱 Simulated TikTok upload (configure API for real uploads)\n"
            else:
                summary += f"📱 Successfully uploaded to TikTok: {upload_data.get('url', 'N/A')}\n"
        
        summary += f"""
        
        **Next Steps:**
        1. Review the generated content
        2. Make any desired adjustments
        3. {"Monitor performance metrics" if auto_upload else "Upload to TikTok when ready"}
        4. Analyze results for future optimization
        
        🚀 Your TikTok marketing content is ready to drive engagement and conversions!
        """
        
        return summary

    def _execute_viral_analysis_only(self, input_videos: List[str], collection_id: str):
        """Execute only viral pattern analysis"""
        # Implementation for viral analysis only workflow
        pass

    def _execute_script_generation_only(self, product_info: Dict, video_style: str):
        """Execute only script generation"""
        # Implementation for script generation only workflow
        pass

    def _execute_full_production_workflow(self, input_videos: List[str], 
                                        product_info: Dict, collection_id: str,
                                        video_style: str, auto_upload: bool):
        """Execute complete production workflow with performance tracking"""
        # Implementation for full production workflow with analytics
        pass
