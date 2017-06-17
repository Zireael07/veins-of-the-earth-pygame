import pygame

#Game sizes
GAME_WIDTH = 800
GAME_HEIGHT = 600

MAP_WIDTH = 20
MAP_HEIGHT = 20

TILE_WIDTH = 42
TILE_HEIGHT = 32

#Color definitions
COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)

#Game colors
COLOR_DEFAULT_BG = COLOR_GREY

#Sprites

S_PLAYER = pygame.image.load("gfx/human_m.png")
S_WALL = pygame.image.load("gfx/wall_stone.png")
S_FLOOR = pygame.image.load("gfx/floor_sand.png")