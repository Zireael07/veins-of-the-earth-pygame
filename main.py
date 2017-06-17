import libtcodpy as libtcod
import pygame
import constants


class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path


class obj_Actor:
    def __init__(self, x, y, name_object, sprite, creature = None):
        self.x = x
        self.y = y
        self.sprite = sprite

        if creature:
            self.creature = creature

    def draw(self):
        SURFACE_MAIN.blit(self.sprite, (self.x*constants.TILE_WIDTH, self.y*constants.TILE_HEIGHT))

    def move(self, dx, dy):
        if self.y + dy >= len(GAME_MAP):
            print("Tried to move out of map")
            return

        if self.x+dx >= len(GAME_MAP[0]):
            print("Tried to move out of map")
            return

        if not GAME_MAP[self.x+dx][self.y+dy]:
            print("Tried to move out of map")
            return


        target = None
        for ent in ENTITIES:
            if (ent is not self
                and ent.x == self.x + dx
                and ent.y == self.y + dy):
                print("Tried to move into occupied tile")
                target = ent
                break
                # return


        tile_is_wall = (GAME_MAP[self.x+dx][self.y+dy].block_path == True)

        if not tile_is_wall and target is None:
            self.x = self.x+dx
            self.y = self.y+dy

class com_Creature:
    def __init__(self, name_instance, hp = 10):
        self.name_instance = name_instance
        self.hp = hp

# MAP
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
    # draw characters
    ENEMY.draw()
    PLAYER.draw()

    # update the display
    pygame.display.flip()


def draw_map(map):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map[x][y].block_path == True:
                # draw wall
                SURFACE_MAIN.blit(constants.S_WALL, (x*constants.TILE_WIDTH, y*constants.TILE_HEIGHT))
            else:
                # draw floor
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    PLAYER.move(0,-1)
                if event.key == pygame.K_DOWN:
                    PLAYER.move(0,1)
                if event.key == pygame.K_LEFT:
                    PLAYER.move(-1,0)
                if event.key == pygame.K_RIGHT:
                    PLAYER.move(1,0)

        # draw
        draw_game()

    # quit the game
    pygame.quit()
    exit()


# Execute game
def game_initialize():
    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, ENTITIES

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode( [constants.GAME_WIDTH, constants.GAME_HEIGHT] )

    GAME_MAP = map_create()

    creature_com1 = com_Creature("Player")
    PLAYER = obj_Actor(0, 0, "Player", constants.S_PLAYER, creature=creature_com1)

    creature_com2 = com_Creature("kobold")
    ENEMY = obj_Actor(9, 9, "kobold", constants.S_KOBOLD, creature=creature_com2)

    ENTITIES = [PLAYER, ENEMY]

if __name__ == "__main__":
    game_initialize()
    game_main_loop()