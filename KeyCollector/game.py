import pgzrun


#this the number of vertical and horizontal tiles along with the size of each tile square:
height_grid = 12
width_grid = 16
size_grid = 50

#total height and width of game window screen:
HEIGHT = size_grid * height_grid
WIDTH = size_grid * width_grid

#game grid with the characters presenting different game elements like keys and players:
MAP = ["WWWWWWWWWWWWWWWW",
       "W              W",
       "W              W",
       "W  W  KG       W",
       "W  WWWWWWWWWW  W",
       "W      P       W",
       "W              D",
       "W  WWWWWWWWWW  W",
       "W      GK   W  W",
       "W              W",
       "W              W",
       "WWWWWWWWWWWWWWWW"]

#making the game floor:
def coords(x, y):
    return (size_grid * x, size_grid * y)

#current player coords:
def item_coords(actor):
    current_x = actor.x / size_grid
    current_y = actor.y / size_grid
    return (round(current_x), round(current_y))

#creating an actor with an initial position:
def init():
    global player, enemies, keys_ingame, gm_over
    keys_ingame = []
    enemies = []
    gm_over = False
    player = Actor("player", anchor=("left", "top"))
    for y in range(height_grid):
        for x in range(width_grid):
            #locate player position and extract it:
            sq = MAP[y][x]
            if sq == "P":
                player.pos = coords(x, y)
            elif sq == "G":
                enemy = Actor("guard", anchor=("left", "top"), pos=coords(x, y))
                enemies.append(enemy)
            #create a key:
            elif sq == "K":
                key = Actor("key", anchor=("left", "top"), pos=coords(x, y))
                keys_ingame.append(key)

def actors():
    player.draw()
    for enemy in enemies:
        enemy.draw()
    for key in keys_ingame:
        key.draw()


def bg():
    for y in range(height_grid):
        for x in range(width_grid):
            screen.blit("floor1", coords(x, y))

#making the sceneary (each tile's skeleton background):
def scene():
    for y in range(height_grid):
        for x in range(width_grid):
            #extracting the chracter from the map list:
            sq = MAP[y][x]
            if sq == "W":
                screen.blit("wall", coords(x, y))
            elif sq == "D":
                screen.blit("door", coords(x, y))

#this function is part of the game loop and used to draw all tiles:
def draw():
    bg()
    scene()
    actors()

init()

pgzrun.go()
