"""
Constants used throughout the robot simulation.
"""

FRAME_RATE: float = 1 / 60
LINEAR_SPEED_RATIO: float = 3.0
ANGULAR_SPEED_RATIO: float = 0.6

RESOLUTION_LIDAR_SENSOR: int = 181
MAX_RANGE_LIDAR_SENSOR: int = 300
FOV_LIDAR_SENSOR: int = 360

# 'WINDOW_AUTO_RESIZE_RATIO' is the percentage of screen size used as maximum
# for automatic window resizing (0.85 = 85% of screen size)
WINDOW_AUTO_RESIZE_RATIO: float = 0.85

# 'ENABLE_WINDOW_AUTO_RESIZE' allows to completely disable automatic window resizing
# Set to False to disable auto-resize for all windows
ENABLE_WINDOW_AUTO_RESIZE: bool = True

