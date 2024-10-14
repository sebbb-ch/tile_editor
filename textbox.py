import pygame, sys, random, os, math, json
clock = pygame.time.Clock()
from pygame.locals import *
# rethink imports - im doing all of this because i want the class/file to be 
# copy pasteable 

class Textbox :
    def __init__(self, window_size : tuple) :
        # (number of chars, number of lines)
        self.window_size = window_size
        self.raw_window = None
        self.charset = 

    def print(self, text : str) :
