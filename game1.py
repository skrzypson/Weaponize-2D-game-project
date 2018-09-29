import sys, pygame
import math

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

#sprite images
user_image = pygame.image.load("user.png").convert()
user_shot_image = pygame.image.load("shot.png").convert()

#initiate length travelled
mov_increment = 0

#set clock
clock = pygame.time.Clock()


class UserShot(pygame.sprite.Sprite):

    def __init__(self, user_centerx_coordinate, user_centery_coordinate, user_angle, shot_speed_value):

        pygame.sprite.Sprite.__init__(self)
        self.image_original = user_shot_image
        self.image_original.set_colorkey((255,255,255))
        self.image = pygame.transform.rotate(self.image_original, user_angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = user_centerx_coordinate + math.cos(user_angle)*30
        self.rect.centery = user_centery_coordinate + math.sin(user_angle)*30
        self.shot_speed_value = shot_speed_value
        self.speedx = self.shot_speed_value * math.cos(user_angle)
        self.speedy = self.shot_speed_value * math.sin(user_angle)
        all_sprites.add(self)
        #print("shot x,y: " + str(self.rect.centerx) + "," + str(self.rect.centery))
        print("speedx = " + str(self.speedx) + ", speedy = " + str(self.speedy))

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #print("shot x,y: " + str(self.rect.centerx) + "," + str(self.rect.centery))

        if self.rect.centerx > width or self.rect.centerx < 0 or self.rect.centery > height or self.rect.centery < 0:
            #print("shot x,y: " + str(self.rect.centerx) + "," + str(self.rect.centery))
            all_sprites.remove(self)
            self = None
            print("shot is dead")

class User(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image_original = user_image
        self.image_original.set_colorkey((255, 255, 255))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 30
        self.speedx = 0
        self.speedy = 0
        self.angle = 0

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

        pressed_keystate = pygame.key.get_pressed()
        released_keystate = pygame.KEYUP

        if pressed_keystate[pygame.K_a]:

            self.speedx = -8
            print("a pressed, x = " + str(self.rect.x))

        if pressed_keystate[pygame.K_d]:
            print("d pressed, x = " + str(self.rect.x))
            self.speedx = 8

        if pressed_keystate[pygame.K_s]:

            self.speedy = 8
            print("w pressed, y = " + str(self.rect.y))

        if pressed_keystate[pygame.K_w]:
            print("s pressed, y = " + str(self.rect.y))
            self.speedy = -8

        if pressed_keystate[pygame.K_KP4]:

            self.angle = (self.angle + 5) % 360
            self.rot_center(self.angle)
            print("q pressed, angle = " + str(self.angle))

        if pressed_keystate[pygame.K_KP6]:

            self.angle = (self.angle - 5) % 360
            self.rot_center(self.angle)
            print("q pressed, angle = " + str(self.angle))

        if pressed_keystate[pygame.K_KP5]:
            self.shot_initialize_time = pygame.time.get_ticks()

        if event.type == released_keystate:
            if event.key == pygame.K_KP5:
                self.shot_speed_value = min((pygame.time.get_ticks() - self.shot_initialize_time)/5, 15)
                UserShot(self.rect.centerx, self.rect.centery, self.angle, self.shot_speed_value)
                empty_event = pygame.event.Event(pygame.USEREVENT)
                pygame.event.post(empty_event)
                #print("speed: " + str(self.shot_speed_value))


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

    def rot_center(self, angle):
        """rotate an image while keeping its center"""
        self.image = pygame.transform.rotate(self.image_original, angle)
        self.rect = self.image.get_rect(center=self.rect.center)





all_sprites = pygame.sprite.Group()
user1 = User()
all_sprites.add(user1)

while True:

    clock.tick(fps)

    for event in pygame.event.get():

        print(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update()
    screen.blit(background_image, [0,0])
    all_sprites.draw(screen)

    pygame.display.flip()