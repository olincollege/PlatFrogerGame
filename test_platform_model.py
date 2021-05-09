"""
Test the initialization of the Platform model class.
"""
import pytest
from platform_model import Platform
from game_model import GameModel
from game_view import GameView

test_model = GameModel()
test_view = GameView(test_model)
X_COORD = 100
Y_COORD = 100



platform_cases = [
    # Check if correct small platform is initialzed.
    (0, (236, 140)),
    # Check if correct large platform is initialzed.
    (1, (354, 154)),
]

# Test if correct image is drawn for each frame.
@pytest.mark.parametrize("index,coordinates", platform_cases)
def test_platforms(index,coordinates):
    """
    Check if both the small and large platforms are initialized correctly.

    It is not possible to directly identify a sprite, so check the coordinates
    of the bottom-right of the platform sprite rectangle which essentially has
    the coordinates of (x + width, y + height), hence by fixing the expected
    coordinates of placement, check if correct platform is initialized in the
    correct position.

    Args:
        index: An integer containing the list index of the platform image in
            the list of all (in this case two) platform images.
        coordinates: A tuple containing integers representing the coordinates
            of the bottomright of the platform sprite rectangle.
    """
    # Keep initializing instances of Platform until the desired platform is
    # obtained (the type of platform is chosen randomly so this can't be
    # explicitly selected).
    test_platform = Platform(test_view, X_COORD, Y_COORD)
    while test_platform.image != test_platform.images[index]:
        test_platform = Platform(test_view, X_COORD, Y_COORD)

    # Check if the coordinates of the bottom-right point match as expected.
    assert (test_platform.rect.bottomright) == coordinates
