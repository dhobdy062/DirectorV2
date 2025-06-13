"""
Media processing and generation agents
"""

from director.agents.censor import CensorAgent
from director.agents.dubbing import DubbingAgent
from director.agents.clone_voice import CloneVoiceAgent
from director.agents.voice_replacement import VoiceReplacementAgent

MEDIA_AGENTS = [
    CensorAgent,
    DubbingAgent,
    CloneVoiceAgent,
    VoiceReplacementAgent,
]
