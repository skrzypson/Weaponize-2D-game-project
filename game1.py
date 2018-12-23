import sys, pygame
import math
import operator
import threading
from random import randint
from typing import Tuple, Set
from pathfinding import a_star
from collections import deque

# import os
# import psutil



#unchangeable dimensions of window
size = width, height = 1000, 500
fps = 30

#initiate screen
pygame.init()

#set display
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Weaponize")

#set background
#background_image = pygame.image.load("img.png").convert()
background_image = pygame.Surface((width, height))
background_image.fill((255,255,255))

#sprite images
user_image = pygame.image.load("user2.png").convert()
user_shot_image = pygame.image.load("shot.png").convert_alpha()

#initiate length travelled
mov_increment = 0

#set clock
clock = pygame.time.Clock()

def round_base_5(x, base=5):
    return int(base * round(float(x)/base))

class Obstacle(pygame.sprite.Sprite):

    obstacles = set()

    def __init__(self, top_left_corner: Tuple[int,int], bottom_right_corner: Tuple[int,int]):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((abs(top_left_corner[0] - bottom_right_corner[0])
                                     , abs(top_left_corner[1] - bottom_right_corner[1]))).convert_alpha()

        self.image.fill((50,200,50))
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left_corner

        self.inner_outline = set()
        for _ in range(1,5):

            self.temp_surf = pygame.Surface((abs(top_left_corner[0] - bottom_right_corner[0]) - 2*_
                                     , abs(top_left_corner[1] - bottom_right_corner[1]) - 2*_)).convert_alpha()

            self.temp_mask = pygame.mask.from_surface(self.temp_surf)
            self.temp_outline = self.temp_mask.outline()
            self.temp_adjusted_outline = {tuple(map(operator.add, node, self.rect.topleft)) for node in self.temp_outline}
            self.inner_outline.update(self.temp_adjusted_outline)

        del self.temp_surf, self.temp_outline, self.temp_mask, self.temp_adjusted_outline

        self.mask = pygame.mask.from_surface(self.image)
        self.outline = self.mask.outline()
        self.adjusted_outline = {tuple(map(operator.add, node, self.rect.topleft))
                                 for node in self.outline}.union(self.inner_outline)
        del self.inner_outline

        Obstacle.obstacles.update(self.adjusted_outline)
        print(Obstacle.obstacles, len(Obstacle.obstacles))
        all_wall_sprites.add(self)


class ElementalEntities(pygame.sprite.Sprite):

    sprite_id = 0
    elemental_entity_details_array = dict()
    path_threads_list = []

    def __init__(self, init_coord_x=100, init_coord_y=100, init_color=(100,100,100)):

        pygame.sprite.Sprite.__init__(self)

        self.sprite_id = ElementalEntities.sprite_id
        self.path_generator = a_star.PathGenerator((0, 0), (width, height), self.sprite_id)
        self.path = ()
        self.frames_past = 0

        self.image = pygame.Surface((3,3)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = init_coord_x
        self.rect.centery = init_coord_y
        #self.current_user_location = User.get_player_location()
        self.image.fill((init_color[0],init_color[1],init_color[2]))

        self.path_generator_thread = threading.Thread()

        ElementalEntities.elemental_entity_details_array.update(
            {self.sprite_id : {'path' : iter(()), 'current_location' : (self.rect.centerx, self.rect.centery)}}
        )

        ElementalEntities.sprite_id += 1
        all_elementals.add(self)
        self.last_loc_player = User.get_player_location()
        self.current_loc_player = self.last_loc_player

    def update(self):

        self.current_loc_player = User.get_player_location()

        next_x = 0
        next_y = 0

        # if the path is being calculated, do nothing
        if self.path_generator_thread.isAlive():

            #print('doing nothing lalala')
            return

        # if the path calc thread has started and is done
        elif self.frames_past == -1 and not self.path_generator_thread.isAlive():

            self.path = iter(ElementalEntities.elemental_entity_details_array[self.sprite_id]['path'])
            #print('new path created')
            self.frames_past = 0

        # the player is not near and the path calc is done and has yielded an empty path, and 3*fps has past
        elif not self.player_in_vicinity() and (self.frames_past > 3*fps-1 or not self.path) \
                and not self.path_generator_thread.isAlive():

            #kkprint('no calc :(')
            ElementalEntities.elemental_entity_details_array[self.sprite_id]['path'] = ()
            self.path = iter(())

        elif self.player_in_vicinity() and (self.frames_past > 3*fps-1 or not self.path) \
                and not self.path_generator_thread.isAlive():

            #print('calcs...')
            self.path_generator_thread = threading.Thread(target=self.path_generator.aStar
                                                          , name=(str(self.sprite_id) + '_path_gen_thread')
                                                          , args=((self.rect.centerx, self.rect.centery)
                                                                  , (round_base_5(User.get_player_location()[0]),
                                                                  round_base_5(User.get_player_location()[1]))
                                                                  , Obstacle.obstacles
                                                                  , True
                                                                  , ElementalEntities.elemental_entity_details_array
                                                                  )
                                                          )
            print(User.get_player_location(), (self.rect.centerx, self.rect.centery))
            self.path_generator_thread.start()
            self.frames_past = -1
            #print('calc path')
            # print('sprite ' + str(self.sprite_id) + ' is alive - ' + str(self.path_generator_thread.isAlive()))

        elif self.player_in_vicinity() and self.frames_past < 3*fps:

            #print('frames past lol')
            try:

                next_x, next_y = tuple(map(operator.sub, next(self.path), (self.rect.centerx, self.rect.centery)))
                #print('move')
                self.frames_past += 1

            except StopIteration:

                #print('no move')
                ElementalEntities.elemental_entity_details_array[self.sprite_id]['path'] = ()
                self.path = iter(())
                self.frames_past += fps

        else:

            next_x = 0 #ElementalEntities.random_movement_generator()
            next_y = 0 #ElementalEntities.random_movement_generator()
            self.path = iter(()) #iter(())
            self.frames_past += 1
            #print('nothing')

        self.rect.centerx += next_x
        self.rect.centery += next_y

        self.check_bounds()

        ElementalEntities.elemental_entity_details_array[self.sprite_id]['current_location'] = (self.rect.centerx, self.rect.centery)

        self.mask = pygame.mask.from_surface(self.image)

        self.last_loc_player = User.get_player_location()

    def player_in_vicinity(self) -> bool:

        if ElementalEntities.distBetween((self.rect.centerx, self.rect.centery), User.get_player_location()) < 200:

            return True

        return False

    @staticmethod
    def distBetween(_from: Tuple[int, int], _to: Tuple[int, int]) -> float:

        _dx = abs(_to[1] - _from[1])
        _dy = abs(_to[0] - _from[0])
        _dist = round(math.sqrt(_dx ** 2 + _dy ** 2), 2)

        return _dist

    def check_bounds(self):

        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0

    @staticmethod
    def random_movement_generator():
        return randint(-1, 1)

class UserShot(pygame.sprite.Sprite):

    def __init__(self, user_centerx_coordinate, user_centery_coordinate, user_angle, shot_speed_value):

        pygame.sprite.Sprite.__init__(self)
        self.image_original = user_shot_image
        self.image_original.set_colorkey((255,255,255))
        self.image = pygame.transform.rotate(self.image_original, user_angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = user_centerx_coordinate + math.cos(math.radians(user_angle))*30
        self.rect.centery = user_centery_coordinate - math.sin(math.radians(user_angle))*30
        self.shot_speed_value = shot_speed_value
        self.speedx = round(self.shot_speed_value * math.cos(math.radians(user_angle))*30, 4)
        self.speedy = - round(self.shot_speed_value * math.sin(math.radians(user_angle))*30, 4)
        all_bullets.add(self)

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #print("shot x,y: " + str(self.rect.centerx) + "," + str(self.rect.centery))

        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.centerx > width or self.rect.centerx < 0 or self.rect.centery > height or self.rect.centery < 0:
            #print("shot x,y: " + str(self.rect.centerx) + "," + str(self.rect.centery))
            all_bullets.remove(self)
            self = None
            print("shot is dead")

class User(pygame.sprite.Sprite):

    rect_centerx, rect_centery = None, None

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image_original = user_image
        self.image_original.set_colorkey((255, 255, 255))
        self.image = self.image_original.copy()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 30
        self.speedx = 0
        self.speedy = 0
        self.angle = 0
        self.mask = pygame.mask.from_surface(self.image)

        User.rect_centerx, User.rect_centery = self.rect.centerx, self.rect.centery

        #-return to this
        #####self.outline = self.mask.outline()

    def update(self):

        self.speedx = 0
        self.speedy = 0

        pressed_keystate = pygame.key.get_pressed()
        keyup_keystate = pygame.KEYUP
        keydown_keystate = pygame.KEYDOWN

        if pressed_keystate[pygame.K_a]:

            self.speedx = -10
            #print("a pressed, x = " + str(self.rect.x))

        if pressed_keystate[pygame.K_d]:
            #print("d pressed, x = " + str(self.rect.x))
            self.speedx = 10

        if pressed_keystate[pygame.K_s]:

            self.speedy = 10
            #print("w pressed, y = " + str(self.rect.y))

        if pressed_keystate[pygame.K_w]:
            #print("s pressed, y = " + str(self.rect.y))
            self.speedy = -10

        if pressed_keystate[pygame.K_j]:

            self.angle = (self.angle + 5) % 360
            self.rot_center(self.angle)
            #print("q pressed, angle = " + str(self.angle))

        if pressed_keystate[pygame.K_l]:

            self.angle = (self.angle - 5) % 360
            self.rot_center(self.angle)
            #print("q pressed, angle = " + str(self.angle))

        if event.type == keydown_keystate:
            if event.key == pygame.K_k:
                self.shot_initialize_time = pygame.time.get_ticks()
                empty_event = pygame.event.Event(pygame.USEREVENT)
                pygame.event.post(empty_event)
                #print("init time: " + str(self.shot_initialize_time))

        if event.type == keyup_keystate:
            if event.key == pygame.K_k:
                time_delta = round(0.5 + pygame.time.get_ticks()/1000 - self.shot_initialize_time/1000, 4)
                self.shot_speed_value = min(time_delta, 3)
                #print("get ticks: " + str(pygame.time.get_ticks()/1000) + ", init time:  " + str(self.shot_initialize_time/1000))
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

        self.rect.centerx, self.rect.centery = round_base_5(self.rect.centerx), round_base_5(self.rect.centery)

        User.rect_centerx, User.rect_centery = self.rect.centerx, self.rect.centery

        # -return to this
        #### print(self.outline)

    def rot_center(self, angle):
        """rotate an image while keeping its center"""
        self.image = pygame.transform.rotate(self.image_original, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        # -return to this
        ####self.mask = pygame.mask.from_surface(self.image)

    @staticmethod
    def get_player_location() -> Tuple[int, int]:

        return User.rect_centerx, User.rect_centery

all_sprites = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
all_elementals = pygame.sprite.Group()
all_wall_sprites = pygame.sprite.Group()

user1 = User()

e_x, e_y = 150, 100
el1 = ElementalEntities(e_x, e_y+10,(25,125,225))
el3 = ElementalEntities(e_x, e_y+20,(25,125,225))
el4 = ElementalEntities(e_x, e_y+30,(25,125,225))
el5 = ElementalEntities(e_x, e_y+40,(25,125,225))
el6 = ElementalEntities(e_x, e_y+50,(25,125,225))
el7 = ElementalEntities(e_x, e_y+60,(25,125,225))
el8 = ElementalEntities(e_x, e_y+70,(25,125,225))
el9 = ElementalEntities(e_x, e_y+80,(25,125,225))
el10 = ElementalEntities(e_x, e_y+90,(25,125,225))
el11 = ElementalEntities(e_x, e_y+100,(25,125,225))
el12 = ElementalEntities(e_x, e_y+110,(25,125,225))
el13 = ElementalEntities(e_x, e_y+120,(25,125,225))
el14 = ElementalEntities(e_x, e_y+130,(25,125,225))
el15 = ElementalEntities(e_x+100, e_y+140,(25,125,225))
el16 = ElementalEntities(e_x+100, e_y+150,(25,125,225))
el17 = ElementalEntities(e_x+100, e_y+160,(25,125,225))
el18 = ElementalEntities(e_x+100, e_y+170,(25,125,225))
el19 = ElementalEntities(e_x+100, e_y+180,(25,125,225))
el20 = ElementalEntities(e_x+100, e_y+190,(25,125,225))

all_sprites.add(user1)#, el1, el2)


wall1 = Obstacle((350, 350), (370, 370))
wall2 = Obstacle((200, 300), (250, 350))
wall3 = Obstacle((600, 100), (620, 250))


while True:

    clock.tick(fps)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update()
    all_bullets.update()
    all_elementals.update()
    #print(ElementalEntities.elemental_entity_details_array)

    # pid = os.getpid()
    # py = psutil.Process(pid)
    # memoryUse = py.memory_info()[0]/2.**30  # memory use in GB...I think
    # print('memory use:', memoryUse)

    hits = pygame.sprite.groupcollide(all_elementals, all_bullets, True, False, pygame.sprite.collide_mask)
    #if pygame.sprite.spritecollide(user1, all_elementals, False, pygame.sprite.collide_mask):
    #    print("fudge")
    # if hits == True:
    #     print("BAM")

    screen.blit(background_image, [0,0])
    all_wall_sprites.draw(screen)
    all_sprites.draw(screen)
    all_bullets.draw(screen)
    all_elementals.draw(screen)

    pygame.display.flip()
