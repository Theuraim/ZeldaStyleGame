import pygame
import settings
from tile import Tile
from player import Player
from worldmap import *

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        #Map setup
        settings.WORLD_MAP = self.setWorldMap()
        # sprite setup
        self.create_map()

    def setWorldMap(self):
        # Example usage
        self.width = 200
        self.height = 50
        self.wall_chance = 0.3
        self.world_map = generate_map(self.width, self.height, self.wall_chance)
        for row in self.world_map:
            print(' '.join(row))
        return self.world_map

    def create_map(self):
        for row_index, row in enumerate(settings.WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * settings.TILESIZE
                y = row_index * settings.TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    Player((x,y), [self.visible_sprites])

    def run(self):
        # update and draw the game
        self.visible_sprites.draw(self.display_surface)