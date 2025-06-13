"""
Visual style generation for TextToMovieAgent
"""

import json
from typing import List
from director.core.session import ContextMessage, RoleTypes
from director.llm.base import LLMResponse
from .models import VisualStyle, EngineConfig


class StyleGenerator:
    """Handles visual style generation and scene creation"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def generate_visual_style(self, storyline: str) -> VisualStyle:
        """Generate consistent visual style for entire film."""
        style_prompt = f"""
        As a cinematographer, define a consistent visual style for this short film:
        Storyline: {storyline}
        
        Return a JSON response with visual style parameters:
        {{
            "camera_setup": "Camera and lens combination",
            "color_grading": "Color grading style and palette",
            "lighting_style": "Core lighting approach",
            "movement_style": "Camera movement philosophy",
            "film_mood": "Overall atmospheric mood",
            "director_reference": "Key director's style to reference",
            "character_constants": {{
                "physical_description": "Consistent character details",
                "costume_details": "Consistent costume elements"
            }},
            "setting_constants": {{
                "time_period": "When this takes place",
                "environment": "Core setting elements that stay consistent"
            }}
        }}
        """

        style_message = ContextMessage(content=style_prompt, role=RoleTypes.user)
        llm_response = self.llm.chat_completions(
            [style_message.to_llm_msg()], response_format={"type": "json_object"}
        )
        return VisualStyle(**json.loads(llm_response.content))

    def generate_scene_sequence(
        self, storyline: str, style: VisualStyle, engine: str, engine_configs: dict
    ) -> List[dict]:
        """Generate 3-5 scenes with visual and narrative consistency."""
        engine_config = engine_configs[engine]

        sequence_prompt = f"""
        Break this storyline into 3 distinct scenes maintaining visual consistency.
        Generate scene descriptions optimized for {engine} {engine_config.preferred_style} style.
        
        Visual Style:
        - Camera/Lens: {style.camera_setup}
        - Color Grade: {style.color_grading}
        - Lighting: {style.lighting_style}
        - Movement: {style.movement_style}
        - Mood: {style.film_mood}
        - Director Style: {style.director_reference}
        
        Character Constants:
        {json.dumps(style.character_constants, indent=2)}
        
        Setting Constants:
        {json.dumps(style.setting_constants, indent=2)}
        
        Maximum duration per scene: {engine_config.max_duration} seconds
        
        Storyline: {storyline}

        Return a JSON array of scenes with:
        {{
            "story_beat": "What happens in this scene",
            "scene_description": "Visual description optimized for {engine}",
            "suggested_duration": "Duration as integer in seconds (max {engine_config.max_duration})"
        }}
        Make sure suggested_duration is a number, not a string.
        """

        sequence_message = ContextMessage(content=sequence_prompt, role=RoleTypes.user)
        llm_response = self.llm.chat_completions(
            [sequence_message.to_llm_msg()], response_format={"type": "json_object"}
        )
        scenes_data = json.loads(llm_response.content)["scenes"]

        # Ensure durations are integers
        for scene in scenes_data:
            try:
                scene["suggested_duration"] = int(scene.get("suggested_duration", 5))
            except (ValueError, TypeError):
                scene["suggested_duration"] = 5

        return scenes_data

    def generate_engine_prompt(
        self, scene: dict, style: VisualStyle, engine: str
    ) -> str:
        """Generate engine-specific prompt"""
        if engine == "stabilityai":
            return f"""
            {style.director_reference} style.
            {scene['scene_description']}.
            {style.character_constants['physical_description']}.
            {style.lighting_style}, {style.color_grading}.
            Photorealistic, detailed, high quality, masterful composition.
            """
        else:  # Kling
            initial_prompt = f"""
            {style.director_reference} style shot. 
            Filmed on {style.camera_setup}.
            
            {scene['scene_description']}
            
            Character Details:
            {json.dumps(style.character_constants, indent=2)}
            
            Setting Elements:
            {json.dumps(style.setting_constants, indent=2)}
            
            {style.lighting_style} lighting.
            {style.color_grading} color palette.
            {style.movement_style} camera movement.
            
            Mood: {style.film_mood}
            """

            # Run through LLM to compress while maintaining structure
            compression_prompt = f"""
            Compress the following prompt to under 2450 characters while maintaining its structure and key information:

            {initial_prompt}
            """

            compression_message = ContextMessage(
                content=compression_prompt, role=RoleTypes.user
            )
            llm_response = self.llm.chat_completions(
                [compression_message.to_llm_msg()], response_format={"type": "text"}
            )
            return llm_response.content.strip()

    def generate_audio_prompt(self, storyline: str) -> str:
        """Generate audio prompt for background music"""
        audio_prompt = f"""
        Create a background music description for this storyline:
        {storyline}
        
        Focus on:
        - Musical genre and style
        - Emotional tone
        - Instrumentation
        - Tempo and rhythm
        
        Keep it concise but descriptive for audio generation.
        """
        
        audio_message = ContextMessage(content=audio_prompt, role=RoleTypes.user)
        llm_response = self.llm.chat_completions(
            [audio_message.to_llm_msg()], response_format={"type": "text"}
        )
        return llm_response.content.strip()
