import sys, pygame

#unchangeable dimensions of window
size = width, height = 1000, 500
fps = 30

#initiate screen
pygame.init()

#set display
screen = pygame.display.set_mode(size)

#set background
background_image = pygame.image.load("img.png").convert()

#set clock
clock = pygame.time.Clock()

img = pygame.image.load("x_sprite.png").convert_alpha()

class x_sprite(pygame.sprite.Sprite):

    def __init__(self, delta_x, init_coord_x=100, init_coord_y=100, init_color=(100,100,100)):

        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = init_coord_x
        self.rect.centery = init_coord_y
        self.mask = pygame.mask.from_surface(self.image)
        self.delta_x = delta_x

    def update(self):

        self.rect.centerx += self.delta_x
        self.rect.centery += 0

right_going_sprites = pygame.sprite.Group()
left_going_sprites = pygame.sprite.Group()

r1 = x_sprite(1, 100, 100)
r2 = x_sprite(1, 100, 200)
r3 = x_sprite(1, 100, 300)

l1 = x_sprite(-1, 200, 100)
l2 = x_sprite(-1, 200, 200)
l3 = x_sprite(-1, 200, 300)

right_going_sprites.add(r1, r2, r3)
left_going_sprites.add(l1, l2, l3)

print(right_going_sprites)
print(left_going_sprites)

while True:

    clock.tick(fps)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    right_going_sprites.update()
    left_going_sprites.update()

    print(pygame.sprite.groupcollide(right_going_sprites, left_going_sprites, True, True, collided=pygame.sprite.collide_mask))

    pygame.sprite.groupcollide(right_going_sprites, left_going_sprites, True, True, collided=pygame.sprite.collide_mask)

    screen.blit(background_image, [0, 0])

    right_going_sprites.draw(screen)
    left_going_sprites.draw(screen)

    pygame.display.flip()