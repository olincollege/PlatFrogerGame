"""
Create an instance of a Platform sprite.
"""
from random import choice
import pygame as pg
from settings import BLACK


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

    def __init__(self, game_view, x_coord, y_coord):
        """
        Set initial conditions for Platform class.

        Grab platform images from spritesheet, randomly choose a platform, and
        create pygame sprite of Platform at specified position.

        Args:
            game_view: an instance of a GameView
            x_coord: the x positon of the platform
            y_coord: the y position of the platform
        """
        # Create an instance of a game view.
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
        self.rect.x = x_coord
        self.rect.y = y_coord
