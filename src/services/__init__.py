"""
Eye Music - Services 模組
"""
from .ai_service import (
    AIService,
    ai_service,
    analyze_music_style,
    get_creative_suggestion,
    generate_video_description,
    generate_social_content,
    get_ai_service_status
)

__all__ = [
    'AIService',
    'ai_service',
    'analyze_music_style',
    'get_creative_suggestion',
    'generate_video_description',
    'generate_social_content',
    'get_ai_service_status'
]
