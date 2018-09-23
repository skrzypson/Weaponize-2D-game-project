import sys, pygame

#unchangeable dimensions of window
size = width, height = 1000, 500

#set frames per second
fps = 30

#initiate screen
pygame.init()

#set display
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Weaponize")

#set background
background_image = pygame.image.load("img.png").convert()
user_image = pygame.image.load("user.png").convert()

#initiate length travelled
mov_increment = 0

#set clock
clock = pygame.time.Clock()

class User(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = user_image
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        #self.rect.center = (self.image.get_size()[0], self.image.get_size()[1])
        self.rect.centerx = width / 2
        self.rect.bottom = height - 30
        self.speedx = 0
        self.speedy = 0

        # pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50, 40))
        # self.image.fill((30,30,30))
        # self.rect = self.image.get_rect()
        # self.rect.centerx = width / 2
        # self.rect.bottom = height - 10
        # self.speedx = 0

    def update(self):

        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_a]:

            self.speedx = -8
            print("a pressed, x = " + str(self.rect.x))

        if keystate[pygame.K_d]:
            print("d pressed, x = " + str(self.rect.x))
            self.speedx = 8

        if keystate[pygame.K_s]:

            self.speedy = 8
            print("w pressed, y = " + str(self.rect.y))

        if keystate[pygame.K_w]:
            print("s pressed, y = " + str(self.rect.y))
            self.speedy = -8

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0

all_sprites = pygame.sprite.Group()
user1 = User()
all_sprites.add(user1)

while True:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update()
    screen.blit(background_image, [0,0])
    all_sprites.draw(screen)

    pygame.display.flip()