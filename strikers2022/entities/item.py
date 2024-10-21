"""Item entities."""

from enum import Enum, auto
import pygame
from .base import GameEntity
from ..config import ITEM_SIZE, ITEM_SPEED, assets


class ItemType(Enum):
    """Types of collectible items."""

    HEAL = auto()
    WEAPON_POWER = auto()
    WEAPON_SPEED = auto()
    WEAPON_NUMBER = auto()


ITEM_IMAGES = {
    ItemType.HEAL: "heal_item.png",
    ItemType.WEAPON_POWER: "power_item.png",
    ItemType.WEAPON_SPEED: "attack_speed_item.png",
    ItemType.WEAPON_NUMBER: "weapon_count_item.png",
}


class Item(GameEntity):
    """Collectible item entity."""

    def __init__(
        self,
        item_type: ItemType,
        xpos: int,
        ypos: int,
        size: tuple[int, int] = ITEM_SIZE,
    ):
        super().__init__()

        self.item_type = item_type
        image_file = ITEM_IMAGES[item_type]

        self.image = pygame.image.load(assets.get_image(image_file)).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = ITEM_SPEED
        self.sx, self.sy = size

    def update(self) -> None:
        """Update item position (falls down)."""
        self.rect.y += self.speed
        if self.rect.y > 1000:  # Off screen
            self.kill()


def create_item(item_type: ItemType, xpos: int, ypos: int = 10) -> Item:
    """Factory function to create items."""
    return Item(item_type, xpos, ypos)
