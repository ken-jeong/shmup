"""Collision handling manager."""

import pygame
from ..entities import Player, Boss, ItemType
from ..config import HEAL_AMOUNT


class CollisionManager:
    """Handles all collision detection and response."""

    def __init__(
        self,
        player1: Player,
        player2: Player,
        boss: Boss,
        screen: pygame.Surface,
    ):
        self.player1 = player1
        self.player2 = player2
        self.boss = boss
        self.screen = screen

        # Explosion effect
        self._explosion_func = None
        self._get_item_func = None

    def set_effects(self, explosion_func, get_item_func) -> None:
        """Set effect callback functions."""
        self._explosion_func = explosion_func
        self._get_item_func = get_item_func

    def _trigger_explosion(self, x: int, y: int, width: int, height: int) -> None:
        """Trigger explosion effect if available."""
        if self._explosion_func:
            self._explosion_func(self.screen, x, y, width, height)

    def _trigger_item_pickup(self) -> None:
        """Trigger item pickup sound if available."""
        if self._get_item_func:
            self._get_item_func()

    def check_player_weapon_vs_enemies(
        self,
        weapons: pygame.sprite.Group,
        enemy_groups: list[pygame.sprite.Group],
        power_level: int,
    ) -> int:
        """Check player weapon collisions with enemies.

        Returns:
            Number of enemies killed
        """
        kills = 0
        for weapon in list(weapons):
            for enemies in enemy_groups:
                enemy = weapon.crash(enemies)
                if enemy:
                    weapon.kill()
                    if enemy.take_damage(power_level):
                        enemy.kill()
                        self._trigger_explosion(
                            enemy.rect.x, enemy.rect.y, 40, 40
                        )
                        kills += 1
                    break
        return kills

    def check_player_vs_enemies(
        self,
        player: Player,
        enemy_groups: list[pygame.sprite.Group],
        enemy_level: int,
    ) -> int:
        """Check player collision with enemies.

        Returns:
            Damage taken
        """
        damage = 0
        for enemies in enemy_groups:
            if player.crash(enemies):
                damage += enemy_level
                self._trigger_explosion(player.rect.x, player.rect.y, 50, 50)
        return damage

    def check_player_vs_enemy_weapons(
        self,
        player: Player,
        weapon_groups: list[pygame.sprite.Group],
        enemy_level: int,
    ) -> int:
        """Check player collision with enemy weapons.

        Returns:
            Damage taken
        """
        damage = 0
        for weapons in weapon_groups:
            if player.crash(weapons):
                damage += enemy_level
                self._trigger_explosion(player.rect.x, player.rect.y, 50, 50)
        return damage

    def check_boss_vs_player_weapons(
        self,
        weapons: pygame.sprite.Group,
        power_level: int,
    ) -> int:
        """Check boss collision with player weapons.

        Returns:
            Number of hits on boss
        """
        hits = 0
        for weapon in list(weapons):
            if pygame.sprite.collide_mask(self.boss, weapon):
                weapon.kill()
                self.boss.take_damage(power_level)
                hits += 1

        if hits > 0:
            self._trigger_explosion(
                self.boss.rect.x + 50, self.boss.rect.y + 100, 400, 300
            )
        return hits

    def check_player_vs_items(
        self,
        player: Player,
        items: pygame.sprite.Group,
        item_type: ItemType,
    ) -> int:
        """Check player collision with items.

        Returns:
            Number of items collected
        """
        collected = 0
        if player.crash(items):
            collected = 1
            self._trigger_item_pickup()

            if item_type == ItemType.WEAPON_NUMBER:
                player.state.upgrade_weapon_number()
            elif item_type == ItemType.WEAPON_POWER:
                player.state.upgrade_weapon_power()
            elif item_type == ItemType.WEAPON_SPEED:
                player.state.upgrade_weapon_speed()

        return collected

    def check_player_vs_heal_items(
        self,
        items: pygame.sprite.Group,
    ) -> int:
        """Check both players for heal item collision.

        Returns:
            Heal amount if collected, 0 otherwise
        """
        if self.player1.crash(items) or self.player2.crash(items):
            self._trigger_item_pickup()
            return HEAL_AMOUNT
        return 0

    def remove_collided_sprites(
        self,
        enemy1s: pygame.sprite.Group,
        enemy2s: pygame.sprite.Group,
        enemy1_weapons: pygame.sprite.Group,
        enemy2_weapons: pygame.sprite.Group,
        player1_weapons: pygame.sprite.Group,
        player2_weapons: pygame.sprite.Group,
        item_groups: list[pygame.sprite.Group],
    ) -> None:
        """Remove all collided sprites using pygame's spritecollide."""
        # Players vs enemies
        pygame.sprite.spritecollide(
            self.player1, enemy1s, True, pygame.sprite.collide_mask
        )
        pygame.sprite.spritecollide(
            self.player1, enemy2s, True, pygame.sprite.collide_mask
        )
        pygame.sprite.spritecollide(
            self.player2, enemy1s, True, pygame.sprite.collide_mask
        )
        pygame.sprite.spritecollide(
            self.player2, enemy2s, True, pygame.sprite.collide_mask
        )

        # Players vs enemy weapons
        pygame.sprite.spritecollide(
            self.player1, enemy1_weapons, True, pygame.sprite.collide_mask
        )
        pygame.sprite.spritecollide(
            self.player1, enemy2_weapons, True, pygame.sprite.collide_mask
        )
        pygame.sprite.spritecollide(
            self.player2, enemy1_weapons, True, pygame.sprite.collide_mask
        )
        pygame.sprite.spritecollide(
            self.player2, enemy2_weapons, True, pygame.sprite.collide_mask
        )

        # Boss vs player weapons - handled in check_boss_vs_player_weapons

        # Players vs items
        for items in item_groups:
            pygame.sprite.spritecollide(
                self.player1, items, True, pygame.sprite.collide_mask
            )
            pygame.sprite.spritecollide(
                self.player2, items, True, pygame.sprite.collide_mask
            )
