"""
Controller for the player of the PlatFrogs game.
"""
import pygame as pg
class PlayerController:
    """
    The controller class for controlling the player jumping and game quitting.

    Attributes:
        game: An instance of a GameModel.
    """

    def __init__(self, game):
        """
        Initialize an instance of the game model as an attribute.

        Args:
            game: An instance of a GameModel class.
        """
        self.game = game

    def events(self):
        """
        Check events in the game loop and change attributes based on that.

        (E.g. if the event is QUIT, it quits the game by calling the approiate
        method.)
        """

        # Check each event in list of past, non-executed events.
        for event in pg.event.get():

            # Check for end of program.
            if event.type == pg.QUIT:
                self.game.quit_game()


            # Check for space key for jumping.
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.game.player.jump()

            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.game.player.jump_cut()

    def move_test(self):
        """
        Control movement of player using arrow keys.

        Pressing the left arrow key results in a message to go left, while
        pressing the right arrow key results in a message to go right. Pressing
        both results in the player coming to a halt.
        """
        # Obtain all the current key presses.
        keys = pg.key.get_pressed()

        # Match key presses to corresponding direction messages.
        if keys[pg.K_LEFT]:
            self.game.player.move("Left")

        if keys[pg.K_RIGHT]:
            self.game.player.move("Right")

        if keys[pg.K_LEFT] and keys[pg.K_RIGHT]:
            self.game.player.move("Stop")
