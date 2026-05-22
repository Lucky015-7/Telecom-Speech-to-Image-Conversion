"""
Scene vocabulary management for Voice-to-Image system
"""

from backend.config import SCENE_VOCABULARY, SCENE_CATEGORIES


def get_all_scenes():
    """Get all scene descriptions"""
    return SCENE_VOCABULARY


def get_scenes_by_category(category):
    """Get scenes for a specific category"""
    return SCENE_CATEGORIES.get(category, [])


def get_categories():
    """Get all category names"""
    return list(SCENE_CATEGORIES.keys())


def search_scenes(query):
    """Search scenes by keyword"""
    query_lower = query.lower()
    return [scene for scene in SCENE_VOCABULARY if query_lower in scene.lower()]
