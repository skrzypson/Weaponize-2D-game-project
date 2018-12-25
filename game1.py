import sys, pygame
import math
import operator
import threading
from random import randint
from typing import Tuple, Set
from pathfinding import a_star
from collections import deque

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
background_image.fill((250,255,170))

#sprite images
user_image = pygame.image.load("x_sprite.png").convert()
user_shot_image = pygame.image.load("shot_v3.png").convert() #_alpha()
elemental_image = pygame.image.load("elem_sprite.png").convert()#_alpha()

#initiate length travelled
mov_increment = 0

#set clock
clock = pygame.time.Clock()

def base_round(*x, base=5):

    if len(x) > 1:
        return tuple(int(base * round(float(_)/base)) for _ in x)
    elif len(x) <= 1:
        return int(base * round(float(*x)/base))

def base_round_floor(*x, base=5):

    if len(x) > 1:
        return tuple(int(base * math.floor(float(_)/base)) for _ in x)
    elif len(x) <= 1:
        return int(base * math.floor(float(*x)/base))

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

    # organizes enemy entity details
    init_sprite_id = 0
    elemental_entity_details_array = dict()
    path_threads_list = []

    mov_rotations = {(5, 5) : 135, (5, 0) : 90, (5, -5) : 45, (0, 5) : 180,
                         (0, -5) : 0, (-5, 5) : 225, (-5, 0) : 270, (-5, -5) : 315}

    def __init__(self, init_coord_x=100, init_coord_y=100, init_color=(100,100,100)):

        pygame.sprite.Sprite.__init__(self)

        # rendering-related data
        #self.image = pygame.Surface((3,3)).convert_alpha()
        self.image_original = elemental_image
        self.image_original.set_colorkey((255,255,255))
        self.image = pygame.transform.rotate(self.image_original, 0) ########!!!!#########
        self.image.set_colorkey((255,255,255))
        #self.image.fill((init_color[0],init_color[1],init_color[2]))

        # spatial data
        self.rect = self.image.get_rect()
        self.rect.centerx = init_coord_x
        self.rect.centery = init_coord_y

        # pathfinding-related objects
        self.sprite_id = ElementalEntities.init_sprite_id
        self.path_generator = a_star.PathGenerator((0, 0), (width, height), self.sprite_id)
        self.path_generator_thread = threading.Thread()
        self.path = iter(())
        self.frames_past = 0

        ElementalEntities.elemental_entity_details_array.update(
            {self.sprite_id : {'path' : (), 'current_location' : (self.rect.centerx, self.rect.centery)}}
        )

        ElementalEntities.init_sprite_id += 1
        all_elementals.add(self)

    def update(self):

        # self.frames_past represents the amount of iterations done over the latest
        # player-targeted path that's been generated for the elemental entity

        next_x = 0
        next_y = 0

        # if the path is being calculated, elemental should be idle (update() does nothing)
        if self.path_generator_thread.isAlive():

            #print('path gen alive')
            return

        # if the path calc is done and frames_past has been reset, build path iterator
        elif self.frames_past == -1 and not self.path_generator_thread.isAlive():

            #print('building path iterator')
            self.path = iter(ElementalEntities.elemental_entity_details_array[self.sprite_id]['path'])
            self.frames_past = 0
            #print('path len: ', len(ElementalEntities.elemental_entity_details_array[self.sprite_id]['path']))

        # check if
        # 1. the player is not near the elemental entity
        # and
        # 2. if the path calculation thread has expired
        # and
        # 3. frames_past has surpassed the path iteration limit and most recent path calc has yielded an empty path
        elif not self.player_in_vicinity() and (self.frames_past > 3*fps-1 or not self.path) \
                and not self.path_generator_thread.isAlive():

            #print(self.sprite_id, 'ladida')
            ElementalEntities.elemental_entity_details_array[self.sprite_id]['path'] = ()
            self.path = iter(())

        # check if
        # 1. player is near elemental entity
        # and
        # 2. path-node iterations have surpassed the defined limit
        # and
        # 3. there is no path calc thread running
        elif self.player_in_vicinity() and (self.frames_past > 3*fps-1 or not self.path) \
                and not self.path_generator_thread.isAlive():

            if self.last_loc_player == User.get_player_location():

                return

            self.path_generator_thread = threading.Thread(target=self.path_generator.aStar
                                                          , name=(str(self.sprite_id) + '_path_gen_thread')
                                                          , args=((self.rect.centerx, self.rect.centery)
                                                                  , (base_round(*User.get_player_location()))
                                                                  , Obstacle.obstacles
                                                                  , True
                                                                  , ElementalEntities.elemental_entity_details_array
                                                                  )
                                                          )
            #print(self.sprite_id, User.get_player_location(), (self.rect.centerx, self.rect.centery))
            self.path_generator_thread.start()

            # reset path-node iteration
            self.frames_past = -1


        elif self.player_in_vicinity() and self.frames_past < 3*fps:

            try:

                next_x, next_y = tuple(map(operator.sub, next(self.path), (self.rect.centerx, self.rect.centery)))
                self.frames_past += 1

            except StopIteration:

                ElementalEntities.elemental_entity_details_array[self.sprite_id]['path'] = ()
                self.path = iter(())
                self.frames_past += fps
                #print('failing')

        else:

            next_x = base_round(ElementalEntities.random_movement_generator())
            next_y = base_round(ElementalEntities.random_movement_generator())
            self.path = iter(())
            self.frames_past += 1

        self.rect.centerx += next_x
        self.rect.centery += next_y

        # if entity randomly walks into obstacle as a result of randomly generated movement, return to previous position
        if (self.rect.centerx, self.rect.centery) in Obstacle.obstacles:

            self.rect.centerx -= next_x
            self.rect.centery -= next_y

        self.check_bounds()

        if (next_x, next_y) != (0,0):

            self.rot_center(- ElementalEntities.mov_rotations[(next_x, next_y)])

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

        if self.rect.centerx > width-5:
            self.rect.centerx = width-5
        if self.rect.centerx < 5:
            self.rect.centerx = 5
        if self.rect.centery > height-5:
            self.rect.centery = height-5
        if self.rect.centery < 5:
            self.rect.centeryk = 5

    @staticmethod
    def random_movement_generator():
        return randint(-5, 5)

    def rot_center(self, angle):
        """rotate an image while keeping its center"""
        self.image = pygame.transform.rotate(self.image_original, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

class UserShot(pygame.sprite.Sprite):

    def __init__(self, user_centerx_coordinate, user_centery_coordinate, user_angle, shot_speed_value):

        pygame.sprite.Sprite.__init__(self)
        self.image_original = user_shot_image
        self.image_original.set_colorkey((255,255,255))
        self.image = pygame.transform.rotate(self.image_original, user_angle)
        #self.image.set_colorkey((255,255,255))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = user_centerx_coordinate + math.cos(math.radians(user_angle))*15
        self.rect.centery = user_centery_coordinate - math.sin(math.radians(user_angle))*15
        self.shot_speed_value = shot_speed_value
        self.speedx = round(self.shot_speed_value * math.cos(math.radians(user_angle))*30, 4)
        self.speedy = - round(self.shot_speed_value * math.sin(math.radians(user_angle))*30, 4)
        all_bullets.add(self)

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy

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
        self.angle = self.prev_angle = 0
        self.mask = pygame.mask.from_surface(self.image)

        User.rect_centerx, User.rect_centery = self.rect.centerx, self.rect.centery
        self.rotate_signal = 0
        #-return to this
        #####self.outline = self.mask.outline()

    def update(self):

        self.speedx = 0
        self.speedy = 0
        self.prev_rect_x = self.rect.x
        self.prev_rect_y = self.rect.y

        pressed_keystate = pygame.key.get_pressed()
        keyup_keystate = pygame.KEYUP
        keydown_keystate = pygame.KEYDOWN

        if pressed_keystate[pygame.K_a]:
            self.speedx = -10

        if pressed_keystate[pygame.K_d]:
            self.speedx = 10

        if pressed_keystate[pygame.K_s]:
            self.speedy = 10

        if pressed_keystate[pygame.K_w]:
            self.speedy = -10

        if event.type == keydown_keystate:
            if event.key == pygame.K_k:
                self.shot_initialize_time = pygame.time.get_ticks()
                empty_event = pygame.event.Event(pygame.USEREVENT)
                pygame.event.post(empty_event)

            if event.key == pygame.K_j and self.rotate_signal==-1:
                self.prev_angle = self.angle
                self.angle = (self.angle + 30) % 360
                self.rot_center(self.angle)

                self.rotate_signal = 0
                self.mask = pygame.mask.from_surface(self.image)
                self.outline = self.mask.outline()
                self.adjusted_outline = {tuple(map(operator.add, node, self.rect.topleft)) for node in self.outline}

                if self.adjusted_outline & Obstacle.obstacles:

                    print('yus')
                    self.angle = self.prev_angle
                    self.rot_center(self.angle)

                self.rotate_signal = 0
                self.mask = pygame.mask.from_surface(self.image)
                self.outline = self.mask.outline()
                self.adjusted_outline = {tuple(map(operator.add, node, self.rect.topleft)) for node in self.outline}

            if event.key == pygame.K_l and self.rotate_signal==1:
                self.prev_angle = self.angle
                self.angle = (self.angle - 30) % 360
                self.rot_center(self.angle)

                self.rotate_signal = 0
                self.mask = pygame.mask.from_surface(self.image)
                self.outline = self.mask.outline()
                self.adjusted_outline = {tuple(map(operator.add, node, self.rect.topleft)) for node in self.outline}

                if self.adjusted_outline & Obstacle.obstacles:
                    print('yus')
                    self.angle = self.prev_angle
                    self.rot_center(self.angle)#-self.prev_angle)

                self.rotate_signal = 0
                self.mask = pygame.mask.from_surface(self.image)
                self.outline = self.mask.outline()
                self.adjusted_outline = {tuple(map(operator.add, node, self.rect.topleft)) for node in self.outline}

        if event.type == keyup_keystate:
            if event.key == pygame.K_k:
                time_delta = round(0.5 + pygame.time.get_ticks()/1000 - self.shot_initialize_time/1000, 4)
                self.shot_speed_value = min(time_delta, 3)
                UserShot(self.rect.centerx, self.rect.centery, self.angle, self.shot_speed_value)
                empty_event = pygame.event.Event(pygame.USEREVENT)
                pygame.event.post(empty_event)

            if event.key == pygame.K_l:
                self.rotate_signal = 1
            if event.key == pygame.K_j:
                self.rotate_signal = -1

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rect.centerx = base_round_floor(self.rect.centerx)
        self.rect.centery = base_round_floor(self.rect.centery)

        self.mask = pygame.mask.from_surface(self.image)
        self.outline = self.mask.outline()
        self.adjusted_outline = {tuple(map(operator.add, node, self.rect.topleft)) for node in self.outline}

        if self.rect.right > width:
            self.rect.right = width
            self.rect.centerx = base_round_floor(self.rect.centerx)

        if self.rect.left < 0:
            self.rect.left = 0
            self.rect.centerx = base_round(self.rect.centerx)
            if self.rect.centerx % 5 == 0 and not self.rect.centerx % 10 == 0:
                self.rect.centerx +=5

        if self.rect.bottom > height:
            self.rect.bottom = height
            self.rect.centery = base_round_floor(self.rect.centery)
            if self.rect.centery % 5 == 0 and not self.rect.centery % 10 == 0:
                self.rect.centery -= 5

        if self.rect.top < 0:
            self.rect.top = 0
            self.rect.centery = base_round((self.rect.bottom-self.rect.top)/2)
            if self.rect.centery % 5 == 0 and not self.rect.centery % 10 == 0:
                self.rect.centery += 5

        if self.adjusted_outline & Obstacle.obstacles:

            self.rect.x -= self.speedx
            self.rect.y -= self.speedy

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

class UserCoordsText():

    def __init__(self):

        self.myfont = pygame.font.Font(None, 15)
        self.label = self.myfont.render(str(User.get_player_location()), 1, (0,0,0))

    def update(self):

        self.label = self.myfont.render(str(User.get_player_location()), 1, (0,0,0))


all_sprites = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
all_elementals = pygame.sprite.Group()
all_wall_sprites = pygame.sprite.Group()

user1 = User()
userCoordsDisplay = UserCoordsText()

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
    userCoordsDisplay.update()
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
    screen.blit(userCoordsDisplay.label, [940,480])
    all_wall_sprites.draw(screen)
    all_bullets.draw(screen)
    all_sprites.draw(screen)
    all_elementals.draw(screen)

    pygame.display.flip()
