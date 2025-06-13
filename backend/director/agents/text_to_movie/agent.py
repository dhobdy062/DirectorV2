"""
Main TextToMovieAgent implementation
"""

import logging
import os
from typing import Optional

from director.agents.base import BaseAgent, AgentResponse, AgentStatus
from director.core.session import Session, MsgStatus, VideoContent, VideoData
from director.llm import get_default_llm
from director.tools.kling import KlingAITool
from director.tools.stabilityai import StabilityAITool
from director.tools.elevenlabs import ElevenLabsTool
from director.tools.videodb_tool import VDBAudioGenerationTool, VDBVideoGenerationTool, VideoDBTool

from .models import TEXT_TO_MOVIE_AGENT_PARAMETERS, ENGINE_CONFIGS
from .style_generator import StyleGenerator
from .video_processor import VideoProcessor


logger = logging.getLogger(__name__)


class TextToMovieAgent(BaseAgent):
    """Agent for generating movies from storylines using Gen AI models"""
    
    def __init__(self, session: Session, **kwargs):
        """Initialize agent with basic parameters"""
        self.agent_name = "text_to_movie"
        self.description = (
            "Agent for generating movies from storylines using Gen AI models"
        )
        self.parameters = TEXT_TO_MOVIE_AGENT_PARAMETERS
        self.llm = get_default_llm()
        self.engine_configs = ENGINE_CONFIGS
        super().__init__(session=session, **kwargs)

    def run(
        self,
        collection_id: str,
        engine: str = "stabilityai",
        audio_engine: str = "videodb",
        job_type: str = "text_to_movie",
        text_to_movie: Optional[dict] = None,
        *args,
        **kwargs,
    ) -> AgentResponse:
        """
        Process the storyline to generate a movie.

        :param collection_id: The collection ID to store generated assets
        :param engine: Video generation engine to use
        :return: AgentResponse containing information about generated movie
        """
        try:
            # Initialize tools and setup
            videodb_tool = VideoDBTool(collection_id=collection_id)
            self.output_message.actions.append("Processing input...")
            
            video_content = VideoContent(
                agent_name=self.agent_name,
                status=MsgStatus.progress,
                status_message="Generating movie...",
            )
            self.output_message.content.append(video_content)
            self.output_message.push_update()

            if engine not in self.engine_configs:
                raise ValueError(f"Unsupported engine: {engine}")

            # Initialize video generation tool
            video_gen_tool = self._initialize_video_tool(engine)
            video_gen_config_key = self._get_video_config_key(engine)
            
            # Initialize audio generation tool
            audio_gen_tool = self._initialize_audio_tool(audio_engine)
            audio_gen_config_key = "audio_elevenlabs_config"

            if job_type == "text_to_movie":
                return self._process_text_to_movie(
                    text_to_movie,
                    engine,
                    video_gen_tool,
                    audio_gen_tool,
                    videodb_tool,
                    video_gen_config_key,
                    audio_gen_config_key,
                    video_content
                )
            else:
                raise ValueError(f"Unsupported job type: {job_type}")

        except Exception as e:
            logger.exception(f"Error in {self.agent_name} agent: {e}")
            video_content.status = MsgStatus.error
            video_content.status_message = "Error generating movie"
            self.output_message.publish()
            return AgentResponse(
                status=AgentStatus.ERROR, message=f"Agent failed with error: {str(e)}"
            )

    def _initialize_video_tool(self, engine: str):
        """Initialize video generation tool based on engine"""
        if engine == "stabilityai":
            STABILITY_API_KEY = os.getenv("STABILITYAI_API_KEY")
            if not STABILITY_API_KEY:
                raise Exception("Stability AI API key not found")
            return StabilityAITool(api_key=STABILITY_API_KEY)
        elif engine == "kling":
            KLING_API_ACCESS_KEY = os.getenv("KLING_AI_ACCESS_API_KEY")
            KLING_API_SECRET_KEY = os.getenv("KLING_AI_SECRET_API_KEY")
            if not KLING_API_ACCESS_KEY or not KLING_API_SECRET_KEY:
                raise Exception("Kling AI API key not found")
            return KlingAITool(
                access_key=KLING_API_ACCESS_KEY, secret_key=KLING_API_SECRET_KEY
            )
        elif engine == "videodb":
            return VDBVideoGenerationTool()
        else:
            raise Exception(f"{engine} not supported")

    def _initialize_audio_tool(self, audio_engine: str):
        """Initialize audio generation tool based on engine"""
        if audio_engine == "elevenlabs":
            ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
            if not ELEVENLABS_API_KEY:
                raise Exception("ElevenLabs API key not found")
            return ElevenLabsTool(api_key=ELEVENLABS_API_KEY)
        else:
            return VDBAudioGenerationTool()

    def _get_video_config_key(self, engine: str) -> str:
        """Get configuration key for video generation"""
        if engine == "stabilityai":
            return "video_stabilityai_config"
        elif engine == "kling":
            return "video_kling_config"
        elif engine == "videodb":
            return "video_kling_config"
        else:
            raise Exception(f"Unknown engine: {engine}")

    def _process_text_to_movie(
        self,
        text_to_movie: dict,
        engine: str,
        video_gen_tool,
        audio_gen_tool,
        videodb_tool,
        video_gen_config_key: str,
        audio_gen_config_key: str,
        video_content: VideoContent
    ) -> AgentResponse:
        """Process text to movie generation"""
        raw_storyline = text_to_movie.get("storyline", [])
        video_gen_config = text_to_movie.get(video_gen_config_key, {})
        
        if engine == "videodb":
            audio_gen_config = {}
        else:
            audio_gen_config = text_to_movie.get(audio_gen_config_key, {})

        # Initialize processors
        style_generator = StyleGenerator(self.llm)
        video_processor = VideoProcessor(video_gen_tool, audio_gen_tool, videodb_tool)

        # Generate visual style
        visual_style = style_generator.generate_visual_style(raw_storyline)
        print("These are visual styles", visual_style)

        # Generate scenes
        scenes = style_generator.generate_scene_sequence(
            raw_storyline, visual_style, engine, self.engine_configs
        )
        print("These are scenes", scenes)

        self.output_message.actions.append(f"Generating {len(scenes)} videos...")
        self.output_message.push_update()

        # Generate videos
        generated_videos_results = video_processor.generate_videos(
            scenes, visual_style, engine, self.engine_configs,
            video_gen_config, self.output_message, style_generator
        )

        # Upload videos and get total duration
        total_duration = video_processor.upload_videos(
            generated_videos_results, scenes, self.output_message
        )

        # Generate audio prompt and background music
        sound_effects_description = style_generator.generate_audio_prompt(raw_storyline)
        sound_effects_media = video_processor.generate_audio(
            sound_effects_description, total_duration, audio_gen_config, self.output_message
        )

        self.output_message.actions.append("Combining assets into final video...")
        self.output_message.push_update()

        # Combine everything into final video
        final_video = video_processor.combine_assets(scenes, sound_effects_media)

        video_content.video = VideoData(stream_url=final_video)
        video_content.status = MsgStatus.success
        video_content.status_message = "Movie generation complete"
        self.output_message.publish()

        return AgentResponse(
            status=AgentStatus.SUCCESS,
            message="Movie generated successfully",
            data={"video_url": final_video},
        )
