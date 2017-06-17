import libtcodpy as libtcod
import pygame

import constants

class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path

def map_create():
    new_map = [[ struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    new_map[10][10].block_path = True
    new_map[12][12].block_path = True

    return new_map

def draw_game():
    # clear
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    # draw map
    draw_map(GAME_MAP)
    # draw character
    SURFACE_MAIN.blit(constants.S_PLAYER, (200, 200))

    # update the display
    pygame.display.flip()

def draw_map(map):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map[x][y].block_path == True:
                #draw wall
                SURFACE_MAIN.blit(constants.S_WALL, (x*constants.TILE_WIDTH, y*constants.TILE_HEIGHT))
            else:
                #draw floor
                SURFACE_MAIN.blit(constants.S_FLOOR, (x*constants.TILE_WIDTH, y*constants.TILE_HEIGHT))

def game_main_loop():
    game_quit = False

    while not game_quit:
        # get input
        events_list = pygame.event.get()

        # process input
        for event in events_list:
            if event.type == pygame.QUIT:
                game_quit = True

        # draw
        draw_game()

    #quit the game
    pygame.quit()
    exit()


# Execute game
def game_initialize():
    global SURFACE_MAIN, GAME_MAP

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode( [constants.GAME_WIDTH, constants.GAME_HEIGHT] )

    GAME_MAP = map_create()

if __name__ == "__main__":
    game_initialize()
    game_main_loop()