"""Weapon entities for players and enemies."""

import math
import pygame
from .base import GameEntity
from ..config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PLAYER_WEAPON_SIZE,
    PLAYER_WEAPON_SPEED,
    ENEMY_WEAPON_SIZE,
    ENEMY_WEAPON_SPEED,
    assets,
)
from ..utils import calculate_angle, calculate_direction


class PlayerWeapon(GameEntity):
    """Player's weapon projectile."""

    _sound = None
    _sound_loaded = False
    _image_cache: dict[int, tuple[pygame.Surface, pygame.mask.Mask]] = {}

    def __init__(
        self,
        xpos: int,
        ypos: int,
        power_level: int,
        size: tuple[int, int] = PLAYER_WEAPON_SIZE,
        speed: int = PLAYER_WEAPON_SPEED,
    ):
        super().__init__()

        # Use cached image if available
        if power_level not in PlayerWeapon._image_cache:
            image_file = f"bullet_{power_level}.png"
            img = pygame.image.load(assets.get_image(image_file)).convert_alpha()
            img = pygame.transform.scale(img, size)
            mask = pygame.mask.from_surface(img)
            PlayerWeapon._image_cache[power_level] = (img, mask)

        self.image, self.mask = PlayerWeapon._image_cache[power_level]
        self.rect = self.image.get_rect()

        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

        # Load sound once for all instances
        if not PlayerWeapon._sound_loaded:
            try:
                PlayerWeapon._sound = pygame.mixer.Sound(
                    assets.get_sound("player_shoot.wav")
                )
            except pygame.error:
                PlayerWeapon._sound = None
            PlayerWeapon._sound_loaded = True

    def launch(self) -> None:
        """Play launch sound."""
        if PlayerWeapon._sound:
            try:
                PlayerWeapon._sound.play()
            except pygame.error:
                pass

    def update(self) -> None:
        """Update weapon position."""
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0:
            self.kill()


class EnemyWeapon(GameEntity):
    """Enemy's weapon projectile that tracks toward a target."""

    _image_cache: dict[str, pygame.Surface] = {}

    def __init__(
        self,
        xpos: int,
        ypos: int,
        target_x: float,
        target_y: float,
        size: tuple[int, int] = ENEMY_WEAPON_SIZE,
        speed: int = ENEMY_WEAPON_SPEED,
        image_file: str = "enemy1_bullet.png",
    ):
        super().__init__()

        # Use cached base image if available
        cache_key = f"{image_file}_{size}"
        if cache_key not in EnemyWeapon._image_cache:
            img = pygame.image.load(assets.get_image(image_file)).convert_alpha()
            img = pygame.transform.scale(img, size)
            EnemyWeapon._image_cache[cache_key] = img

        self.image = EnemyWeapon._image_cache[cache_key].copy()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = xpos
        self.rect.y = ypos
        self.sx, self.sy = size
        self.speed = speed

        # Store original image for rotation
        self.orig_image = self.image
        self.orig_center = self.rect.center

        # Calculate direction and rotate
        center_x = self.rect.x + self.sx / 2
        center_y = self.rect.y + self.sy / 2
        angle = calculate_angle(center_x, center_y, target_x, target_y)
        self.image = pygame.transform.rotate(self.orig_image, angle)

        # Store movement direction
        self.direction = calculate_direction(
            self.rect.x, self.rect.y, target_x, target_y
        )

    def update(self, *args, **kwargs) -> None:
        """Update weapon position along its trajectory."""
        self.rect.x += math.cos(self.direction) * self.speed
        self.rect.y += math.sin(self.direction) * self.speed

        # Remove if off screen
        if self.out_of_screen():
            self.kill()

    def out_of_screen(self) -> bool:
        """Check if weapon is outside screen bounds."""
        if self.rect.x + WINDOW_WIDTH < 0 or self.rect.x > WINDOW_WIDTH:
            return True
        if self.rect.y + WINDOW_HEIGHT < 0 or self.rect.y > WINDOW_HEIGHT:
            return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw with proper centering after rotation."""
        self.rect = self.image.get_rect(center=self.orig_center)
        surface.blit(self.image, self.rect)
