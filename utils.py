# ========================================================
# gameboy resolution is 160 x 144 with 16 x 16 tiles
# ========================================================
import pygame, sys, random, os, math, json
clock = pygame.time.Clock()
from pygame.locals import *
from tkinter import * 
import tkinter as tk

# https://stackoverflow.com/questions/23319059/embedding-a-pygame-window-into-a-tkinter-or-wxpython-frame
pygame.init()
root = tk.Tk()
root.title("At Home Map Maker")
root.geometry("250x170")

label = tk.Label(root, text="Foobar: ")
label.pack()
entry = tk.Entry(root)
entry.pack()

root.mainloop()


# DEFAULT VALUES
TILE_SIZE = 16
X_TILES = 10
Y_TILES = 9

# HELPER FUNCTIONS ==========================================
BASE_PATH = './'
def load_image(path):
    img = pygame.image.load(BASE_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_dir(path) :
    images = []
    for img_name in sorted(os.listdir(BASE_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

# normalize according to tile size
def adjust_mouse_pos(coords : tuple) :
    adjusted_coords = (
        math.floor( (coords[0]) / (TILE_SIZE * WIN_SCALE) ), 
        math.floor( (coords[1]) / (TILE_SIZE * WIN_SCALE) )
    )
    return adjusted_coords

# TODO: take this out of the CLI
def poll_user() -> None :
    global TILE_SIZE
    global X_TILES
    global Y_TILES
    skip_y = False

    print("Welcome to your own in-house tile editor. You can use this to draw tiles on a grid of a size of your choosing, and then output that as a json file.")
    print("NOTE: CHARACTER INPUT FAILS")
    # POLL FOR TILE SIZE
    u_tile_size = int(input("Enter tile size: "))
    if u_tile_size == 8 or u_tile_size == 16 :
        TILE_SIZE = u_tile_size
        print(TILE_SIZE)
    else : 
        print("Invalid tile size - reverting to default of 16")

    # POLL FOR X AND Y DIMENSIONS
    print("When inputting x tiles, press enter (blank/invalid) to default to a 10x9 gameboy resolution.")
    # this feels silly
    u_x_tiles = input("Enter the number of tiles in the x-axis: ")
    if not u_x_tiles.isnumeric() :
        skip_y = True
        u_x_tiles = 10
    
    X_TILES = int(u_x_tiles)

    if not skip_y :
        print("When inputting y tiles, press enter (blank/invalid) to default to a 4:3 ratio of whatever x-dimensions you inputted.")
        print("NOTE: gameboy ratio != 4:3")
        u_y_tiles = input("Enter the number of tiles in the y-axis: ")
        if not u_y_tiles.isnumeric() :
            u_y_tiles = math.floor((X_TILES * 3 ) / 4 )
            print("Defaulting to our calculated 4:3 ratio: ", X_TILES, u_y_tiles)
        
        Y_TILES = u_y_tiles 
    else :
        print("Defaulting to 10 x 9 dimesions.")
        Y_TILES = 9

poll_user()

canvas_width = X_TILES * TILE_SIZE
palette_width = TILE_SIZE * 3
WIN_WIDTH = canvas_width + palette_width

WIN_HEIGHT = Y_TILES * TILE_SIZE

WIN_SCALE = 3 if TILE_SIZE == 16 else 4

print(TILE_SIZE)

# HELPER DATA ============================================
display_window = pygame.display.set_mode((WIN_WIDTH * WIN_SCALE, WIN_HEIGHT * WIN_SCALE), 0, 32)
raw_window = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))

canvas_rect = pygame.Rect(0,0, (canvas_width) * WIN_SCALE, WIN_HEIGHT * WIN_SCALE)
subsurf = display_window.subsurface(canvas_rect)

draw_grid = False

x_offset = 0
y_offset = 0

# TODO: choose a specific directory to load in from
tile_palette = load_dir("tiles-16") if TILE_SIZE == 16 else load_dir("tiles-8")

curr_brush = None
curr_brush_value = -1
canvas = {
    # tile coordinates : tile type in coord
}
painting = False
erasing = False
# IM PRETTY SURE CANVAS BUFFER ACTS AS THE IN-BETWEEN FOR WHEN WE'RE HOLDING THE MOUSE
# CLICK DOWN TO DRAW SOMETHING
canvas_buffer = {}