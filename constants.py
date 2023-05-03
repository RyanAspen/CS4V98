"""

This file contains all of the constants required for any given
execution of main.py. 

"""

# Map/Environment file used to generate simulation
MAP_NAME = "many_cameras.txt"

# Multiplicative constants used for handshake matching
POS_CONST = 0.1
APPEARANCE_CONST = 1.0
SIZE_CONST = 4.0

# Defines the size of the simulation visual. For example, SCALE = 5 means that each square tile
# in the environment is represented as a 5x5 group of pixels.
SCALE = 6

# If set to false, the simulation pauses after each frame, requiring the user to press any button to continue to the next frame.
AUTOPLAY = False

# If AUTOPLAY is set to True, the simulation will be limited to the given frame rate
FPS = 10