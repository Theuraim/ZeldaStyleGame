import pygame, os 
from settings import *


class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.curent_directory = os.getcwd()
		self.image = pygame.image.load(self.curent_directory + '\\graphics\\test\\rock.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)