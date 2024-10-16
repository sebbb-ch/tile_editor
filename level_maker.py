from textbox import *

user_polling = True
playing = True

# tbox = Textbox((40, 6))
# tbox.open()
# tbox.print("This is an example query")
# tbox.multiprint(
#     "This is an example of a query",
#     "that could span multiple lines",
#     "though I'm not sure if it's necessary if text wrapping is going be automatic"
# )
# # I'd like for the polling to be always on the bottom line and things get pushed up as you enter them
# # In other words, the bottom line will always be reserved for user input
# tbox.get()
# tbox.close()
# # QUESTION : how are we going to get that data from the textbox over to the main program

tbox = Textbox(40, 20)
while user_polling :
    for event in pygame.event.get() :
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            user_polling = False
        
        if event.type == KEYDOWN :
            tbox.handle_type_event(event)
            if event.key == K_RETURN :
                print("enter")
                # TODO: FIX THIS BUG
                tbox.text_print("I pressed enter") 

    tbox.text_print("The five boxing wizards jump quickly. And this sentence will cause some overflow in the console.")
    tbox.text_print("The five boxing wizards jump quickly.")
    tbox.text_print("The five boxing wizards jump quickly.")
    tbox.text_print("The five boxing wizards jump quickly.")
    tbox.text_print("The five boxing wizards jump quickly.")
    tbox.text_print("The five boxing wizards jump quickly.")
    tbox.text_print("The five boxing wizards jump quickly.")
    tbox.text_print("The five boxing wizards jump quickly.")
    tbox.render()
    
tbox.close()

# this feels like a silly way to do this
# but i dont wanna deal with window stuff and this makes sure the canvas gets run after the textbox
from utils import *

# ========================================
while playing:
    raw_window.fill((0,0,0))

    mouse_pos = pygame.mouse.get_pos()
    adjusted_mouse_pos = adjust_mouse_pos(mouse_pos)

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
            if event.key == K_e :
                # export current canvas to json
                # Python types that map to JSON keys must be str, int, float, bool or None, only need to figure out how to map to one of those types
                # https://stackoverflow.com/questions/56403013/how-to-save-the-dictionary-that-have-tuple-keys
                # ISSUE WITH TUPLE KEYS ^^
                # better: https://stackoverflow.com/questions/12337583/saving-dictionary-whose-keys-are-tuples-with-json-python/12337657#12337657 
                draw_grid = False
                pygame.image.save(subsurf, "export.png")
                push_dict = {str(k): v for (k,v) in canvas.items()}
                with open("map.json", "w") as outfile:
                    json.dump(push_dict, outfile)
                print("MAP EXPORTED")
        if event.type == pygame.MOUSEBUTTONDOWN :
            click_coords = pygame.mouse.get_pos()
            adj_click_coords = adjust_mouse_pos(click_coords)
            # PALETTE CLICK EVENT
            if click_coords[0] > canvas_width * WIN_SCALE :
                if event.button == 1:
                    # turn mouse click coords into tile array index
                    # index = (adj_click_coords[0] - 1) % 3 + 3 * adj_click_coords[1]
                    # TRY SUBTRACTING THE ENTIRE CANVAS WIDTH AND THEN CHECKING INSTEAD

                    index = adj_click_coords[0] - int(canvas_width / TILE_SIZE) + 3 * adj_click_coords[1]
                    print(adj_click_coords, index)
                    if index < len(tile_palette) :
                        curr_brush = tile_palette[index]
                        curr_brush_value = index
                    else :
                        curr_brush = None
            # CANVAS CLICK
            else :
                if event.button == 1 : 
                    painting = True
                if event.button == 3 :
                    erasing = True
        if event.type == pygame.MOUSEBUTTONUP :
            if painting :
                painting = False
                for key in canvas_buffer.keys() :
                    if canvas_buffer[key] != -1:
                        canvas[key] = canvas_buffer[key]
                canvas_buffer = {}
            elif erasing :
                erasing = False
                for key in canvas_buffer.keys() :
                    if key in canvas.keys() :
                        canvas.pop(key)

    if painting and adjusted_mouse_pos not in canvas.keys():
        if curr_brush == None : 
            pass
        else :
            canvas_buffer[adjusted_mouse_pos] = curr_brush_value
    elif erasing :
        canvas_buffer[adjusted_mouse_pos] = -1


    # draw the PALETTE on the side =========================================
    draw_pos = [0,0]
    for i in range(len(tile_palette)) :
        draw_pos[0] = canvas_width + (TILE_SIZE * (i % 3))
        if i % 3 == 0 and i != 0:
            draw_pos[1] += TILE_SIZE
        raw_window.blit(tile_palette[i], pygame.Rect(draw_pos, (TILE_SIZE, TILE_SIZE)))
    # CANVAS ==========================================
    if draw_grid :
        # draw grid lines
        # NOTE: we don't need to adjust for win_scale because we're drawing directly onto the raw surface, which then gets scaled
        for i in range(0, WIN_WIDTH - (TILE_SIZE * 3)) :
            if i % TILE_SIZE == 0:
                pygame.draw.line(raw_window, (255, 0, 0), (i + x_offset, 0), (i + x_offset, WIN_HEIGHT))
        for i in range(0, WIN_HEIGHT) :
            if i % TILE_SIZE == 0 :
                pygame.draw.line(raw_window, (255, 0, 0), (0, i + y_offset), (WIN_WIDTH - (TILE_SIZE * 3), i + y_offset))

        # get mouse position, normalize it to 16x16 grid, account for offset
        
        # print(adjusted_mouse_pos)
        if curr_brush != None :
            raw_window.blit(curr_brush, (adjusted_mouse_pos[0] * TILE_SIZE, adjusted_mouse_pos[1] * TILE_SIZE) )
                
    # RECALL: idx of this dict is the raw tile coords, capping at (9,8)
    for idx in canvas.keys() :
        draw_coords : tuple = tuple(TILE_SIZE * x for x in idx)
        # WIN_SCALE comes later (I think)
        tile = canvas[idx]
        raw_window.blit(tile_palette[tile], draw_coords)
    

    # ========
    scaled_window = pygame.transform.scale(raw_window, display_window.get_size())
    display_window.blit(scaled_window, (0,0))
    pygame.display.update()

    # ========
    clock.tick(60)

pygame.quit()
sys.exit()
