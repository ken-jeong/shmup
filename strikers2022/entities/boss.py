"""Boss entity."""

import pygame
from .base import GameEntity
from ..config import BOSS_SIZE, BOSS_DEFAULT_HP, assets


class Boss(GameEntity):
    """Boss enemy entity."""

    def __init__(
        self,
        hp: int = BOSS_DEFAULT_HP,
        xpos: int = 0,
        ypos: int = 0,
        image_file: str = "boss.png",
    ):
        super().__init__()

        self.image = pygame.image.load(assets.get_image(image_file)).convert_alpha()
        self.image = pygame.transform.scale(self.image, BOSS_SIZE)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = xpos
        self.rect.y = ypos
        self.hp = hp
        self.dx = 0
        self.dy = 0
        self.sx, self.sy = BOSS_SIZE

    def update(self) -> None:
        """Update boss state. Currently stationary."""
        pass

    def take_damage(self, damage: int) -> bool:
        """Apply damage to boss.

        Args:
            damage: Amount of damage to apply

        Returns:
            True if boss is destroyed, False otherwise
        """
        self.hp -= damage
        return self.hp <= 0
