import pygame as pg

from game_model import GameModel
from game_view import GameView
from controller import PlayerController
from settings import FPS
g_model = GameModel()
g_controller = PlayerController(g_model)
g_view = GameView(g_model)

g_view.show_start_screen()

while g_model.running:
    g_model.new()
    # Start running the game loop.
    g_model.playing = True

    # Game loop.
    while g_model.playing:
        # Set delay for fixed time gap for each iteration of game loop (in
        # this case, 60 iterations (frames) per second).
        g_model.clock.tick(FPS)

        # Input and process user's key presses.
        g_controller.events()

        # Input and process left and right key presses.
        # g_controller.movement()

        # Update the game state to reflect the key presses.
        g_model.update()

        # Draw (render) the changes.
        g_view.draw()

    pg.mixer.music.fadeout(500)
    g_view.show_go_screen()


pg.quit()
