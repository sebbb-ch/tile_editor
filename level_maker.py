    # done: infinite grid that i can scroll through with wasd
    # done(kinda): move the grid with wasd
        # could use continuous scroll
    # done: maintain canvas along with palette
# current objective: A MAP MAKER
    # doing: tile picker from palette
# ========================================================
# DESIRED FUNCTIONALITY
    # load in tiles from png folder onto the palette
    # click on a tile in palette to select is as brush
    # when brush is selected, click on canvas to place current selected tile
    # export created maps onto a file
# ========================================================
# gameboy resolution is 160 x 144
# 16 x 16 tiles
# ========================================================
import pygame, sys, random, os, math
clock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
WIN_WIDTH = 160 + 48
WIN_HEIGHT = 144
WIN_SCALE = 4

BASE_PATH = './'

display_window = pygame.display.set_mode((WIN_WIDTH * WIN_SCALE, WIN_HEIGHT * WIN_SCALE), 0, 32)
raw_window = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))

playing = True

draw_grid = False

x_offset = 0
y_offset = 0


def load_image(path):
    img = pygame.image.load(BASE_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_dir(path) :
    images = []
    for img_name in sorted(os.listdir(BASE_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

frame_start = 0
frame_end = pygame.time.get_ticks()
dt = frame_end - frame_start
# ========================================
tile_palette = load_dir("tiles")
curr_brush = None
# ========================================
while playing:
    frame_start = frame_end
    raw_window.fill((0,0,0))

    for event in pygame.event.get() :
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN : 
            if event.key == K_ESCAPE:
                playing = False
            if event.key == K_g :
                # toggle grid drawing
                draw_grid = not draw_grid
            # we wanna think of holding one of the wasd keys as constantly adding an offset
            if event.key == K_w : # up
                y_offset -= 4
            if event.key == K_a : # left
                x_offset -= 4
            if event.key == K_s : # down 
                y_offset += 4
            if event.key == K_d : # right
                x_offset += 4
        if event.type == pygame.MOUSEBUTTONDOWN :
            click_coords = pygame.mouse.get_pos()
            # if click was in the palette
            if click_coords[0] > 160 * WIN_SCALE :
                if event.button == 1:
                    # turn mouse click coords into tile array index
                    index = math.floor(((click_coords[0] / (WIN_SCALE *16)) - 1) % 3) + 3 * math.floor((click_coords[1] / (WIN_SCALE * 16)))
                    if index < len(tile_palette) :
                        curr_brush = tile_palette[index]
                    else :
                        curr_brush = None
            # if click coords were in the canvas
            else : 
                pass
            

    
    # PALETTE =========================================
    draw_pos = [0,0]
    for i in range(len(tile_palette)) :
        draw_pos[0] = 16 * 10 + (16 * (i % 3))
        if i % 3 == 0 and i != 0:
            draw_pos[1] += 16
        raw_window.blit(tile_palette[i], pygame.Rect(draw_pos, (16, 16)))
    # CANVAS ==========================================
    if draw_grid :
        # draw grid lines
        # NOTE: we don't need to adjust for win_scale because we're drawing directly onto the raw surface, which then gets scaled
        for i in range(0, WIN_WIDTH - 48) :
            if (i - x_offset) % 16 == 0:
                pygame.draw.line(raw_window, (255, 0, 0), (i, 0), (i, WIN_HEIGHT))
        for i in range(0, WIN_HEIGHT) :
            if (i - y_offset) % 16 == 0 :
                pygame.draw.line(raw_window, (255, 0, 0), (0,i), (WIN_WIDTH - 48, i))

        # get mouse position, normalize it to 16x16 grid, account for offset
        mouse_pos = pygame.mouse.get_pos()
        adjusted_mouse_pos = (
            # again, why the fuckinng * 4
            math.floor( (mouse_pos[0] ) / (16 * WIN_SCALE) ), 
            math.floor( (mouse_pos[1] ) / (16 * WIN_SCALE) )
            )
        print(adjusted_mouse_pos)
        if curr_brush != None :
            raw_window.blit(
                curr_brush, 
                pygame.Rect(
                    adjusted_mouse_pos[0] * 16 , 
                    adjusted_mouse_pos[1] * 16 , 
                    16 * WIN_SCALE,
                    16 * WIN_SCALE
                    )
            )
                

    # ========
    scaled_window = pygame.transform.scale(raw_window, display_window.get_size())
    display_window.blit(scaled_window, (0,0))
    pygame.display.update()

    # ========
    frame_end = pygame.time.get_ticks()
    dt = frame_end - frame_start
    clock.tick(60)

pygame.quit()
sys.exit()
