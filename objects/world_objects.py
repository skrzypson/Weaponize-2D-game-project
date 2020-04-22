import operator
import pygame
import random

from typing import Tuple, Set


class Obstacle(pygame.sprite.Sprite):
    """ Generic obstacle class """
    _obstacles = None
    _all_wall_sprites = None

    def __new__(cls, top_left_corner: Tuple[int,int], bottom_right_corner: Tuple[int,int]):
        """ Force the user to set the containers prior to instantiating obstacles.

        Args:
            top_left_corner:
            bottom_right_corner:
        """
        if not hasattr(cls, '_obstacles'):
            raise Exception("First set the _obstacles container before instantiating an Obstacle")
        if not hasattr(cls, '_all_wall_sprites'):
            raise Exception("First set the _all_wall_sprites container before instantiating an Obstacle")
        return pygame.sprite.Sprite.__new__(cls)

    def __init__(self, top_left_corner: Tuple[int,int], bottom_right_corner: Tuple[int,int]):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((abs(top_left_corner[0] - bottom_right_corner[0])
                                     , abs(top_left_corner[1] - bottom_right_corner[1]))).convert()

        self.image.fill((0, 0, 0))
        self.image.set_alpha(150)
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left_corner

        self.inner_outline = set()
        for _ in range(1, 5):

            self.temp_surf = pygame.Surface((abs(top_left_corner[0] - bottom_right_corner[0]) - 2*_
                                    , abs(top_left_corner[1] - bottom_right_corner[1]) - 2*_)
                                    ).convert_alpha()

            self.temp_mask = pygame.mask.from_surface(self.temp_surf)
            self.temp_outline = self.temp_mask.outline()
            self.temp_adjusted_outline = {tuple(map(operator.add, node, self.rect.topleft))
                                          for node in self.temp_outline}
            self.inner_outline.update(self.temp_adjusted_outline)

        del self.temp_surf, self.temp_outline, self.temp_mask, self.temp_adjusted_outline

        self.mask = pygame.mask.from_surface(self.image)
        self.outline = self.mask.outline()
        self.adjusted_outline = {tuple(map(operator.add, node, self.rect.topleft))
                                 for node in self.outline}.union(self.inner_outline)
        del self.inner_outline

        Obstacle._obstacles.update(self.adjusted_outline)
        print('stuff')
        print(Obstacle._obstacles, len(Obstacle._obstacles))
        Obstacle._all_wall_sprites.add(self)

    @classmethod
    def set_obstacle_container(cls, obst_container):
        assert isinstance(obst_container, set)
        cls._obstacles = obst_container

    @classmethod
    def set_all_wall_sprites_container(cls, wall_container):
        assert isinstance(wall_container, pygame.sprite.Group)
        cls._all_wall_sprites = wall_container


class Tree(Obstacle):
    tree_types_loc = "../graphics/trees/"
    tree_types = dict({"t_1": "tree_1"})

    def __new__(cls, top_left_corner: Tuple[int, int], bottom_right_corner: Tuple[int, int], tree_type: str):
        # super().__new__(top_left_corner, bottom_right_corner)
        # super().__new__()
        return Obstacle.__new__(cls, top_left_corner, bottom_right_corner)

    def __init__(self, top_left_corner: Tuple[int, int], bottom_right_corner: Tuple[int, int], tree_type: str):
        assert (bottom_right_corner[0] - top_left_corner[0]) % 50 == 0
        assert (bottom_right_corner[1] - top_left_corner[1]) % 50 == 0
        assert tree_type in Tree.tree_types

        super().__init__(top_left_corner, bottom_right_corner)
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.image.load(Tree.tree_types_loc + Tree.tree_types[tree_type] + ".png").convert()
        self.image_original.set_colorkey((255, 255, 255))
        self.image = self.image_original.copy()
        self.image.set_colorkey((255, 255, 255))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left_corner


if __name__ == "__main__":
    ...
