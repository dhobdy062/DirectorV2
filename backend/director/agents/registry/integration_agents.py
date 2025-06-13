"""
Third-party integration agents
"""

from director.agents.slack_agent import SlackAgent
from director.agents.composio import ComposioAgent

INTEGRATION_AGENTS = [
    SlackAgent,
    ComposioAgent,
]
