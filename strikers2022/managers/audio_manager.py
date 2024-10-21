"""Audio management for sounds and music."""

import pygame
from ..config import assets


class AudioManager:
    """Manages game audio: music and sound effects."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._initialized = True

    def load_sounds(self) -> None:
        """Pre-load commonly used sounds."""
        sound_files = {
            "explosion": "explosion.wav",
            "get_item": "item_pickup.wav",
            "gameover": "game_over.wav",
            "gameclear": "game_clear.wav",
        }

        for name, filename in sound_files.items():
            try:
                self._sounds[name] = pygame.mixer.Sound(assets.get_sound(filename))
            except pygame.error:
                print(f"Warning: Could not load sound {filename}")

    def play_sound(self, name: str) -> None:
        """Play a named sound effect."""
        if name in self._sounds:
            self._sounds[name].play()

    def play_music(self, loop: bool = True) -> None:
        """Play background music."""
        try:
            pygame.mixer.music.load(assets.get_music("bgm.wav"))
            pygame.mixer.music.play(-1 if loop else 0)
        except pygame.error:
            print("Warning: Could not load background music")

    def stop_music(self) -> None:
        """Stop background music."""
        pygame.mixer.music.stop()

    def get_sound(self, name: str) -> pygame.mixer.Sound | None:
        """Get a sound by name."""
        return self._sounds.get(name)


# Global instance
audio = AudioManager()


def occur_explosion(
    surface: pygame.Surface, x: int, y: int, xsize: int, ysize: int
) -> None:
    """Display explosion effect at position.

    This function maintains compatibility with the original API.
    """
    try:
        explosion_image = pygame.image.load(
            assets.get_image("explosion.png")
        ).convert_alpha()
        explosion_image = pygame.transform.scale(explosion_image, (xsize, ysize))
        explosion_rect = explosion_image.get_rect()
        explosion_rect.x = x
        explosion_rect.y = y
        surface.blit(explosion_image, explosion_rect)
        audio.play_sound("explosion")
    except pygame.error:
        pass


def occur_get_item() -> None:
    """Play item pickup sound.

    This function maintains compatibility with the original API.
    """
    audio.play_sound("get_item")
