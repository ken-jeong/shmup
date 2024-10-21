"""Main Game class containing the game loop."""

from datetime import datetime
import pygame

from .config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    PLAYER_HP,
    BOSS_DEFAULT_HP,
    ENEMY_SPAWN_PROBABILITY,
    ENEMY_ATTACK_INTERVAL,
    assets,
)
from .entities import Player, Boss, PlayerWeapon, EnemyWeapon, ItemType
from .managers import (
    InputManager,
    CollisionManager,
    SpawnManager,
    audio,
    occur_explosion,
    occur_get_item,
)
from .ui import HUD, fonts


class Game:
    """Main game class managing the game loop and state."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = False

        # Load resources
        self._load_resources()

    def _load_resources(self) -> None:
        """Load game resources."""
        self.default_font = fonts.get_font(20)
        self.background = pygame.image.load(
            assets.get_image("background.png")
        ).convert_alpha()
        self.background = pygame.transform.scale(
            self.background, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        # Load sounds
        audio.load_sounds()

    def _create_entities(self) -> None:
        """Create game entities."""
        # Boss
        self.boss = Boss(
            hp=BOSS_DEFAULT_HP,
            xpos=round(WINDOW_WIDTH * 1 / 2 - 250),
            ypos=0,
        )

        # Players
        self.player1 = Player(
            xpos=round(WINDOW_WIDTH * 2 / 3 - 25),
            ypos=WINDOW_HEIGHT - 80,
            image_file="player1.png",
        )
        self.player2 = Player(
            xpos=round(WINDOW_WIDTH * 1 / 3 - 25),
            ypos=WINDOW_HEIGHT - 80,
            image_file="player2.png",
        )

    def _create_sprite_groups(self) -> None:
        """Create sprite groups for entities."""
        self.player1_weapons = pygame.sprite.Group()
        self.player2_weapons = pygame.sprite.Group()

        self.enemy1s = pygame.sprite.Group()
        self.enemy2s = pygame.sprite.Group()

        self.enemy1_weapons = pygame.sprite.Group()
        self.enemy2_weapons = pygame.sprite.Group()

        self.weapon_power_items = pygame.sprite.Group()
        self.weapon_speed_items = pygame.sprite.Group()
        self.weapon_number_items = pygame.sprite.Group()
        self.heal_items = pygame.sprite.Group()

    def _create_managers(self) -> None:
        """Create manager instances."""
        self.input_manager = InputManager(self.player1, self.player2)
        self.collision_manager = CollisionManager(
            self.player1, self.player2, self.boss, self.screen
        )
        self.collision_manager.set_effects(occur_explosion, occur_get_item)
        self.spawn_manager = SpawnManager()

    def _reset_game_state(self) -> None:
        """Reset game state variables."""
        self.shot_count = 0
        self.count_missed = 0
        self.players_hp = PLAYER_HP
        self.enemy_level = 1
        self.enemy_attack_counter = 0

        # Time tracking
        self.start_time = datetime.now().replace(microsecond=0)

    def _handle_player_attack(
        self, player: Player, weapons: pygame.sprite.Group
    ) -> None:
        """Handle weapon firing for a player."""
        state = player.state

        if not state.can_attack():
            return

        power_level = state.weapon_power_level
        number_level = state.weapon_number_level

        # Calculate weapon positions based on number level
        if number_level == 1:
            positions = [player.rect.centerx - 5]
        elif number_level == 2:
            positions = [
                player.rect.x + player.sx / 4 * (2 * i + 1) - 5 for i in range(2)
            ]
        elif number_level == 3:
            positions = [player.rect.x + player.sx / 3 * i - 5 for i in range(4)]
        else:  # 4
            positions = [player.rect.x + player.sx / 4 * i - 5 for i in range(5)]

        # Create weapons
        for xpos in positions:
            weapon = PlayerWeapon(
                xpos=int(xpos),
                ypos=player.rect.centery - 40,
                power_level=power_level,
            )
            weapon.launch()
            weapons.add(weapon)

    def _spawn_enemy_weapons(self) -> None:
        """Spawn enemy weapons at regular intervals."""
        if self.enemy_attack_counter % ENEMY_ATTACK_INTERVAL != 0:
            return

        # Enemy1 weapons targeting player1
        for enemy in self.enemy1s:
            weapon = EnemyWeapon(
                xpos=enemy.rect.centerx - 5,
                ypos=enemy.rect.centery,
                target_x=self.player1.center_x,
                target_y=self.player1.center_y,
            )
            self.enemy1_weapons.add(weapon)

        # Enemy2 weapons targeting player2
        for enemy in self.enemy2s:
            weapon = EnemyWeapon(
                xpos=enemy.rect.centerx - 5,
                ypos=enemy.rect.centery,
                target_x=self.player2.center_x,
                target_y=self.player2.center_y,
            )
            self.enemy2_weapons.add(weapon)

    def _process_missed_enemies(self) -> None:
        """Check for enemies that left the screen."""
        for enemy in list(self.enemy1s):
            if enemy.out_of_screen():
                enemy.kill()
                self.count_missed += 1

        for enemy in list(self.enemy2s):
            if enemy.out_of_screen():
                enemy.kill()
                self.count_missed += 1

    def _process_offscreen_weapons(self) -> None:
        """Remove weapons that left the screen."""
        for weapon in list(self.enemy1_weapons):
            if weapon.out_of_screen():
                weapon.kill()

        for weapon in list(self.enemy2_weapons):
            if weapon.out_of_screen():
                weapon.kill()

    def _process_collisions(self) -> None:
        """Process all collisions."""
        cm = self.collision_manager
        enemy_groups = [self.enemy1s, self.enemy2s]
        weapon_groups = [self.enemy1_weapons, self.enemy2_weapons]

        # Player weapons vs enemies
        self.shot_count += cm.check_player_weapon_vs_enemies(
            self.player1_weapons,
            enemy_groups,
            self.player1.state.weapon_power_level,
        )
        self.shot_count += cm.check_player_weapon_vs_enemies(
            self.player2_weapons,
            enemy_groups,
            self.player2.state.weapon_power_level,
        )

        # Players vs enemies
        self.players_hp -= cm.check_player_vs_enemies(
            self.player1, enemy_groups, self.enemy_level
        )
        self.players_hp -= cm.check_player_vs_enemies(
            self.player2, enemy_groups, self.enemy_level
        )

        # Players vs enemy weapons
        self.players_hp -= cm.check_player_vs_enemy_weapons(
            self.player1, weapon_groups, self.enemy_level
        )
        self.players_hp -= cm.check_player_vs_enemy_weapons(
            self.player2, weapon_groups, self.enemy_level
        )

        # Player weapons vs boss
        cm.check_boss_vs_player_weapons(
            self.player1_weapons, self.player1.state.weapon_power_level
        )
        cm.check_boss_vs_player_weapons(
            self.player2_weapons, self.player2.state.weapon_power_level
        )

        # Players vs items
        for player in (self.player1, self.player2):
            cm.check_player_vs_items(
                player, self.weapon_number_items, ItemType.WEAPON_NUMBER
            )
            cm.check_player_vs_items(
                player, self.weapon_power_items, ItemType.WEAPON_POWER
            )
            cm.check_player_vs_items(
                player, self.weapon_speed_items, ItemType.WEAPON_SPEED
            )

        # Heal items (shared HP)
        self.players_hp += cm.check_player_vs_heal_items(self.heal_items)

        # Clamp player levels
        self.player1.state.clamp_levels()
        self.player2.state.clamp_levels()

        # Remove collided sprites
        cm.remove_collided_sprites(
            self.enemy1s,
            self.enemy2s,
            self.enemy1_weapons,
            self.enemy2_weapons,
            self.player1_weapons,
            self.player2_weapons,
            [
                self.weapon_power_items,
                self.weapon_speed_items,
                self.weapon_number_items,
                self.heal_items,
            ],
        )

    def _update_entities(self) -> None:
        """Update all entities."""
        # Enemies
        self.enemy1s.update(self.player1.center_x, self.player1.center_y)
        self.enemy2s.update(self.player2.center_x, self.player2.center_y)

        # Enemy weapons
        self.enemy1_weapons.update(self.player1.center_x, self.player1.center_y)
        self.enemy2_weapons.update(self.player2.center_x, self.player2.center_y)

        # Player weapons
        self.player1_weapons.update()
        self.player2_weapons.update()

        # Players
        self.player1.update()
        self.player2.update()

        # Boss
        self.boss.update()

        # Items
        self.weapon_number_items.update()
        self.weapon_speed_items.update()
        self.weapon_power_items.update()
        self.heal_items.update()

    def _draw_entities(self) -> None:
        """Draw all entities."""
        self.enemy1s.draw(self.screen)
        self.enemy2s.draw(self.screen)

        self.enemy1_weapons.draw(self.screen)
        self.enemy2_weapons.draw(self.screen)

        self.player1_weapons.draw(self.screen)
        self.player2_weapons.draw(self.screen)

        self.player1.draw(self.screen)
        self.player2.draw(self.screen)

        self.boss.draw(self.screen)

        self.weapon_number_items.draw(self.screen)
        self.weapon_speed_items.draw(self.screen)
        self.weapon_power_items.draw(self.screen)
        self.heal_items.draw(self.screen)

    def _check_game_over(self) -> str | None:
        """Check for game over conditions.

        Returns:
            "gameover" if players lost, "gameclear" if boss defeated, None otherwise
        """
        # Clamp HP values
        if self.players_hp <= 0:
            self.players_hp = 0
        if self.boss.hp <= 0:
            self.boss.hp = 0

        if self.players_hp == 0:
            return "gameover"
        if self.boss.hp == 0:
            return "gameclear"

        return None

    def run(self) -> str:
        """Run the game loop.

        Returns:
            Next game state ("game_menu")
        """
        # Initialize game
        self._create_entities()
        self._create_sprite_groups()
        self._create_managers()
        self._reset_game_state()

        # Start music
        audio.play_music()

        # Create HUD
        hud = HUD(self.default_font)

        self.running = True
        while self.running:
            # Calculate elapsed time
            now = datetime.now().replace(microsecond=0)
            elapsed_time = now - self.start_time

            # Handle input
            for event in pygame.event.get():
                if self.input_manager.handle_event(event):
                    self.running = False

            # Handle player attacks
            self._handle_player_attack(self.player1, self.player1_weapons)
            self._handle_player_attack(self.player2, self.player2_weapons)

            # Update attack counters
            self.player1.state.update_counters()
            self.player2.state.update_counters()

            # Draw background
            self.screen.blit(self.background, self.background.get_rect())

            # Spawn enemies
            self.spawn_manager.spawn_enemies(
                self.enemy1s,
                self.enemy2s,
                self.shot_count,
                self.enemy_level,
                ENEMY_SPAWN_PROBABILITY,
            )

            # Draw HUD
            hud.draw(
                self.screen,
                self.shot_count,
                self.count_missed,
                elapsed_time,
                self.players_hp,
                self.boss.hp,
                self.enemy_level,
            )

            # Spawn items based on boss HP
            if self.spawn_manager.spawn_items_for_boss_hp(
                self.boss.hp,
                self.heal_items,
                self.weapon_power_items,
                self.weapon_speed_items,
                self.weapon_number_items,
            ):
                self.enemy_level += 1

            # Spawn items periodically
            self.spawn_manager.spawn_items_periodic(
                self.heal_items,
                self.weapon_power_items,
                self.weapon_speed_items,
                self.weapon_number_items,
            )

            # Spawn enemy weapons
            self._spawn_enemy_weapons()
            self.enemy_attack_counter += 1

            # Process missed enemies and offscreen weapons
            self._process_missed_enemies()
            self._process_offscreen_weapons()

            # Update and draw entities
            self._update_entities()
            self._draw_entities()

            pygame.display.flip()

            # Process collisions
            self._process_collisions()

            # Check game over
            result = self._check_game_over()
            if result:
                audio.stop_music()
                pygame.display.update()

                if result == "gameover":
                    audio.play_sound("gameover")
                else:
                    audio.play_sound("gameclear")

                pygame.time.wait(1000)
                self.running = False

            # Maintain FPS
            self.clock.tick(FPS)

        return "game_menu"
