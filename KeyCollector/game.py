import pgzrun


#this the number of vertical and horizontal tiles along with the size of each tile square:
height_grid = 15
width_grid = 20
size_grid = 50
enemy_move_secs = 0.6

#total height and width of game window screen:
HEIGHT = size_grid * height_grid
WIDTH = size_grid * width_grid

#game grid with the characters presenting different game elements like keys, enemies and players:
MAP = ["WWWWWWWWWWWWWWWWWWWW",
       "W         WW   W   W",
       "W  W           W   W",
       "W  W  KG           W",
       "W  WWWWWWWWWW      W",
       "W      P           W",
       "W                  D",
       "W  WWWWWWWWWW      W",
       "W      GK   W      W",
       "W           W    W W",
       "W                W W",
       "W     WWWW WWW     W",
       "W    W  K          W",
       "W       G          W",
       "WWWWWWWWWWWWWWWWWWWW"]

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

#Messages during game:
def game_over():
    screen_middle = (WIDTH / 2, HEIGHT / 2)
    screen.draw.text("GAME OVER", midbottom=screen_middle, fontsize=size_grid, color="gray", owidth=3)
    if won:
        screen.draw.text("You WON!!!", midtop=screen_middle, fontsize=size_grid, color="green", owidth=1)
    else:
        screen.draw.text("YOU DIED :(", midtop=screen_middle, fontsize=size_grid, color="red", owidth=1)

    screen.draw.text("Press SPACEBAR to Restart", midtop=(WIDTH / 2, size_grid + HEIGHT / 2), fontsize=size_grid / 2, color="gray", owidth=2)

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
    if gm_over:
        game_over()

#restarting automatically:
def on_key_up(key):
    if key == keys.SPACE and gm_over:
        init()

#detect keyboard key press and moves player:
def on_key_down(key):
    if key == keys.UP:
        player_mover(0, -1)
    elif key == keys.DOWN:
        player_mover(0, 1)
    elif key == keys.LEFT:
        player_mover(-1, 0)
    elif key == keys.RIGHT:
        player_mover(1, 0)

def player_mover(dx, dy):
    global gm_over, won
    if gm_over:
        return
    #getting current player position:
    (x, y) = item_coords(player)
    x = x + dx
    y = y + dy
    #getting the tile at the this position:
    sq = MAP[y][x]
    if sq == "W":
        return
    elif sq == "D":
        if len(keys_ingame) > 0:
            return
        else:
            gm_over = True
            won = True
    #looping over each key in the list:
    for key in keys_ingame:
        (x_key, y_key) = item_coords(key)
        if x == x_key and y == y_key:
            keys_ingame.remove(key)
            break
    #update the position to new one:
    player.pos = coords(x, y)

#moving the enemy while checking position relative to player:
def enemy_mover(enemy):
    global gm_over
    if gm_over:
        return
    (x_player, y_player) = item_coords(player)
    (x_enemy, y_enemy) = item_coords(enemy)

    if x_player < x_enemy and MAP[y_enemy][x_enemy - 1] != "W":
        x_enemy -= 1
    elif x_player > x_enemy and MAP[y_enemy][x_enemy + 1] != "W":
        x_enemy += 1
    elif y_player > y_enemy and MAP[y_enemy + 1][x_enemy] != "W":
        y_enemy += 1
    elif y_player < y_enemy and MAP[y_enemy - 1][x_enemy] != "W":
        y_enemy -= 1

    enemy.pos = coords(x_enemy, y_enemy)
    if x_enemy == x_player and y_enemy == y_player:
        gm_over = True

#moves all enemies in turn:
def enemies_mover():
    for enemy in enemies:
        enemy_mover(enemy)

init()
clock.schedule_interval(enemies_mover, enemy_move_secs)

pgzrun.go()
