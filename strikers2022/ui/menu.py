"""Game menu screens."""

import pygame
from ..config import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, YELLOW, assets
from .hud import draw_text
from .fonts import fonts


class GameMenu:
    """Main game menu."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_70 = fonts.get_font(70)
        self.font_40 = fonts.get_font(40)

        # Load background
        self.background = pygame.image.load(
            assets.get_image("background.png")
        ).convert_alpha()
        self.background = pygame.transform.scale(
            self.background, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def draw(self) -> None:
        """Draw the menu screen."""
        self.screen.blit(self.background, [0, 0])

        draw_x = int(WINDOW_WIDTH / 4)
        draw_y = int(WINDOW_HEIGHT / 4)

        draw_text(
            "STRIKERS 2022", self.font_70, self.screen, draw_x + 250, draw_y, YELLOW
        )
        draw_text(
            "PRESS ENTER KEY",
            self.font_40,
            self.screen,
            draw_x + 150,
            draw_y + 200,
            WHITE,
        )
        draw_text(
            "TO START THE GAME.",
            self.font_40,
            self.screen,
            draw_x + 150,
            draw_y + 250,
            WHITE,
        )

        pygame.display.update()

    def handle_events(self) -> str:
        """Handle menu events. Returns next game state."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "play"
            if event.type == pygame.QUIT:
                return "quit"

        return "game_menu"
