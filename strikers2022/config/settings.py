"""Game settings and constants."""

# Window settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (250, 250, 50)
RED = (250, 50, 50)

# Player settings
PLAYER_HP = 1000  # Default: 300
PLAYER_SIZE = (50, 80)
PLAYER_SPEED = 5

# Attack settings
ATTACK_COOLDOWN_BASE = 26
ATTACK_SPEED_MULTIPLIER = 3

# Weapon level limits
MAX_WEAPON_SPEED_LEVEL = 5
MAX_WEAPON_POWER_LEVEL = 5
MAX_WEAPON_NUMBER_LEVEL = 4

# Enemy settings
ENEMY_ATTACK_INTERVAL = 100
ENEMY_SIZE = (50, 50)
ENEMY_SPAWN_PROBABILITY = 250  # Higher = fewer enemies (1 in N chance per frame)

# Item spawn settings
ITEM_SPAWN_INTERVAL = 300  # Frames between automatic item spawns (5 seconds at 60 FPS)

# Boss settings
BOSS_DEFAULT_HP = 5000
BOSS_SIZE = (500, 350)

# Item settings
ITEM_SIZE = (40, 40)
ITEM_SPEED = 1
HEAL_AMOUNT = 20

# Item spawn thresholds (boss HP values)
ITEM_SPAWN_THRESHOLDS = [
    4950, 4900, 4850, 4750, 4650, 4550,
    4350, 4050, 3750, 3350, 2950, 2450,
    1950, 1450, 950
]

# Weapon settings
PLAYER_WEAPON_SIZE = (10, 40)
PLAYER_WEAPON_SPEED = 15
ENEMY_WEAPON_SIZE = (10, 40)
ENEMY_WEAPON_SPEED = 5
