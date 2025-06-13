"""
Agent Registry Package

This package contains the refactored agent registration system
split into multiple modules for better maintainability.
"""

from .core_agents import CORE_AGENTS
from .media_agents import MEDIA_AGENTS
from .ai_agents import AI_AGENTS
from .integration_agents import INTEGRATION_AGENTS
from .tiktok_agents import TIKTOK_AGENTS

# Combine all agent groups
ALL_AGENTS = [
    *CORE_AGENTS,
    *MEDIA_AGENTS,
    *AI_AGENTS,
    *INTEGRATION_AGENTS,
    *TIKTOK_AGENTS,
]

__all__ = [
    "CORE_AGENTS",
    "MEDIA_AGENTS", 
    "AI_AGENTS",
    "INTEGRATION_AGENTS",
    "TIKTOK_AGENTS",
    "ALL_AGENTS",
]
