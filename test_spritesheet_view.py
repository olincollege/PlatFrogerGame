"""
Test the get_images method of the Spritesheet class in the spritesheet_view
file.
"""
from os import path
import pytest
import pygame as pg
from spritesheet_view import Spritesheet
from settings import WIDTH, HEIGHT, SPRITESHEET

img_dir = path.join(path.dirname(__file__), "img")

# Define game display.
screen = pg.display.set_mode((WIDTH, HEIGHT))

test_spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

spritesheet_cases = [
    # Check the left walking frames.
    ((83, 346, 64, 50, 1), (64, 50)),
    ((413, 178, 66, 50, 1), (66, 50)),
    # Check the right walking frames.
    ((413, 230, 66, 50, 1), (66, 50)),
    ((149, 346, 64, 50, 1), (64, 50)),
    # Check the right jump frame (scaled).
    ((403, 282, 80, 90, 1.2), (96, 108)),
    # Check for correctly displayed start screen.
    ((1, 1, 465, 175, 0.9), (418, 158)),
    # Check for correctly displayed game over screen.
    ((1, 178, 410, 96), (410, 96)),
    # Check for correctly displayed small platform.
    ((215, 346, 136, 40), (136, 40)),
    # Check for correctly displayed large platform (scaled).
    ((83, 276, 318, 68, 0.8), (254, 54)),
]

# Test if player is initialized correctly.
@pytest.mark.parametrize("specifications,dimensions", spritesheet_cases)
def test_player_initialization(specifications, dimensions):
    """
    Check if the correct sprites are obtained from the spritesheet.

    It is not possible to directly identify a sprite, so check if the output
    sprite image object has the expected width and height (which are unique for
    nearly every sprite image).

    Args:
        specifications: A tuple containing integers representing the
        x-coordinate, y-coordinate, width and height of the desired sprite in
        pixels.
        dimensions: A tuple containing integers representing the expected width
        and height of the (scaled) sprite in pixels.
    """
    image = test_spritesheet.get_image(*specifications)
    assert (image.get_width(), image.get_height()) == dimensions
