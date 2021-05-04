import pygame as pg

from game_model import *
from game_view import *

g_model = GameModel()
g_view = GameView(g_model)

g_view.show_start_screen()

while g_model.running:
    g_model.new(g_view)
    g_view.show_go_screen()


pg.quit()
