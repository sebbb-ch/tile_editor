import pygame, sys, random, os, math, json
clock = pygame.time.Clock()
from pygame.locals import *
# rethink imports - im doing all of this because i want the class/file to be 
# copy pasteable 

# https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame

# chars are 4x4

# QUESTIONS : do I want this to be in its own separate window? or do I want it to exist within a main window?
# por que no los dos
    # but for this I definitely want it in its own window before the program runs
class Textbox :
    def __init__(self, line_length : int, num_lines : int) :
        win_scale   = 6
        char_size   = 4
        # NOTE: i'm cheating here to be able to add my '> ' characters in the text
        # it's gonna look funcky because the first line will be the only 32 char one
        # but it'll be a TODO - refer to @text_print to try and fix
        win_width   = (line_length + 2) * char_size
        # y-lines of size 4 + CLI line + 2 px of spacing for every line
        win_height  = ((num_lines + 1) * char_size) + (2 * num_lines)

        # (number of chars, number of lines)
        self.line_length    = line_length
        self.num_lines      = num_lines
        self.alnum_chars    = pygame.image.load('./alphabet.png')
        self.special_chars  = pygame.image.load('./special_characters.png')
        # a list of all sentences (lists) on screen at the moment - should be limited by user input
        self.on_screen_text = []
        self.cursor         = pygame.Rect(0, (win_height - char_size - 1), char_size, char_size)
        self.typed_text_raw = ''

        self.display_window     = pygame.display.set_mode((win_width * win_scale, win_height * win_scale), 0, 32)
        self.raw_window         = pygame.Surface((win_width, win_height))

    # pulled out into it's own function so that we can pop at the end and make space
    def __update_onscreen_text(self, images : list) -> None :
        self.on_screen_text.append(images)
        if len(self.on_screen_text) > self.num_lines :
            # we're gonna try just popping the last one but this might need to
            # be a for loop for all extra ones
            self.on_screen_text.pop(0)

    def __text_to_img(self, text : str, rgb : tuple = None) -> list:
        def color_surface(surface : pygame.Surface, rgb : tuple = None) :
            arr = pygame.surfarray.pixels3d(surface)
            arr[:,:,0] = rgb[0]
            arr[:,:,1] = rgb[1]
            arr[:,:,2] = rgb[2]
        
        alnum_chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9', ' ', '.']
        special_chars = [' ', '.', ',', '>', '<']
        # create a list of pygame surfaces, each of which is a letter in the surface
        utext = text.upper()
        sentence = []

        for c in utext :
            index = alnum_chars.index(c) if c.isalnum() else special_chars.index(c)
            letter_rect = pygame.Rect(index * 4, 0, 4, 4)
            letter : pygame.Surface = self.alnum_chars.subsurface(letter_rect) if c.isalnum() else self.special_chars.subsurface(letter_rect)
            if rgb != None :
                # consolidate these lines
                letter.convert_alpha()
                colored_letter = letter.copy()
                color_surface(colored_letter, rgb)
                sentence.append(colored_letter)
            else :
                sentence.append(letter)

        return sentence

    # TODO: WHAT ABOUT RETURN KEY
    def handle_type_event(self, event : pygame.event) :
        # if a valid key was typed, add it to the typed_text_raw field
        char = pygame.key.name(event.key) 
        if not char.isalnum() : return 

        if char == 'space' :
            self.typed_text_raw += ' '
        elif char == 'backspace':
            if len(self.typed_text_raw) > 0 :
                self.typed_text_raw = self.typed_text_raw[:-1]
        elif char == 'escape':
            pass
        elif char == 'return':
            # NOTE THIS DOESNT WORK BECAUSE OF HOW WE'RE RENDERING
            self.text_print(self.typed_text_raw)
            self.typed_text_raw = ''
        else :
            self.typed_text_raw += char
        
        # based on what is in typed text, decide where to render the cursor
        self.cursor.x = len(self.typed_text_raw) * 4

    # TODO: nicer textwrapping that doesn't break up words
    # MAYBE TODO: COLOR TEXT OR PARTS OF TEXT
    # TODO: add the >  in the new line of text
    def text_print(self, text : str, color : tuple = None) :
        if len(text) > self.line_length :
            num_chunks = math.ceil(len(text) / self.line_length)
            chunk_size = self.line_length
            for i in range(num_chunks) :
                chunk = text[i * chunk_size : ((i + 1) * chunk_size)]
                self.text_print(chunk, i == 0)
        else :
            imgs = self.__text_to_img(text)
            # self.on_screen_text.append(imgs)
            self.__update_onscreen_text(imgs)

    def render(self) :
        self.raw_window.fill((0,0,0)) # might need to go in outer loop

        # blit console text
        for i in range(len(self.on_screen_text)) :
            sentence = self.on_screen_text[i]
            spacing_offset = i * 2
            for j in range(len(sentence)) :
                self.raw_window.blit(sentence[j], (j * 4, (i * 4) + spacing_offset))

        # blit cursor + user text
        if self.typed_text_raw != '' :
            user_sentence = self.__text_to_img(self.typed_text_raw)
            for i in range(len(user_sentence)) :
                self.raw_window.blit(user_sentence[i], (i * 4, ((self.num_lines) * 4) + (2 * self.num_lines) - 1))

        # TODO: MAKE THE CURSOR BLINK
        pygame.draw.rect(self.raw_window, (255, 0, 0), self.cursor)

        # scale and render
        scaled_window = pygame.transform.scale(self.raw_window, self.display_window.get_size())
        self.display_window.blit(scaled_window, (0,0))
        pygame.display.update()



    def close(self) :
        # closes the textbox window to then open a new one 
        pygame.display.quit()