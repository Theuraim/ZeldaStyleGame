import pygame
import settings
from tile import Tile
from player import Player
from worldmap import *
from debug import debug 

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #Map setup
        settings.WORLD_MAP = self.setDungeon()
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

    def setDungeon(self):
        self.width = 80
        self.height = 40
        self.num_rooms = 20

        self.dungeon = generate_dungeon(self.width, self.height, self.num_rooms)
        for row in self.dungeon:
            print(' '.join(row))
        
        return self.dungeon

    def create_map(self):
        for row_index, row in enumerate(settings.WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * settings.TILESIZE
                y = row_index * settings.TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        #debug(self.player.direction)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    
    def custom_draw(self, player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)