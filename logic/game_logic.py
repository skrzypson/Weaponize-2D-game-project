import warnings
import sys, pygame, pygame.mixer
import math
import operator
import threading
import random
from random import randint, uniform
from typing import Tuple
from pathfinding import a_star
from objects.world_objects import Tree, Obstacle
# from sound_logic import speed_change

# input(pygame.__name__)

obstacle_set = set()

# ignore these for now but fix later
warnings.filterwarnings("ignore", category=DeprecationWarning)

# unchangeable dimensions of window
size = width, height = 1000, 500
fps = 60

# initiate screen
pygame.init()

# set display
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Weaponize")

# sound file locations and objects
sounds_loc = {'sound_MachineGunFire':   "../sounds/fastshot.wav",
              'sound_LaserGunfire1':    "../sounds/fastlasershot.wav",
              'sound_LaserGunfire2':    "../sounds/fasterlasershot.wav",
              'sound_LaserGunfire3':    "../sounds/fastererlasershot.wav",
              }
sounds = {sound_name: pygame.mixer.Sound(loc) for sound_name, loc in sounds_loc.items()}

# graphic files - locations
graphics_loc = {"player_sprites":          "../graphics/player_sprites/",
                "player_bullet_sprites":   "../graphics/player_bullet_sprites/",
                "enemy_sprites":           "../graphics/enemy_sprites/",
                "background_images":       "../graphics/background_images/"}

player_sprites_img = dict({0: "p_0", 1: "p_1", 1.1: "p_1.1", 1.2: "p_1.2", 2: "p_2", 2.1: "p_2.1"})
player_bullet_sprites_img = dict({0: "p_s_0", 1: "m_g_fire"})
enemy_sprites_img = dict({0: "el_0", 1: "el_1", 2: "el_2"})
background_img = dict({0: "grass_backgr_8p_grayscale", 1: "grass_backgr_8p_dark"})

# set background
background_image = pygame.image.load(graphics_loc["background_images"] + background_img[1] + ".png").convert()

# sprite images
user_image = pygame.image.load(graphics_loc["player_sprites"]
                               + player_sprites_img[2.1] + ".png").convert()
user_shot_image = pygame.image.load(graphics_loc["player_bullet_sprites"]
                                    + player_bullet_sprites_img[0] + ".png").convert() #_alpha()
machine_gun_fire_image = pygame.image.load(graphics_loc["player_bullet_sprites"]
                                           + player_bullet_sprites_img[1] + ".png").convert()
elemental_image = pygame.image.load(graphics_loc["enemy_sprites"] + enemy_sprites_img[2]
                                    + ".png").convert()#_alpha()

# initiate length travelled
mov_increment = 0

# set clock
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


class ElementalEntities(pygame.sprite.Sprite):

    # organizes enemy entity details
    init_sprite_id = 0
    elemental_entity_details_array = dict()
    path_threads_list = []

    mov_rotations = {(5, 5): 135, (5, 0): 90, (5, -5): 45, (0, 5): 180,
                     (0, -5): 0, (-5, 5): 225, (-5, 0): 270, (-5, -5): 315}

    def __init__(self, init_coord_x=100, init_coord_y=100):

        pygame.sprite.Sprite.__init__(self)

        # rendering-related data
        #self.image = pygame.Surface((3,3)).convert_alpha()
        self.image_original = elemental_image
        self.image_original.set_colorkey((255, 255, 255))
        self.image = pygame.transform.rotate(self.image_original, 0)
        self.image.set_colorkey((255,255,255))

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
            {self.sprite_id: {'path': (), 'current_location': (self.rect.centerx, self.rect.centery)}}
        )

        ElementalEntities.init_sprite_id += 1
        all_elementals.add(self)

    def update(self):

        # self.frames_past represents the amount of iterations done over the latest
        # player-targeted path that's been generated for the elemental entity

        next_x = 0
        next_y = 0

        # if the path is being calculated, elemental should be idle (update() does nothing)
        if self.path_generator_thread.is_alive():

            return

        # if the path calc is done and frames_past has been reset, build path iterator
        elif self.frames_past == -1 and not self.path_generator_thread.is_alive():

            self.path = iter(ElementalEntities.elemental_entity_details_array[self.sprite_id]['path'])
            self.frames_past = 0

        # check if
        # 1. the player is not near the elemental entity
        # and
        # 2. if the path calculation thread has expired
        # and
        # 3. frames_past has surpassed the path iteration limit and most recent path calc has yielded an empty path
        elif not self.player_in_vicinity() and (self.frames_past > 3 * fps-1 or not self.path) \
                and not self.path_generator_thread.is_alive():

            ElementalEntities.elemental_entity_details_array[self.sprite_id]['path'] = ()
            self.path = iter(())

        # check if
        # 1. player is near elemental entity
        # and
        # 2. path-node iterations have surpassed the defined limit
        # and
        # 3. there is no path calc thread running
        elif self.player_in_vicinity() and (self.frames_past > 3 * fps-1 or not self.path) \
                and not self.path_generator_thread.is_alive():

            # if self.last_loc_player == User.get_player_location():
            #
            #     print('nanana')
            #     return

            self.path_generator_thread = threading.Thread(target=self.path_generator.aStar
                                                          , name=(str(self.sprite_id) + '_path_gen_thread')
                                                          , args=((self.rect.centerx, self.rect.centery)
                                                                  , (base_round(*User.get_player_location()))
                                                                  , obstacle_set
                                                                  , True
                                                                  , ElementalEntities.elemental_entity_details_array
                                                                  )
                                                          )

            self.path_generator_thread.start()

            # reset path-node iteration
            self.frames_past = -1

        elif self.player_in_vicinity() and self.frames_past < 3 * fps:

            try:

                next_x, next_y = tuple(map(operator.sub, next(self.path), (self.rect.centerx, self.rect.centery)))
                self.frames_past += 1

            except StopIteration:

                ElementalEntities.elemental_entity_details_array[self.sprite_id]['path'] = ()
                self.path = iter(())
                self.frames_past += fps

        else:

            if self.frames_past % 3 == 0:

                next_x = base_round(ElementalEntities.random_movement_generator())
                next_y = base_round(ElementalEntities.random_movement_generator())

            self.path = iter(())
            self.frames_past += 1

        self.rect.centerx += next_x
        self.rect.centery += next_y

        # if entity randomly walks into obstacle as a result of randomly generated movement, return to previous position
        if (self.rect.centerx, self.rect.centery) in obstacle_set:

            self.rect.centerx -= next_x
            self.rect.centery -= next_y

        self.check_bounds()

        if (next_x, next_y) != (0, 0):

            self.rot_center(- ElementalEntities.mov_rotations[(next_x, next_y)])

        ElementalEntities.elemental_entity_details_array[self.sprite_id]['current_location'] = (self.rect.centerx, self.rect.centery)

        self.mask = pygame.mask.from_surface(self.image)

        self.last_loc_player = User.get_player_location()

    def player_in_vicinity(self) -> bool:

        if ElementalEntities.distBetween((self.rect.centerx, self.rect.centery), User.get_player_location()) < 300:

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
            self.rect.centery = 5

    @staticmethod
    def random_movement_generator():
        return randint(-5, 5)

    def rot_center(self, angle):
        """rotate an image while keeping its center"""
        self.image = pygame.transform.rotate(self.image_original, angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class LaserGunfire(pygame.sprite.Sprite):

    def __init__(self, user_centerx_coordinate, user_centery_coordinate, user_angle, shot_speed_value):

        pygame.sprite.Sprite.__init__(self)
        self.image_original = user_shot_image
        self.image_original.set_colorkey((255, 255, 255))
        self.image = pygame.transform.rotate(self.image_original, user_angle)
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
            all_bullets.remove(self)
            self = None

    # def scatter_shrapnel(self):
    #     ...

    def __del__(self):
        print('del')
        Shrapnel(self)


class Shrapnel(pygame.sprite.Sprite):

    def __init__(self, lgf: LaserGunfire):
        self.updates = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30)).convert()
        self.image.fill((0, 0, 255))
        # self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = lgf.rect.center
        self.var = uniform(0.5, 1.0)
        self.xspeed = lgf.speedx * self.var
        self.yspeed = lgf.speedy * self.var
        all_shrapnel.add(self)

    def update(self):
        self.updates += 1
        self.rect.x = self.rect.x + self.xspeed
        self.rect.y = self.rect.y + self.yspeed
        self.xspeed = self.xspeed * 0.5
        self.yspeed = self.yspeed * 0.5

        if self.updates > 115:
            del self


class MachineGunFire(pygame.sprite.Sprite):

    def __init__(self, user_centerx_coordinate, user_centery_coordinate, user_angle, offset):

        pygame.sprite.Sprite.__init__(self)
        self.image_original = machine_gun_fire_image
        self.image_original.set_colorkey((255,255,255))
        self.image = pygame.transform.rotate(self.image_original, user_angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = user_centerx_coordinate + math.cos(math.radians(user_angle))*1 \
                            - (offset * math.cos(math.radians(90-user_angle)) + randint(0,3))
        self.rect.centery = user_centery_coordinate - math.sin(math.radians(user_angle))*1 \
                            - (offset * math.sin(math.radians(90-user_angle)) + randint(0,3))
        self.shot_speed_value = 1 + random.uniform(0, 1)/10
        self.speedx = round(self.shot_speed_value * math.cos(math.radians(user_angle))*30, 4)
        self.speedy = - round(self.shot_speed_value * math.sin(math.radians(user_angle))*30, 4)
        all_bullets.add(self)

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.centerx > width or self.rect.centerx < 0 or self.rect.centery > height or self.rect.centery < 0:
            all_bullets.remove(self)
            self = None
            # print("shot is dead")


class User(pygame.sprite.Sprite):

    rect_centerx, rect_centery = None, None

    mgf_sound = sounds['sound_MachineGunFire']
    lgf_sound_slow = sounds['sound_LaserGunfire1']
    lgf_sound_fast = sounds['sound_LaserGunfire2']
    lgf_sound_fastest = sounds['sound_LaserGunfire3']

    sound_dict = {1: lgf_sound_slow, 2: lgf_sound_fast, 3: lgf_sound_fastest}
    laser_sound = lambda v: User.sound_dict.get(math.ceil(v), User.lgf_sound_slow)

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
        self.mask = pygame.mask.from_surface(self.image)

        User.angle = self.angle = self.prev_angle = 0
        User.rect_centerx, User.rect_centery = self.rect.centerx, self.rect.centery
        self.rotate_signal = 0
        self.weapon_set = {0: user_shot_image, 1: machine_gun_fire_image}
        self.weapon_chosen = 0
        self.machine_gun_shooting = False

    def update(self):

        self.speedx = 0
        self.speedy = 0
        self.prev_rect_x = self.rect.x
        self.prev_rect_y = self.rect.y

        pressed_keystate = pygame.key.get_pressed()
        keyup_keystate = pygame.KEYUP
        keydown_keystate = pygame.KEYDOWN

        if pressed_keystate[pygame.K_a]:
            self.speedx = -5

        if pressed_keystate[pygame.K_d]:
            self.speedx = 5

        if pressed_keystate[pygame.K_s]:
            self.speedy = 5

        if pressed_keystate[pygame.K_w]:
            self.speedy = -5

        if event.type == keydown_keystate:

            if event.key == pygame.K_SPACE:
                self.machine_gun_shooting = True

            if event.key == pygame.K_k:
                self.shot_initialize_time = pygame.time.get_ticks()
                empty_event = pygame.event.Event(pygame.USEREVENT)
                pygame.event.post(empty_event)

            if event.key == pygame.K_l and self.rotate_signal != 1:
                self.rotate_signal = 1

            if event.key == pygame.K_j and self.rotate_signal != -1:
                self.rotate_signal = -1

        if event.type == keyup_keystate:

            if event.key == pygame.K_SPACE :

                self.machine_gun_shooting = False

            if event.key == pygame.K_k:

                time_delta = round(0.5 + pygame.time.get_ticks()/1000 - self.shot_initialize_time/1000, 4)
                self.shot_speed_value = min(time_delta, 3)
                LaserGunfire(self.rect.centerx, self.rect.centery, self.angle, self.shot_speed_value)
                print(f'self.shot_speed_value: {self.shot_speed_value}')
                User.laser_sound(self.shot_speed_value).play()
                empty_event = pygame.event.Event(pygame.USEREVENT)
                pygame.event.post(empty_event)

            if event.key == pygame.K_j and self.rotate_signal == -1:
                self.prev_angle = self.angle
                self.angle = (self.angle + 30) % 360
                self.rot_center(self.angle)

                self.rotate_signal = 0
                self.get_players_adj_outline()

                if self.adjusted_outline & obstacle_set:

                    self.angle = self.prev_angle
                    self.rot_center(self.angle)
                    self.get_players_adj_outline()

            if event.key == pygame.K_l and self.rotate_signal == 1:
                self.prev_angle = self.angle
                self.angle = (self.angle - 30) % 360
                self.rot_center(self.angle)

                self.rotate_signal = 0
                self.get_players_adj_outline()

                if self.adjusted_outline & obstacle_set:
                    print('yus')
                    self.angle = self.prev_angle
                    self.rot_center(self.angle)
                    self.get_players_adj_outline

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rect.centerx = base_round_floor(self.rect.centerx)
        self.rect.centery = base_round_floor(self.rect.centery)

        self.get_players_adj_outline()

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

        if self.adjusted_outline & obstacle_set:

            self.rect.x -= self.speedx
            self.rect.y -= self.speedy

        User.rect_centerx, User.rect_centery = self.rect.centerx, self.rect.centery
        User.angle = self.angle

        # this din't work :(
        # if self.machine_gun_shooting:
        if pressed_keystate[pygame.K_SPACE]:
            MachineGunFire(self.rect.centerx, self.rect.centery, self.angle, 15)
            MachineGunFire(self.rect.centerx, self.rect.centery, self.angle, -15)
            User.mgf_sound.play()

    def rot_center(self, angle):
        """rotate an image while keeping its center"""
        self.image = pygame.transform.rotate(self.image_original, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    @staticmethod
    def get_player_location() -> Tuple[int, int]:

        return User.rect_centerx, User.rect_centery

    @staticmethod
    def get_player_angle() -> float:

        return User.angle

    def get_players_adj_outline(self) -> None:

        self.mask = pygame.mask.from_surface(self.image)
        self.outline = self.mask.outline()
        self.adjusted_outline = {tuple(map(operator.add, node, self.rect.topleft)) for node in self.outline}


class UserCoordsText():

    def __init__(self):

        self.myfont = pygame.font.Font(None, 15)
        self.label = self.myfont.render('coords:  ' + str(User.get_player_location())
                                        + ',  angle:  ' + str(User.angle), 1, (0,0,0))

    def update(self):

        self.label = self.myfont.render('coords:  ' + str(User.get_player_location())
                                        + ',  angle:  ' + str(User.angle), 1, (0,0,0))


''' generate sprite groups'''
all_sprites = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
all_elementals = pygame.sprite.Group()
all_wall_sprites = pygame.sprite.Group()
all_shrapnel = pygame.sprite.Group()

''' instantiate player sprite and add to all_sprites '''
user1 = User()
all_sprites.add(user1)

''' instantiate text display '''
userCoordsDisplay = UserCoordsText()

''' generate multiple enemies - automatically added to all_elemental sprite group '''
e_x, e_y = 150, 100
el1 = ElementalEntities(e_x, e_y+10)
el3 = ElementalEntities(e_x, e_y+20)
el4 = ElementalEntities(e_x, e_y+30)
el5 = ElementalEntities(e_x, e_y+40)
el6 = ElementalEntities(e_x, e_y+50)
el7 = ElementalEntities(e_x, e_y+60)
el8 = ElementalEntities(e_x, e_y+70)
el9 = ElementalEntities(e_x, e_y+80)
el10 = ElementalEntities(e_x, e_y+90)
el11 = ElementalEntities(e_x, e_y+100)
el12 = ElementalEntities(e_x, e_y+110)
el13 = ElementalEntities(e_x, e_y+120)
el14 = ElementalEntities(e_x, e_y+130)
el15 = ElementalEntities(e_x+100, e_y+140)
el16 = ElementalEntities(e_x+100, e_y+150)
el17 = ElementalEntities(e_x+100, e_y+160)
el18 = ElementalEntities(e_x+100, e_y+170)
el19 = ElementalEntities(e_x+100, e_y+180)
el20 = ElementalEntities(e_x+100, e_y+190)

''' create obstacles '''
# Obstacle.set_pygame(pygame)
Obstacle.set_obstacle_container(obstacle_set)
Obstacle.set_all_wall_sprites_container(all_wall_sprites)

# wall1 = Obstacle((350, 350), (370, 370))
tree1 = Tree((700, 50), (750, 100), "t_1")
tree1 = Tree((750, 50), (800, 100), "t_1")
tree1 = Tree((700, 100), (750, 150), "t_1")
tree1 = Tree((200, 300), (250, 350), "t_1")
tree1 = Tree((600, 100), (650, 150), "t_1")
tree1 = Tree((300, 200), (350, 250), "t_1")
tree1 = Tree((350, 200), (400, 250), "t_1")
tree1 = Tree((400, 200), (450, 250), "t_1")

# input('obstacles: {}'.format(Obstacle._obstacles))
# input('walls: {}'.format(Obstacle._all_wall_sprites))

''' main loop'''
while True:

    ''' run with established frame rate per sec '''
    clock.tick(fps)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ''' update sprite groups and text display '''
    all_sprites.update()
    all_bullets.update()
    all_elementals.update()
    all_shrapnel.update()
    userCoordsDisplay.update()

    ''' on enemy and bullet collsion -> delete elemental '''
    hits = pygame.sprite.groupcollide(all_elementals, all_bullets, True, True, pygame.sprite.collide_mask)
    hits = pygame.sprite.groupcollide(all_wall_sprites, all_bullets, False, True, pygame.sprite.collide_mask)

    ''' blit images on screen '''
    screen.blit(background_image, [0, 0])
    screen.blit(userCoordsDisplay.label, [835, 480])
    all_wall_sprites.draw(screen)
    all_bullets.draw(screen)
    all_sprites.draw(screen)
    all_elementals.draw(screen)
    all_shrapnel.draw(screen)
    pygame.display.flip()
