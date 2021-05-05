import pygame as pg
import players_controller
class PlayerController:
    """docstring for PlayerController."""

    def __init__(self, player, game):
        self.player = player
        self.game = game


    def movement(self):
        # Move player left and right.
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT and pg.K_RIGHT]:
            self.player.update("Stop")

        elif keys[pg.K_LEFT]:
            self.player.update("Left")

        elif keys[pg.K_RIGHT]:
            self.player.update("Right")


    def events(self):
        """
        Checks events in the game loop and changes attributes based on that
        (i.e. if the event is QUIT, it quits the game by setting playing = False)
        This is a controller element.
        """
        # Events in game loop.
        #CONTROLLER

        # Check each event in list of past, non-executed events.
        for event in pg.event.get():

            # Check for end of program.
            if event.type == pg.QUIT:
                self.game.quit_game()


            # Check for space key for jumping.
            if event.type == pg.KEYDOWN:
               if event.key == pg.K_SPACE:
                   self.player.jump()

            if event.type == pg.KEYUP:
               if event.key == pg.K_SPACE:
                   self.player.jump_cut()
