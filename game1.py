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
        self.rect.centerx = user_centerx_coordinate + math.cos(math.radians(user_angle))*30
        self.rect.centery = user_centery_coordinate - math.sin(math.radians(user_angle))*30
        print(math.cos(user_angle))
        print(math.sin(user_angle))
        self.shot_speed_value = shot_speed_value
        self.speedx = self.shot_speed_value * math.cos(math.radians(user_angle))*30
        self.speedy = -(self.shot_speed_value * math.sin(math.radians(user_angle)))*30
        all_sprites.add(self)
        print("shot x,y: " + str(self.rect.centerx) + "," + str(self.rect.centery))
        print("speedx = " + str(self.speedx) + ", speedy = " + str(self.speedy) + ", angle = " + str(user_angle))

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

    def update(self):

        self.speedx = 0
        self.speedy = 0

        pressed_keystate = pygame.key.get_pressed()
        keyup_keystate = pygame.KEYUP
        keydown_keystate = pygame.KEYDOWN

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

        if event.type == keydown_keystate:
            if event.key == pygame.K_KP5:
                self.shot_initialize_time = pygame.time.get_ticks()
                empty_event = pygame.event.Event(pygame.USEREVENT)
                pygame.event.post(empty_event)
                print("init time: " + str(self.shot_initialize_time))

        if event.type == keyup_keystate:
            if event.key == pygame.K_KP5:
                time_delta = 0.5 + pygame.time.get_ticks()/1000 - self.shot_initialize_time/1000
                self.shot_speed_value = min(time_delta, 3)
                print("get ticks: " + str(pygame.time.get_ticks()/1000) + ", init time:  " + str(self.shot_initialize_time/1000))
                UserShot(self.rect.centerx, self.rect.centery, self.angle, self.shot_speed_value)
                empty_event = pygame.event.Event(pygame.USEREVENT)
                pygame.event.post(empty_event)
                print("speed: " + str(self.shot_speed_value))


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

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update()
    screen.blit(background_image, [0,0])
    all_sprites.draw(screen)

    pygame.display.flip()