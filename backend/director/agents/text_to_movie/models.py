"""
Data models and configurations for TextToMovieAgent
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from director.tools.kling import PARAMS_CONFIG as KLING_PARAMS_CONFIG
from director.tools.stabilityai import PARAMS_CONFIG as STABILITYAI_PARAMS_CONFIG
from director.tools.elevenlabs import PARAMS_CONFIG as ELEVENLABS_PARAMS_CONFIG


# Constants
SUPPORTED_ENGINES = ["stabilityai", "kling", "videodb"]
SUPPORTED_AUDIO_ENGINES = ["elevenlabs", "videodb"]

# Agent Parameters Configuration
TEXT_TO_MOVIE_AGENT_PARAMETERS = {
    "type": "object",
    "properties": {
        "collection_id": {
            "type": "string",
            "description": "Collection ID to store the video",
        },
        "engine": {
            "type": "string",
            "description": "The video generation engine to use",
            "enum": SUPPORTED_ENGINES,
            "default": "videodb",
        },
        "audio_engine": {
            "type": "string",
            "description": "The audio generation engine to use",
            "enum": SUPPORTED_AUDIO_ENGINES,
            "default": "videodb",
        },
        "job_type": {
            "type": "string",
            "enum": ["text_to_movie"],
            "description": "The type of video generation to perform",
        },
        "text_to_movie": {
            "type": "object",
            "properties": {
                "storyline": {
                    "type": "string",
                    "description": "The storyline to generate the video",
                },
                "sound_effects_description": {
                    "type": "string",
                    "description": "Optional description for background music generation",
                    "default": None,
                },
                "video_stabilityai_config": {
                    "type": "object",
                    "description": "Optional configuration for StabilityAI engine",
                    "properties": STABILITYAI_PARAMS_CONFIG["text_to_video"],
                },
                "video_kling_config": {
                    "type": "object",
                    "description": "Optional configuration for Kling engine",
                    "properties": KLING_PARAMS_CONFIG["text_to_video"],
                },
                "audio_elevenlabs_config": {
                    "type": "object",
                    "description": "Optional configuration for ElevenLabs engine",
                    "properties": ELEVENLABS_PARAMS_CONFIG["sound_effect"],
                },
            },
            "required": ["storyline"],
        },
    },
    "required": ["job_type", "collection_id", "engine"],
}


@dataclass
class VideoGenResult:
    """Track results of video generation"""
    step_index: int
    video_path: Optional[str]
    success: bool
    error: Optional[str] = None
    video: Optional[dict] = None


@dataclass
class EngineConfig:
    """Configuration for different video generation engines"""
    name: str
    max_duration: int
    preferred_style: str
    prompt_format: str


@dataclass
class VisualStyle:
    """Visual style configuration for consistent movie generation"""
    camera_setup: str
    color_grading: str
    lighting_style: str
    movement_style: str
    film_mood: str
    director_reference: str
    character_constants: Dict
    setting_constants: Dict


# Engine configurations
ENGINE_CONFIGS = {
    "kling": EngineConfig(
        name="kling",
        max_duration=10,
        preferred_style="cinematic",
        prompt_format="detailed",
    ),
    "stabilityai": EngineConfig(
        name="stabilityai",
        max_duration=4,
        preferred_style="photorealistic",
        prompt_format="concise",
    ),
    "videodb": EngineConfig(
        name="kling",
        max_duration=6,
        preferred_style="cinematic",
        prompt_format="detailed",
    ),
}
