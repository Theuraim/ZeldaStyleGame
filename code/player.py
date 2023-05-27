import pygame, os
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.curent_directory = os.getcwd()
        self.image = pygame.image.load(self.curent_directory +'\\graphics\\test\\player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)