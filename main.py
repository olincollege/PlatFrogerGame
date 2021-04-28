import pygame as pg

from game_model import *

g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()


pg.quit()
