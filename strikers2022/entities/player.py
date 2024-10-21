"""Player entity and state management."""

import pygame
from .base import GameEntity
from ..config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PLAYER_SIZE,
    PLAYER_SPEED,
    ATTACK_COOLDOWN_BASE,
    ATTACK_SPEED_MULTIPLIER,
    MAX_WEAPON_SPEED_LEVEL,
    MAX_WEAPON_POWER_LEVEL,
    MAX_WEAPON_NUMBER_LEVEL,
    assets,
)


class PlayerState:
    """Encapsulates player-specific state."""

    def __init__(self):
        self.weapon_speed_level = 1
        self.weapon_power_level = 1
        self.weapon_number_level = 1

        # Attack state
        self.attack_go1 = False
        self.attack_go2 = False
        self.attack_counter = 0
        self.attack_cooldown = ATTACK_COOLDOWN_BASE

    @property
    def attack_delay(self) -> int:
        """Calculate attack delay based on weapon speed level."""
        return ATTACK_COOLDOWN_BASE - self.weapon_speed_level * ATTACK_SPEED_MULTIPLIER

    def can_attack(self) -> bool:
        """Check if player can attack."""
        return (
            self.attack_go1
            and self.attack_counter % self.attack_delay == 0
            and self.attack_go2
        )

    def start_attack(self) -> None:
        """Start attack sequence."""
        self.attack_go1 = True
        self.attack_counter = 0
        if self.attack_cooldown >= self.attack_delay:
            self.attack_go2 = True
            self.attack_cooldown = 0

    def stop_attack(self) -> None:
        """Stop attack sequence."""
        self.attack_go1 = False
        self.attack_go2 = False

    def update_counters(self) -> None:
        """Update attack counters each frame."""
        self.attack_counter += 1
        self.attack_cooldown += 1

    def upgrade_weapon_speed(self) -> None:
        """Upgrade weapon speed level."""
        if self.weapon_speed_level < MAX_WEAPON_SPEED_LEVEL:
            self.weapon_speed_level += 1

    def upgrade_weapon_power(self) -> None:
        """Upgrade weapon power level."""
        if self.weapon_power_level < MAX_WEAPON_POWER_LEVEL:
            self.weapon_power_level += 1

    def upgrade_weapon_number(self) -> None:
        """Upgrade weapon number level."""
        if self.weapon_number_level < MAX_WEAPON_NUMBER_LEVEL:
            self.weapon_number_level += 1

    def clamp_levels(self) -> None:
        """Ensure all levels are within maximum bounds."""
        self.weapon_speed_level = min(self.weapon_speed_level, MAX_WEAPON_SPEED_LEVEL)
        self.weapon_power_level = min(self.weapon_power_level, MAX_WEAPON_POWER_LEVEL)
        self.weapon_number_level = min(self.weapon_number_level, MAX_WEAPON_NUMBER_LEVEL)


class Player(GameEntity):
    """Player character entity."""

    def __init__(self, xpos: int, ypos: int, image_file: str):
        super().__init__()

        self.image = pygame.image.load(assets.get_image(image_file)).convert_alpha()
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = xpos
        self.rect.y = ypos

        self.sx, self.sy = PLAYER_SIZE
        self.dx = 0
        self.dy = 0

        # Player state
        self.state = PlayerState()

    def update(self) -> None:
        """Update player position with boundary checking."""
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Keep player within screen bounds
        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
            self.rect.x -= self.dx

        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy

    def move_left(self) -> None:
        """Start moving left."""
        self.dx = -PLAYER_SPEED

    def move_right(self) -> None:
        """Start moving right."""
        self.dx = PLAYER_SPEED

    def move_up(self) -> None:
        """Start moving up."""
        self.dy = -PLAYER_SPEED

    def move_down(self) -> None:
        """Start moving down."""
        self.dy = PLAYER_SPEED

    def stop_horizontal(self) -> None:
        """Stop horizontal movement."""
        self.dx = 0

    def stop_vertical(self) -> None:
        """Stop vertical movement."""
        self.dy = 0

    @property
    def center_x(self) -> float:
        """Get player center X coordinate."""
        return self.rect.x + self.sx / 2

    @property
    def center_y(self) -> float:
        """Get player center Y coordinate."""
        return self.rect.y + self.sy / 2
