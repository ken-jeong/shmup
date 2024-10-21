"""Main entry point for STRIKERS 2022."""

import pygame

from .config import WINDOW_WIDTH, WINDOW_HEIGHT
from .game import Game
from .ui import GameMenu


def main() -> None:
    """Main function to run the game."""
    pygame.init()

    # Try to initialize mixer (may fail in some environments like WSL)
    try:
        pygame.mixer.init()
    except pygame.error:
        print("Warning: Audio mixer could not be initialized. Game will run without sound.")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("STRIKERS 2022")

    menu = GameMenu(screen)
    game = Game(screen)

    action = "game_menu"

    while action != "quit":
        if action == "game_menu":
            menu.draw()
            action = menu.handle_events()
        elif action == "play":
            action = game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
