import sys, pygame
import numpy

#initiate screen
pygame.init()

#unchangeable dimensions of window
size = width, height = 500, 500

#set display
screen = pygame.display.set_mode(size)

#background settings
black = 0, 0, 0
background = (pygame.Surface(screen.get_size())).convert()
background.fill(black)

random_matrix = numpy.random.rand(2,3)
print(random_matrix)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
