"""
AI-powered generation and processing agents
"""

from director.agents.image_generation import ImageGenerationAgent
from director.agents.audio_generation import AudioGenerationAgent
from director.agents.video_generation import VideoGenerationAgent
from director.agents.text_to_movie import TextToMovieAgent
from director.agents.code_assistant import CodeAssistantAgent
from director.agents.web_search_agent import WebSearchAgent

AI_AGENTS = [
    ImageGenerationAgent,
    AudioGenerationAgent,
    VideoGenerationAgent,
    TextToMovieAgent,
    CodeAssistantAgent,
    WebSearchAgent,
]
