"""
Core video processing agents
"""

from director.agents.frame import FrameAgent
from director.agents.summarize_video import SummarizeVideoAgent
from director.agents.download import DownloadAgent
from director.agents.upload import UploadAgent
from director.agents.search import SearchAgent
from director.agents.prompt_clip import PromptClipAgent
from director.agents.index import IndexAgent
from director.agents.stream_video import StreamVideoAgent
from director.agents.subtitle import SubtitleAgent
from director.agents.editing import EditingAgent
from director.agents.transcription import TranscriptionAgent
from director.agents.comparison import ComparisonAgent
from director.agents.pricing import PricingAgent

CORE_AGENTS = [
    SummarizeVideoAgent,
    UploadAgent,
    IndexAgent,
    SearchAgent,
    PromptClipAgent,
    FrameAgent,
    DownloadAgent,
    StreamVideoAgent,
    SubtitleAgent,
    EditingAgent,
    TranscriptionAgent,
    ComparisonAgent,
    PricingAgent,
]
