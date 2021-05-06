import pygame as pg

# Import vectors from pygame math module.
vec = pg.math.Vector2

class Spritesheet:
    """
    Utility class for loading and parsing spritesheets

    Attributes:
        spritesheet: the spritesheet we will be using in our game
    """
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height, scale=1):
        """
        Grab an image out of a larger spreadsheet

        Args:
            x: int, the x position of the smaller image
            y: int, the y position of the smaller image
            width: int, the width of the image
            height: int, the height of the image
            scale: an optional argument to scale the image. This should be set
            to an int and will be the scale factor by which the size of the
            image will be multiplied
        """

        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        image = pg.transform.scale(image, (round(width * scale), round(height * scale)))
        return image
