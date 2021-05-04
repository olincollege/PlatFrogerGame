from settings import *
import pygame as pg
from random import choice

class Platform(pg.sprite.Sprite):
    """
    Platform model class that inherits from the pygame Sprite class.


    Attributes:
    game: an instance of a Game
    images: a list of images that can be displayed for the platforms (in this
    case, lillypads)
    image: a random choice of either the larger or smaller lillypad which will
    be displayed
    rect: the interactable area of the lillypad platforms
    """

    def __init__(self, game_view, x, y):
        """
        Sets initial conditions for Platform class

        Args:
            game_view: an instance of a GameView
            x: the x positon of the platform
            y: the y position of the platform
        """
        self.game_view = game_view
        # Inherit all attributes of pygame Sprite class.
        pg.sprite.Sprite.__init__(self)

        # Create platform sprite.
        self.images = [self.game_view.spritesheet.get_image(215, 346, 136, 40),
                        self.game_view.spritesheet.get_image(83, 276, 318, 68, scale=0.8)]

        self.image = choice(self.images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        # Set platform positions.
        self.rect.x = x
        self.rect.y = y
