# ========================================================
# gameboy resolution is 160 x 144 with 16 x 16 tiles
# ========================================================
import pygame, sys, random, os, math, json
clock = pygame.time.Clock()
from pygame.locals import *

pygame.init()

# DEFAULT VALUES
TILE_SIZE = 16

x_tiles = 10
canvas_width = x_tiles * TILE_SIZE
palette_width = TILE_SIZE * 3
WIN_WIDTH = canvas_width + palette_width

y_tiles = 9
WIN_HEIGHT = y_tiles * TILE_SIZE

WIN_SCALE = 3 if TILE_SIZE == 16 else 4

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
    print("Welcome to your own in-house tile editor. You can use this to draw tiles on a grid of a size of your choosing, and then output that as a json file.")
    print("Please input your desired x and y dimensions IN TILES, respectively.")
    print("NOTE: I recommend sticking to a 4:3 aspect ratio.")

    u_tile_size = int(input("Enter tile size: "))
    if u_tile_size == 8 or u_tile_size == 16 :
        TILE_SIZE = u_tile_size
        print(TILE_SIZE)
    else : 
        print("Invalid tile size - reverting to default of 16")

    # NEXT TODO: ADJUST WIN SIZE FOR TILE SIZE AFTER POLLING FOR IT 
    # A LITTLE SILLY BUT PROBABLY EASIEST JUST TO HARDCODE IT

poll_user()

print(TILE_SIZE)

# HELPER DATA ============================================
display_window = pygame.display.set_mode((WIN_WIDTH * WIN_SCALE, WIN_HEIGHT * WIN_SCALE), 0, 32)
raw_window = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))

canvas_rect = pygame.Rect(0,0, 160 * WIN_SCALE, 144 * WIN_SCALE)
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