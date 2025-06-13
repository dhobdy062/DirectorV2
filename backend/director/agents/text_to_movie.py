"""
DEPRECATED: This file is kept for backward compatibility.
The TextToMovieAgent has been refactored into a modular package.
Please import from director.agents.text_to_movie instead.
"""

# Import the refactored agent for backward compatibility
from director.agents.text_to_movie import TextToMovieAgent

# Re-export for backward compatibility
__all__ = ["TextToMovieAgent"]


