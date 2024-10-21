"""Input handling manager."""

import pygame
from ..entities import Player


class InputManager:
    """Handles input for both players."""

    # Player 1 key bindings (arrow keys + numpad 0)
    P1_LEFT = pygame.K_LEFT
    P1_RIGHT = pygame.K_RIGHT
    P1_UP = pygame.K_UP
    P1_DOWN = pygame.K_DOWN
    P1_ATTACK = pygame.K_KP0

    # Player 2 key bindings (WASD + Space)
    P2_LEFT = pygame.K_a
    P2_RIGHT = pygame.K_d
    P2_UP = pygame.K_w
    P2_DOWN = pygame.K_s
    P2_ATTACK = pygame.K_SPACE

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle a single input event.

        Args:
            event: Pygame event to process

        Returns:
            True if game should quit, False otherwise
        """
        if event.type == pygame.QUIT:
            return True

        if event.type == pygame.KEYDOWN:
            self._handle_keydown(event.key)
        elif event.type == pygame.KEYUP:
            self._handle_keyup(event.key)

        return False

    def _handle_keydown(self, key: int) -> None:
        """Handle key press."""
        # Player 1 movement
        if key == self.P1_LEFT:
            self.player1.move_left()
        elif key == self.P1_RIGHT:
            self.player1.move_right()
        elif key == self.P1_UP:
            self.player1.move_up()
        elif key == self.P1_DOWN:
            self.player1.move_down()
        elif key == self.P1_ATTACK:
            self.player1.state.start_attack()

        # Player 2 movement
        if key == self.P2_LEFT:
            self.player2.move_left()
        elif key == self.P2_RIGHT:
            self.player2.move_right()
        elif key == self.P2_UP:
            self.player2.move_up()
        elif key == self.P2_DOWN:
            self.player2.move_down()
        elif key == self.P2_ATTACK:
            self.player2.state.start_attack()

    def _handle_keyup(self, key: int) -> None:
        """Handle key release."""
        # Player 1
        if key in (self.P1_LEFT, self.P1_RIGHT):
            self.player1.stop_horizontal()
        elif key in (self.P1_UP, self.P1_DOWN):
            self.player1.stop_vertical()
        elif key == self.P1_ATTACK:
            self.player1.state.stop_attack()

        # Player 2
        if key in (self.P2_LEFT, self.P2_RIGHT):
            self.player2.stop_horizontal()
        elif key in (self.P2_UP, self.P2_DOWN):
            self.player2.stop_vertical()
        elif key == self.P2_ATTACK:
            self.player2.state.stop_attack()
