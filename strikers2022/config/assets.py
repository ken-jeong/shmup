"""Asset path management."""

import os
from pathlib import Path


class AssetManager:
    """Manages asset paths for images, sounds, and music."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Get the project root directory (parent of strikers2022 package)
        self._package_dir = Path(__file__).parent.parent
        self._project_dir = self._package_dir.parent

        self._image_path = self._project_dir / "images"
        self._sound_path = self._project_dir / "sounds"
        self._music_path = self._project_dir / "musics"

        self._initialized = True

    @property
    def image_path(self) -> Path:
        return self._image_path

    @property
    def sound_path(self) -> Path:
        return self._sound_path

    @property
    def music_path(self) -> Path:
        return self._music_path

    def get_image(self, filename: str) -> str:
        """Get full path to an image file."""
        return str(self._image_path / filename)

    def get_sound(self, filename: str) -> str:
        """Get full path to a sound file."""
        return str(self._sound_path / filename)

    def get_music(self, filename: str) -> str:
        """Get full path to a music file."""
        return str(self._music_path / filename)


# Global instance
assets = AssetManager()
