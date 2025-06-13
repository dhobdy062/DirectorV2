"""
TikTok-specific agents and workflows
"""

from director.agents.tiktok_viral_analysis import ViralPatternAnalysisAgent
from director.agents.tiktok_script_generator import TikTokScriptGeneratorAgent
from director.agents.tiktok_upload import TikTokUploadAgent
from director.agents.tiktok_workflow import TikTokMarketingWorkflow

TIKTOK_AGENTS = [
    ViralPatternAnalysisAgent,
    TikTokScriptGeneratorAgent,
    TikTokUploadAgent,
    TikTokMarketingWorkflow,
]
