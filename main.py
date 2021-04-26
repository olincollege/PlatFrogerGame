import pygame as pg
import random
from settings import *

class Game:
    def __init__(self):
        #initialize game window, etc
        self.running = True
        pass

    def new(self):
        #start a new game
        pass

    def run(self):
        #game loop
        pass

    def update(self):
        #Game Loop - Update
        #CONTROLLER
        pass

    def events(self):
        #game loop- events
        #CONTROLLER
        pass

    def draw(self):
        #game loop- draw
        #VIEW
        pass

    def show_start_screen(self):
        #game start screen
        #VIEW
        pass

    def show_go_screen(self):
        #game over screen
        #VIEW
        pass

g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()


pg.quit()
