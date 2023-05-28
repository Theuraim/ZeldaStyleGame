import pygame, settings, os
from support import *
from tile import Tile
from player import Player
from worldmap import *
from debug import debug 

class Level:
    def __init__(self):
        #get the path for the project
        self.path = os.getcwd()
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #Map setup
        #settings.WORLD_MAP = self.setDungeon()
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
        layout = {
            'boundary': import_csv_layout(self.path + '/map/map_floorBlocks.csv'),
            'grass': import_csv_layout(self.path + '/map/map_Grass.csv'),
            'object': import_csv_layout(self.path + '/map/map_LargeObjects.csv')
        }

        graphics = {
            'grass': import_folder(self.path + '/graphics/grass'),
            'objects': import_folder(self.path + '/graphics/objects') 
        }

        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * settings.TILESIZE
                        y = row_index * settings.TILESIZE

                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], sprite_type = 'invisible')
                        if style == 'grass':
                            #creates the grass tiles
                            random_grass_image = random.choice(graphics['grass'])
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)

                            
                            pass
                        if style == 'object':
                            #create the object tiles
                            surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                        
        self.player = Player((2000,1430), [self.visible_sprites], self.obstacle_sprites)

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
        self.path = os.getcwd()

        #creating the floor
        self.floor_surf = pygame.image.load(self.path + '/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))
    
    def custom_draw(self, player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)