import pygame as pg

from game_model import GameModel
from game_view import GameView
from controller import PlayerController
g_controller = PlayerController
g_model = GameModel()
g_view = GameView(g_model)

g_view.show_start_screen()

while g_model.running:
    g_model.new(g_view)
    g_view.show_go_screen()


pg.quit()
