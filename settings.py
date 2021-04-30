# Game options/settings.
TITLE = "PlatFrogs"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = "arial"
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet.png"

# Player movement properties.
PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 1
PLAYER_JUMP = 20

# Define platforms.
PLATFORM_LIST = [(0, HEIGHT - 40),
                 (WIDTH / 2 - 50, HEIGHT * 3/4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

# Define colors.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (112, 181, 80)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (102, 222, 200)
LIGHTGREEN = (188, 242, 170)
BGCOLOUR = LIGHTBLUE
