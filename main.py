import libtcodpy as libtcod
import pygame
import constants


class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path


class obj_Actor:
    def __init__(self, x, y, name_object, sprite, creature = None, ai = None):
        self.x = x
        self.y = y
        self.sprite = sprite

        self.creature = creature
        if creature:

            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

    def draw(self):
        is_visible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)

        if is_visible:
            SURFACE_MAIN.blit(self.sprite, (self.x*constants.TILE_WIDTH, self.y*constants.TILE_HEIGHT))



class com_Creature:
    def __init__(self, name_instance, hp = 10, death_function = None):
        self.name_instance = name_instance
        self.max_hp = hp
        self.hp = hp
        self.death_function = death_function

    def move(self, dx, dy):
        if self.owner.y + dy >= len(GAME_MAP) or self.owner.y + dy < 0:
            print("Tried to move out of map")
            return

        if self.owner.x+dx >= len(GAME_MAP[0]) or self.owner.x + dx < 0:
            print("Tried to move out of map")
            return

        if not GAME_MAP[self.owner.x+dx][self.owner.y+dy]:
            print("Tried to move out of map")
            return


        target = None

        target = map_check_for_creature(self.owner.x+dx, self.owner.y+dy, self.owner)

        if target:
            self.attack(target, 5)

        tile_is_wall = (GAME_MAP[self.owner.x+dx][self.owner.y+dy].block_path == True)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target, damage):
        print(self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + " damage!")
        target.creature.take_damage(damage)


    def take_damage(self, damage):
        self.hp -= damage
        print self.name_instance + " 's hp is " + str(self.hp) + "/" + str(self.max_hp)

        if self.hp < 0:
            if self.death_function is not None:
                self.death_function(self.owner)

class AI_test:
    def take_turn(self):
        self.owner.creature.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))

def death_monster(monster):
    print monster.creature.name_instance + " is dead!"
    monster.creature = None
    monster.ai = None
    # remove from map
    ENTITIES.remove(monster)

# MAP
def map_create():
    new_map = [[ struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    new_map[10][10].block_path = True
    new_map[12][12].block_path = True

    # walls around the map
    for x in range(constants.MAP_WIDTH):
        new_map[x][0].block_path = True
        new_map[x][constants.MAP_WIDTH-1].block_path = True

    for y in range(constants.MAP_HEIGHT):
        new_map[0][y].block_path = True
        new_map[constants.MAP_HEIGHT-1][y].block_path = True

    map_make_fov(new_map)

    return new_map

def map_check_for_creature(x, y, exclude_entity = None):
    target = None

    # find entity that isn't excluded
    if exclude_entity:
        for ent in ENTITIES:
            if (ent is not exclude_entity
                and ent.x == x
                and ent.y == y
                and ent.creature):
                # print("Tried to move into occupied tile")
                target = ent


            if target:
                return target

    # find any entity if no exclusions
    else:
        for ent in ENTITIES:
            if (ent.x == x
                and ent.y == y
                and ent.creature):
                # print("Tried to move into occupied tile")
                target = ent

def map_make_fov(incoming_map):
    global FOV_MAP
    FOV_MAP = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            libtcod.map_set_properties(FOV_MAP, x,y,
                                       not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)

def map_calculate_fov():
    global FOV_CALCULATE

    if FOV_CALCULATE:
        FOV_CALCULATE = False
        libtcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.LIGHT_RADIUS, constants.FOV_LIGHT_WALLS,
                                constants.FOV_ALGO)

def draw_game():
    # clear
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    # draw map
    draw_map(GAME_MAP)
    # draw characters
    for ent in ENTITIES:
        ent.draw()

    # update the display
    pygame.display.flip()


def draw_map(map):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):

            is_visible = libtcod.map_is_in_fov(FOV_MAP, x, y)

            if is_visible:
                if map[x][y].block_path == True:
                    # draw wall
                    SURFACE_MAIN.blit(constants.S_WALL, (x*constants.TILE_WIDTH, y*constants.TILE_HEIGHT))
                else:
                    # draw floor
                    SURFACE_MAIN.blit(constants.S_FLOOR, (x*constants.TILE_WIDTH, y*constants.TILE_HEIGHT))

def game_main_loop():
    game_quit = False
    player_action = "no-action"

    while not game_quit:

        player_action = game_handle_keys()

        map_calculate_fov()

        if player_action == "QUIT":
            game_quit = True

        elif player_action != "no-action":
            for ent in ENTITIES:
                if ent.ai:
                    ent.ai.take_turn()

        # draw
        draw_game()

    # quit the game
    pygame.quit()
    exit()

def game_handle_keys():
    global FOV_CALCULATE

    # get input
    events_list = pygame.event.get()

    # process input
    for event in events_list:
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER.creature.move(0, -1)
                FOV_CALCULATE = True
                return "player-moved"
            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0, 1)
                FOV_CALCULATE = True
                return "player-moved"
            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1, 0)
                FOV_CALCULATE = True
                return "player-moved"
            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1, 0)
                FOV_CALCULATE = True
                return "player-moved"

    return "no-action"

# Init game (watch out for globals)
def game_initialize():
    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, ENTITIES, FOV_CALCULATE

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode( [constants.MAP_WIDTH*constants.TILE_WIDTH,
                                             constants.MAP_HEIGHT*constants.TILE_HEIGHT] )

    GAME_MAP = map_create()

    FOV_CALCULATE = True

    creature_com1 = com_Creature("Player")
    PLAYER = obj_Actor(1, 1, "Player", constants.S_PLAYER, creature=creature_com1)

    creature_com2 = com_Creature("kobold", death_function=death_monster)
    ai_com = AI_test()
    ENEMY = obj_Actor(9, 9, "kobold", constants.S_KOBOLD, creature=creature_com2, ai=ai_com)

    ENTITIES = [PLAYER, ENEMY]

# Execute game
if __name__ == "__main__":
    game_initialize()
    game_main_loop()