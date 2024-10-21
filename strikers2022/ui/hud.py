"""HUD (Heads-Up Display) for game information."""

import pygame
from ..config import WHITE, YELLOW, RED


def draw_text(
    text: str,
    font: pygame.font.Font,
    surface: pygame.Surface,
    x: int,
    y: int,
    color: tuple[int, int, int],
) -> None:
    """Draw centered text on the surface."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)


class HUD:
    """Heads-Up Display for game statistics."""

    def __init__(self, font: pygame.font.Font):
        self.font = font

    def draw(
        self,
        surface: pygame.Surface,
        kill_count: int,
        miss_count: int,
        elapsed_time,
        players_hp: int,
        boss_hp: int,
        enemy_level: int,
    ) -> None:
        """Draw all HUD elements."""
        # Left side - stats
        draw_text(f"kill: {kill_count}", self.font, surface, 50, 20, YELLOW)
        draw_text(f"loss: {miss_count}", self.font, surface, 50, 50, RED)
        draw_text(f"time: {elapsed_time}", self.font, surface, 80, 80, WHITE)

        # Right side - HP and level
        draw_text(f"players hp: {players_hp}", self.font, surface, 920, 20, WHITE)
        draw_text(f"boss hp: {boss_hp}", self.font, surface, 920, 50, WHITE)
        draw_text(f"enemy level: {enemy_level}", self.font, surface, 915, 80, WHITE)
