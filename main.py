import libtcodpy as libtcod
import pygame

import constants

def game_main_loop():
    game_quit = False

    while not game_quit:
        # get input
        events_list = pygame.event.get()

        # process input
        for event in events_list:
            if event.type == pygame.QUIT:
                game_quit = True

        # TODO draw

    #quit the game
    pygame.quit()
    exit()

def game_initialize():

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode( [constants.GAME_WIDTH, constants.GAME_HEIGHT] )

if __name__ == "__main__":
    game_initialize()
    game_main_loop()