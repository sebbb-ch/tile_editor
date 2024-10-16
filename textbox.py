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
        self.typed_text_img = []

        self.display_window     = pygame.display.set_mode((win_width * win_scale, win_height * win_scale), 0, 32)
        self.raw_window         = pygame.Surface((win_width, win_height))

    # TODO: WHAT ABOUT RETURN KEY
    def handle_type_event(self, event : pygame.event) :
        # if a valid key was typed, add it to the typed_text_raw field
        char = pygame.key.name(event.key) 
        if not char.isalnum() : return 

        self.typed_text_raw += char
        print(self.typed_text_raw)
        self.text_print(self.typed_text_raw, False, True)
        
        # based on what is in typed text, decide where to render the cursor
        self.cursor.x = len(self.typed_text_raw) * 4

    def __text_to_img(self, text : str) -> list:
        alnum_chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9', ' ', '.']
        special_chars = [' ', '.', ',', '>', '<']
        # create a list of pygame surfaces, each of which is a letter in the surface
        utext = text.upper()
        sentence = []

        if len(text) > self.line_length :
            num_chunks = math.ceil(len(text) / self.line_length)
            chunk_size = self.line_length
            for i in range(num_chunks) :
                chunk = text[i * chunk_size : ((i + 1) * chunk_size)]
                self.__text_to_img(chunk)
        else :
            for c in utext :
                index = alnum_chars.index(c) if c.isalnum() else special_chars.index(c)
                sprite_x = index * 4
                letter_rect = pygame.Rect(sprite_x, 0, 4, 4)
                letter : pygame.Surface = self.alnum_chars.subsurface(letter_rect) if c.isalnum() else self.special_chars.subsurface(letter_rect)
                sentence.append(letter)

        return sentence


    # TODO: nicer textwrapping that doesn't break up words
    # MAYBE TODO: COLOR TEXT OR PARTS OF TEXT
    def text_print(self, text : str, new_line : bool = True, user_text = False) :
        alnum_chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9', ' ', '.']
        special_chars = [' ', '.', ',', '>', '<']
        # create a list of pygame surfaces, each of which is a letter in the surface
        utext = text.upper()
        if new_line : utext = "> " + utext
        sentence = []

        # if text is longer than self.window_size[0] then break it up and call textprint on each chunk, else proceed normally
        if len(text) > self.line_length :
            num_chunks = math.ceil(len(text) / self.line_length)
            chunk_size = self.line_length
            for i in range(num_chunks) :
                chunk = text[i * chunk_size : ((i + 1) * chunk_size)]
                self.text_print(chunk, i == 0)
        else :
            for c in utext :
                index = alnum_chars.index(c) if c.isalnum() else special_chars.index(c)
                sprite_x = index * 4
                letter_rect = pygame.Rect(sprite_x, 0, 4, 4)
                letter : pygame.Surface = self.alnum_chars.subsurface(letter_rect) if c.isalnum() else self.special_chars.subsurface(letter_rect)
                sentence.append(letter)
            
            if user_text :
                print(sentence)
                self.typed_text_img.append(sentence)
            else: 
                self.on_screen_text.append(sentence)

    def render(self) :
        # blit console text
        for i in range(len(self.on_screen_text)) :
            sentence = self.on_screen_text[i]
            spacing_offset = i * 2
            for j in range(len(sentence)) :
                self.raw_window.blit(sentence[j], (j * 4, (i * 4) + spacing_offset))

        # blit cursor + user text
        if self.typed_text_raw != '' :
            for i in range(len(self.typed_text_img[0])) :
                self.raw_window.blit(self.typed_text_img[0][i], (i * 4, ((self.num_lines) * 4) + (2 * self.num_lines) - 1))        
        # TODO: MAKE THE CURSOR BLINK
        pygame.draw.rect(self.raw_window, (255, 0, 0), self.cursor)

        # scale and render
        scaled_window = pygame.transform.scale(self.raw_window, self.display_window.get_size())
        self.display_window.blit(scaled_window, (0,0))
        pygame.display.update()

        # leave ready for next frame
        self.on_screen_text.clear()
        self.raw_window.fill((0,0,0)) # might need to go in outer loop

    def close(self) :
        # closes the textbox window to then open a new one 
        pygame.display.quit()