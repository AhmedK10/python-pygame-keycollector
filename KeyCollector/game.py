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



pgzrun.go()
