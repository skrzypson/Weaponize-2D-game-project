from logic.game_logic import pygame
import warnings

# pygame = game_logic.pygame

# ignore these for now but fix later
warnings.filterwarnings("ignore", category=DeprecationWarning)

obstacle_set = set()

# unchangeable dimensions of window
size = width, height = 1000, 500
fps = 60

# initiate screen
# pygame.init()

# set display
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Weaponize")
