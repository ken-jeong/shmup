"""Math utility functions."""

import math


def calculate_angle(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate angle between two points for rotation.

    Args:
        x1, y1: Source position
        x2, y2: Target position

    Returns:
        Angle in degrees for pygame rotation
    """
    y = y1 - y2
    x = x1 - x2
    angle = math.atan2(y, x)
    angle = angle * (180 / math.pi)
    angle = -(angle + 90) % 360
    return angle


def calculate_direction(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate direction angle (radians) from point 1 to point 2.

    Args:
        x1, y1: Source position
        x2, y2: Target position

    Returns:
        Angle in radians
    """
    return math.atan2(y2 - y1, x2 - x1)
