"""
Video processing and generation for TextToMovieAgent
"""

import os
import uuid
from typing import List, Optional
from videodb.asset import VideoAsset, AudioAsset
from director.constants import DOWNLOADS_PATH
from .models import VideoGenResult, EngineConfig, VisualStyle


class VideoProcessor:
    """Handles video generation and processing"""
    
    def __init__(self, video_gen_tool, audio_gen_tool, videodb_tool):
        self.video_gen_tool = video_gen_tool
        self.audio_gen_tool = audio_gen_tool
        self.videodb_tool = videodb_tool
    
    def generate_videos(
        self, 
        scenes: List[dict], 
        visual_style: VisualStyle,
        engine: str,
        engine_configs: dict,
        video_gen_config: dict,
        output_message,
        style_generator
    ) -> List[VideoGenResult]:
        """Generate videos for all scenes"""
        engine_config = engine_configs[engine]
        generated_videos_results = []

        # Generate videos sequentially
        for index, scene in enumerate(scenes):
            output_message.actions.append(
                f"Generating video for scene {index + 1}..."
            )
            output_message.push_update()

            suggested_duration = min(
                scene.get("suggested_duration", 5), engine_config.max_duration
            )
            
            # Generate engine-specific prompt
            prompt = style_generator.generate_engine_prompt(scene, visual_style, engine)

            print(f"Generating video for scene {index + 1}...")
            print("This is the prompt", prompt)

            video_path = f"{DOWNLOADS_PATH}/{str(uuid.uuid4())}.mp4"
            os.makedirs(DOWNLOADS_PATH, exist_ok=True)

            video = self.video_gen_tool.text_to_video(
                prompt=prompt,
                save_at=video_path,
                duration=suggested_duration,
                config=video_gen_config,
            )
            generated_videos_results.append(
                VideoGenResult(
                    step_index=index, 
                    video_path=video_path, 
                    success=True, 
                    video=video
                )
            )

        return generated_videos_results
    
    def upload_videos(
        self, 
        generated_videos_results: List[VideoGenResult], 
        scenes: List[dict],
        output_message
    ) -> float:
        """Upload videos to VideoDB and return total duration"""
        output_message.actions.append(
            f"Uploading {len(generated_videos_results)} videos to VideoDB..."
        )
        output_message.push_update()

        # Process videos and track duration
        total_duration = 0
        for result in generated_videos_results:
            if not result.success:
                raise Exception(
                    f"Failed to generate video {result.step_index}: {result.error}"
                )
            if result.video is None:
                output_message.actions.append(
                    f"Uploading video {result.step_index + 1}..."
                )
                output_message.push_update()
                media = self.videodb_tool.upload(
                    result.video_path,
                    source_type="file_path",
                    media_type="video",
                )
            else:
                media = result.video

            total_duration += float(media.get("length", 0))
            scenes[result.step_index]["video"] = media

            if os.path.exists(result.video_path):
                os.remove(result.video_path)
        
        return total_duration
    
    def generate_audio(
        self, 
        sound_effects_description: str, 
        total_duration: float,
        audio_gen_config: dict,
        output_message
    ) -> dict:
        """Generate background audio"""
        output_message.actions.append("Generating background music...")
        output_message.push_update()

        # Generate and add sound effects
        os.makedirs(DOWNLOADS_PATH, exist_ok=True)
        sound_effects_path = f"{DOWNLOADS_PATH}/{str(uuid.uuid4())}.mp3"

        sound_effects_media = self.audio_gen_tool.generate_sound_effect(
            prompt=sound_effects_description,
            save_at=sound_effects_path,
            duration=total_duration,
            config=audio_gen_config,
        )

        if sound_effects_media is None:
            output_message.actions.append(
                "Uploading background music to VideoDB..."
            )
            output_message.push_update()

            sound_effects_media = self.videodb_tool.upload(
                sound_effects_path, source_type="file_path", media_type="audio"
            )

        if os.path.exists(sound_effects_path):
            os.remove(sound_effects_path)
        
        return sound_effects_media
    
    def combine_assets(self, scenes: List[dict], audio_media: Optional[dict]) -> str:
        """Combine video scenes and audio into final movie"""
        timeline = self.videodb_tool.get_and_set_timeline()

        # Add videos sequentially
        for scene in scenes:
            video_asset = VideoAsset(asset_id=scene["video"]["id"])
            timeline.add_inline(video_asset)

        # Add background score if available
        if audio_media:
            audio_asset = AudioAsset(
                asset_id=audio_media["id"], start=0, disable_other_tracks=True
            )
            timeline.add_overlay(0, audio_asset)

        return timeline.generate_stream()
