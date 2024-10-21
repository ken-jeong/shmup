"""Base entity class for all game objects."""

from abc import ABC, abstractmethod
import pygame


class GameEntity(ABC, pygame.sprite.Sprite):
    """Abstract base class for all game entities."""

    def __init__(self):
        super().__init__()
        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None
        self.mask: pygame.mask.Mask = None

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Update entity state."""
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """Draw entity on surface."""
        if self.image and self.rect:
            surface.blit(self.image, self.rect)

    def crash(self, sprites: pygame.sprite.Group) -> pygame.sprite.Sprite | None:
        """Check collision with a group of sprites.

        Args:
            sprites: Group of sprites to check collision against

        Returns:
            The first colliding sprite, or None if no collision
        """
        for sprite in sprites:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite
        return None
