"""Spawn management for enemies and items."""

import random
import pygame
from ..entities import Enemy, Item, ItemType, create_item
from ..config import WINDOW_WIDTH, WINDOW_HEIGHT, ITEM_SPAWN_THRESHOLDS, ITEM_SPAWN_INTERVAL


class SpawnManager:
    """Manages spawning of enemies and items."""

    def __init__(self):
        # Track which boss HP thresholds have triggered item spawns
        self._spawn_triggered = {hp: False for hp in ITEM_SPAWN_THRESHOLDS}
        self._item_spawn_timer = 0

    def reset(self) -> None:
        """Reset spawn state for new game."""
        self._spawn_triggered = {hp: False for hp in ITEM_SPAWN_THRESHOLDS}
        self._item_spawn_timer = 0

    def spawn_enemies(
        self,
        enemy1_group: pygame.sprite.Group,
        enemy2_group: pygame.sprite.Group,
        shot_count: int,
        enemy_level: int,
        spawn_probability: int = 100,
    ) -> None:
        """Spawn enemies based on game progress.

        Args:
            enemy1_group: Group for enemies targeting player 1
            enemy2_group: Group for enemies targeting player 2
            shot_count: Current kill count (affects spawn rate and speed)
            enemy_level: Current enemy level (affects HP)
            spawn_probability: 1 in N chance of spawning (higher = less frequent)
        """
        if random.randint(1, spawn_probability) != 1:
            return

        # Calculate spawn parameters based on progress
        num_enemies = 1 + int(shot_count / 300)
        min_speed = 1 + int(shot_count / 200)
        max_speed = 1 + int(shot_count / 100)

        for _ in range(num_enemies):
            speed = random.randint(min_speed, max_speed)
            hp = 1 * enemy_level

            # Spawn enemy for player 1
            enemy1 = Enemy(
                hp=hp,
                xpos=random.randint(0, WINDOW_WIDTH - 50),
                ypos=5,
                speed=speed,
            )
            enemy1_group.add(enemy1)

            # Spawn enemy for player 2
            enemy2 = Enemy(
                hp=hp,
                xpos=random.randint(0, WINDOW_WIDTH - 50),
                ypos=5,
                speed=speed,
            )
            enemy2_group.add(enemy2)

    def spawn_items_for_boss_hp(
        self,
        boss_hp: int,
        heal_items: pygame.sprite.Group,
        weapon_power_items: pygame.sprite.Group,
        weapon_speed_items: pygame.sprite.Group,
        weapon_number_items: pygame.sprite.Group,
    ) -> bool:
        """Spawn items when boss HP reaches certain thresholds.

        Args:
            boss_hp: Current boss HP

        Returns:
            True if items were spawned (enemy level should increase)
        """
        spawned = False

        for threshold in ITEM_SPAWN_THRESHOLDS:
            if boss_hp <= threshold and not self._spawn_triggered[threshold]:
                self._spawn_triggered[threshold] = True
                spawned = True

                # Always spawn heal item
                heal_item = create_item(
                    ItemType.HEAL,
                    random.randrange(0, WINDOW_WIDTH - 40),
                )
                heal_items.add(heal_item)

                # Randomly spawn 2 of 3 upgrade item types
                item_choice = random.randint(1, 3)

                if item_choice == 1:
                    # Power + Speed
                    power_item = create_item(
                        ItemType.WEAPON_POWER,
                        random.randrange(0, WINDOW_WIDTH - 40),
                    )
                    weapon_power_items.add(power_item)

                    speed_item = create_item(
                        ItemType.WEAPON_SPEED,
                        random.randrange(0, WINDOW_WIDTH - 40),
                    )
                    weapon_speed_items.add(speed_item)

                elif item_choice == 2:
                    # Speed + Number
                    speed_item = create_item(
                        ItemType.WEAPON_SPEED,
                        random.randrange(0, WINDOW_WIDTH - 40),
                    )
                    weapon_speed_items.add(speed_item)

                    number_item = create_item(
                        ItemType.WEAPON_NUMBER,
                        random.randrange(0, WINDOW_WIDTH - 40),
                    )
                    weapon_number_items.add(number_item)

                else:
                    # Power + Number
                    power_item = create_item(
                        ItemType.WEAPON_POWER,
                        random.randrange(0, WINDOW_WIDTH - 40),
                    )
                    weapon_power_items.add(power_item)

                    number_item = create_item(
                        ItemType.WEAPON_NUMBER,
                        random.randrange(0, WINDOW_WIDTH - 40),
                    )
                    weapon_number_items.add(number_item)

        return spawned

    def spawn_items_periodic(
        self,
        heal_items: pygame.sprite.Group,
        weapon_power_items: pygame.sprite.Group,
        weapon_speed_items: pygame.sprite.Group,
        weapon_number_items: pygame.sprite.Group,
    ) -> None:
        """Spawn items periodically based on timer."""
        self._item_spawn_timer += 1

        if self._item_spawn_timer < ITEM_SPAWN_INTERVAL:
            return

        self._item_spawn_timer = 0

        # Spawn a random item
        item_choice = random.randint(1, 4)

        if item_choice == 1:
            heal_item = create_item(
                ItemType.HEAL,
                random.randrange(0, WINDOW_WIDTH - 40),
            )
            heal_items.add(heal_item)
        elif item_choice == 2:
            power_item = create_item(
                ItemType.WEAPON_POWER,
                random.randrange(0, WINDOW_WIDTH - 40),
            )
            weapon_power_items.add(power_item)
        elif item_choice == 3:
            speed_item = create_item(
                ItemType.WEAPON_SPEED,
                random.randrange(0, WINDOW_WIDTH - 40),
            )
            weapon_speed_items.add(speed_item)
        else:
            number_item = create_item(
                ItemType.WEAPON_NUMBER,
                random.randrange(0, WINDOW_WIDTH - 40),
            )
            weapon_number_items.add(number_item)
