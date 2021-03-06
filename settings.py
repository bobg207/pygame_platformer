# create color constants
WHITE = (255, 255, 255)
RED = (87, 9, 9)
GREEN = (12, 148, 37)
BLUE = (2, 0, 94)
BLACK = (0, 0, 0)

# width by height
FPS = 60

# Game Layout
LAYOUT = ['11111111111111111111',
          '10000000000000000001',
          '10000000000000000001',
          '10000000000000000001',
          '10000000000000000001',
          '10000000000000000000',
          '10000000000000000000',
          '10000022000022000001',
          '10000000000000000000',
          '11111111111111111111', ]

WALL_BRICK_WIDTH = 50
WALL_BRICK_HEIGHT = 50

DISPLAY_WIDTH = len(LAYOUT[0]) * WALL_BRICK_WIDTH
DISPLAY_HEIGHT = len(LAYOUT) * WALL_BRICK_HEIGHT

# Player
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
