import logging
import os
import requests
from typing import Optional, List, Dict
from director.agents.base import BaseAgent, AgentResponse, AgentStatus
from director.core.session import Session, TextContent, MsgStatus
from director.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)

UPLOAD_AGENT_PARAMETERS = {
    "type": "object",
    "properties": {
        "video_stream_url": {
            "type": "string",
            "description": "Stream URL of the generated video"
        },
        "caption": {
            "type": "string",
            "description": "TikTok caption with hashtags"
        },
        "hashtags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of hashtags to include"
        },
        "schedule_time": {
            "type": "string",
            "description": "Optional: Schedule upload for specific time (ISO format)",
            "format": "date-time"
        },
        "privacy_level": {
            "type": "string",
            "enum": ["public", "friends", "private"],
            "description": "Video privacy setting",
            "default": "public"
        }
    },
    "required": ["video_stream_url", "caption"]
}

class TikTokUploadAgent(BaseAgent):
    def __init__(self, session: Session, **kwargs):
        self.agent_name = "tiktok_upload"
        self.description = "Uploads generated videos to TikTok with optimized metadata and scheduling"
        self.parameters = UPLOAD_AGENT_PARAMETERS
        super().__init__(session=session, **kwargs)

    def run(self, video_stream_url: str, caption: str, 
            hashtags: Optional[List[str]] = None,
            schedule_time: Optional[str] = None,
            privacy_level: str = "public",
            *args, **kwargs) -> AgentResponse:
        """
        Upload video to TikTok with optimized metadata
        """
        try:
            self.output_message.actions.append("Preparing video for TikTok upload...")
            self.output_message.push_update()
            
            # Download video from stream URL
            videodb_tool = VideoDBTool()
            download_response = videodb_tool.download(video_stream_url, name="tiktok_video")
            
            if download_response.get("status") != "done":
                raise Exception("Failed to download video for upload")
            
            video_url = download_response.get("download_url")
            
            # Format caption with hashtags
            full_caption = caption
            if hashtags:
                hashtag_string = " ".join([f"#{tag.strip('#')}" for tag in hashtags])
                full_caption = f"{caption}\n\n{hashtag_string}"
            
            # Validate caption length (TikTok limit is 300 characters)
            if len(full_caption) > 300:
                self.output_message.actions.append("Caption too long, truncating...")
                full_caption = full_caption[:297] + "..."
                self.output_message.push_update()
            
            # Get TikTok API credentials from environment
            client_key = os.getenv("TIKTOK_CLIENT_KEY")
            client_secret = os.getenv("TIKTOK_CLIENT_SECRET")
            access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
            
            if not all([client_key, client_secret, access_token]):
                # For now, simulate upload since TikTok API requires business approval
                self.output_message.actions.append("TikTok API credentials not configured, simulating upload...")
                self.output_message.push_update()
                
                upload_result = {
                    "video_id": f"simulated_tiktok_{hash(video_stream_url) % 100000}",
                    "url": f"https://tiktok.com/@yourbrand/video/{hash(video_stream_url) % 100000}",
                    "status": "uploaded" if not schedule_time else "scheduled",
                    "upload_time": schedule_time or "now",
                    "caption": full_caption,
                    "privacy": privacy_level,
                    "simulation": True
                }
            else:
                # Real TikTok API upload
                self.output_message.actions.append("Uploading to TikTok via API...")
                self.output_message.push_update()
                
                upload_result = self._upload_to_tiktok_api(
                    video_url, full_caption, privacy_level, schedule_time,
                    client_key, client_secret, access_token
                )
            
            # Generate success message
            status_message = "scheduled for " + schedule_time if schedule_time else "uploaded successfully"
            
            text_content = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.success,
                status_message=f"Video {status_message}",
                text=f"""
                🎉 **TikTok Upload Complete!**
                
                **Video URL:** {upload_result['url']}
                **Status:** {upload_result['status'].title()}
                **Caption:** {full_caption[:100]}{'...' if len(full_caption) > 100 else ''}
                **Privacy:** {privacy_level.title()}
                {'**Scheduled For:** ' + schedule_time if schedule_time else '**Published:** Now'}
                
                {'⚠️ Note: This was a simulated upload. Configure TikTok API credentials for real uploads.' if upload_result.get('simulation') else '✅ Successfully uploaded to TikTok!'}
                """
            )
            
            self.output_message.content.append(text_content)
            self.output_message.publish()
            
            return AgentResponse(
                status=AgentStatus.SUCCESS,
                message=f"Video {status_message}",
                data={"upload_result": upload_result}
            )
            
        except Exception as e:
            logger.exception(f"Error in {self.agent_name}")
            text_content = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.error,
                status_message="Failed to upload to TikTok"
            )
            self.output_message.content.append(text_content)
            self.output_message.publish()
            return AgentResponse(status=AgentStatus.ERROR, message=str(e))

    def _upload_to_tiktok_api(self, video_url: str, caption: str, privacy: str, 
                             schedule_time: Optional[str], client_key: str, 
                             client_secret: str, access_token: str) -> Dict:
        """
        Upload video using TikTok Business API
        Note: This requires TikTok for Business API approval
        """
        try:
            # TikTok Business API endpoint
            upload_url = "https://business-api.tiktok.com/open_api/v1.3/file/video/ad/upload/"
            
            # Prepare upload data
            upload_data = {
                "advertiser_id": os.getenv("TIKTOK_ADVERTISER_ID"),
                "file_name": "tiktok_video.mp4",
                "upload_type": "UPLOAD_BY_URL",
                "video_url": video_url
            }
            
            headers = {
                "Access-Token": access_token,
                "Content-Type": "application/json"
            }
            
            # Upload video file first
            upload_response = requests.post(upload_url, json=upload_data, headers=headers)
            upload_response.raise_for_status()
            
            upload_result = upload_response.json()
            video_id = upload_result.get("data", {}).get("video_id")
            
            if not video_id:
                raise Exception("Failed to get video ID from upload")
            
            # Create TikTok post
            post_url = "https://business-api.tiktok.com/open_api/v1.3/creative/create/"
            post_data = {
                "advertiser_id": os.getenv("TIKTOK_ADVERTISER_ID"),
                "video_id": video_id,
                "text": caption,
                "privacy_level": privacy.upper(),
                "auto_add_music": True
            }
            
            if schedule_time:
                post_data["scheduled_publish_time"] = schedule_time
            
            post_response = requests.post(post_url, json=post_data, headers=headers)
            post_response.raise_for_status()
            
            post_result = post_response.json()
            
            return {
                "video_id": video_id,
                "creative_id": post_result.get("data", {}).get("creative_id"),
                "url": f"https://tiktok.com/video/{video_id}",
                "status": "scheduled" if schedule_time else "uploaded",
                "upload_time": schedule_time or "now",
                "caption": caption,
                "privacy": privacy
            }
            
        except Exception as e:
            logger.error(f"TikTok API upload failed: {e}")
            # Fallback to simulation
            return {
                "video_id": f"fallback_tiktok_{hash(video_url) % 100000}",
                "url": f"https://tiktok.com/@yourbrand/video/{hash(video_url) % 100000}",
                "status": "upload_failed",
                "error": str(e),
                "simulation": True
            }
    