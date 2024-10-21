"""Cross-platform font management."""

import os
import platform
import pygame


class FontManager:
    """Manages fonts across different platforms."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._font_path = None
            cls._instance._font_path_checked = False
            cls._instance._system = platform.system()
        return cls._instance

    def _get_system_font_path(self) -> str | None:
        """Get the appropriate font path for the current OS."""
        font_options = {
            "Windows": [
                "C:/Windows/Fonts/ariblk.ttf",
                "C:/Windows/Fonts/arial.ttf",
            ],
            "Darwin": [  # macOS
                "/System/Library/Fonts/Helvetica.ttc",
                "/Library/Fonts/Arial.ttf",
                "/System/Library/Fonts/SFNSDisplay.ttf",
            ],
            "Linux": [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
            ],
        }

        paths = font_options.get(self._system, [])
        for path in paths:
            if os.path.exists(path):
                return path

        return None

    def _ensure_font_path(self) -> None:
        """Lazy initialization of font path."""
        if not self._font_path_checked:
            self._font_path = self._get_system_font_path()
            self._font_path_checked = True

    def get_font(self, size: int) -> pygame.font.Font:
        """Get a font of the specified size."""
        self._ensure_font_path()

        if self._font_path:
            try:
                return pygame.font.Font(self._font_path, size)
            except (FileNotFoundError, OSError, pygame.error):
                pass

        # Fallback to pygame's default font
        return pygame.font.Font(None, size)


# Global instance
fonts = FontManager()
