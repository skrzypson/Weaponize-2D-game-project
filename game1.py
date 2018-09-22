import sys, pygame

#initiate screen
pygame.init()

#unchangeable dimensions of window
size = width, height = 1000, 1000

#set display
screen = pygame.display.set_mode(size)

#background settings
#black = 0, 0, 0
#background = (pygame.Surface(screen.get_size())).convert()
#background.fill(black)

background_image = pygame.image.load("img.png").convert()
user_image = pygame.image.load("user.png").convert()
mov_increment = 0

class User(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = user_image
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.image.get_size()[0], self.image.get_size()[1])
        self.rect.x = 0
        self.rect.y = 0

    def update(self):

        self.rect.x += mov_increment

all_sprites = pygame.sprite.Group()
user1 = User()
all_sprites.add(user1)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update()
    all_sprites.draw(screen)

    screen.blit(background_image, [0,0])

    mov_increment = (pygame.time.get_ticks()/100)
    print(mov_increment)

    screen.blit(user_image, [mov_increment, mov_increment])
    pygame.display.flip()