"""Enemy entity."""

import pygame
from .base import GameEntity
from ..config import WINDOW_HEIGHT, ENEMY_SIZE, assets
from ..utils import calculate_angle


class Enemy(GameEntity):
    """Enemy entity that moves toward the player."""

    _image_cache: dict[str, pygame.Surface] = {}

    def __init__(
        self,
        hp: int,
        xpos: int,
        ypos: int,
        speed: int,
        size: tuple[int, int] = ENEMY_SIZE,
        image_file: str = "enemy1.png",
    ):
        super().__init__()

        # Use cached image if available
        cache_key = f"{image_file}_{size}"
        if cache_key not in Enemy._image_cache:
            img = pygame.image.load(assets.get_image(image_file)).convert_alpha()
            img = pygame.transform.scale(img, size)
            Enemy._image_cache[cache_key] = img

        self.orig_image = Enemy._image_cache[cache_key]
        self.image = self.orig_image.copy()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = xpos
        self.rect.y = ypos
        self.sx, self.sy = size
        self.speed = speed
        self.hp = hp

    def update(self, target_x: float = 0, target_y: float = 0) -> None:
        """Update enemy position and rotation toward target."""
        self.orig_center = self.rect.center

        # Rotate toward target
        center_x = self.rect.x + self.sx / 2
        center_y = self.rect.y + self.sy / 2
        angle = calculate_angle(center_x, center_y, target_x, target_y)
        self.image = pygame.transform.rotate(self.orig_image, angle)

        # Move down
        self.rect.y += self.speed

        # Remove if moved above screen (shouldn't happen in normal play)
        if self.rect.y < 0:
            self.kill()

    def out_of_screen(self) -> bool:
        """Check if enemy is outside screen bounds."""
        return self.rect.y < 0 or self.rect.y > WINDOW_HEIGHT

    def draw(self, surface: pygame.Surface) -> None:
        """Draw with proper centering after rotation."""
        self.rect = self.image.get_rect(center=self.orig_center)
        surface.blit(self.image, self.rect)

    def take_damage(self, damage: int) -> bool:
        """Apply damage to enemy.

        Args:
            damage: Amount of damage to apply

        Returns:
            True if enemy is destroyed, False otherwise
        """
        self.hp -= damage
        return self.hp <= 0
