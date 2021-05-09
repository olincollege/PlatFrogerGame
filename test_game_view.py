"""
Test select aspects of the GameView class in the game_view file.
"""
import pytest
import pygame as pg
from game_model import GameModel
from game_view import GameView
from player_model import Player
from settings import TITLE, WIDTH, HEIGHT

test_model = GameModel()
test_view = GameView(test_model)

display_cases = [
    # Check if display has been initialized.
    ((pg.display.get_init()), (True)),
    # Check if display has the correct caption.
    (pg.display.get_caption(), (TITLE, TITLE)),
    # Check if display is of the correct size.
    (pg.display.get_window_size(), (WIDTH, HEIGHT)),
    # Check that only one display is initialized.
    ((pg.display.get_num_displays()), (1)),
]

highscore_cases = [
    # Check if highscore updates if current score is more than highscore.
    (100, 400, 400),
    # Check if highscore updates if current score is less than highscore.
    (100, 80, 100),
    # Check if highscore updates if current score is equal to highscore.
    (100, 100, 100),
    # Check if highscore updates if highscore is zero.
    (0, 100, 100),
    # Check if highscore updates if highscore and current score is zero.
    (0, 0, 0),
]


frame_cases = [
    # Check if correct image is chosen for right jump frame.
    (test_view.jump_r, (108, 96)),
    # Check if correct image is chosen for left jump frame.
    (test_view.jump_l, (108, 96)),
    # Check if correct image is chosen for first left walking frame.
    (test_view.walk_frames_l[0], (64, 50)),
    # Check if correct image is chosen for second left walking frame.
    (test_view.walk_frames_l[1], (66, 50)),
    # Check if correct image is chosen for first right walking frame.
    (test_view.walk_frames_r[0], (66, 50)),
    # Check if correct image is chosen for second right walking frame.
    (test_view.walk_frames_r[1], (64, 50)),
]
# Test if display screen is initialzed correctly.
@pytest.mark.parametrize("actual_value,expected_value", display_cases)
def test_display_initialization(actual_value,expected_value):
    """
    Check that the various initial display properties have been initialized to
    the correct values.

    The display should have been initialized, the game window should be the
    correct size, the caption should be correct, and there should be only one
    display running.

    Args:
        actual_value: A tuple containing the initialized display property.
        expected_value: A tuple containing the expected value for the property.
    """
    assert actual_value == expected_value

# Test if highscore is calculated correctly.
@pytest.mark.parametrize("previous_highscore,current_score,new_highscore", highscore_cases)
def test_highscore(previous_highscore,current_score,new_highscore):
    """
    Check if the highscore is calculated approporiately when displaying the
    game over screen for a particular game instance.

    If the score at the end of a game is greater than the highscore, the score
    becomes the new highscore. Otherwise, the highscore stays the same.

    Args:
        previous_highscore: An integer containing the highscore resulting from
        playing all the games up to that point in one instance.
        current_score: An integer containing the score resulting from playing
        the current game.
        new_highscore: The updated highscore after the current game.
    """
    # Initialize highscore and current score.
    test_view.highscore = previous_highscore
    test_view.game_model.score = current_score

    # Simulate a key press required to exit game-over screen.
    newevent = pg.event.Event(pg.KEYUP) # create the event
    pg.event.post(newevent) # add the event to the queue

    # Check if method updates highscore correctly.
    test_view.show_go_screen()
    assert test_view.highscore == new_highscore

# Test if correct image is drawn for each frame.
@pytest.mark.parametrize("image,dimensions", frame_cases)
def test_load_images(image, dimensions):
    """
    Check if the correct image is chosen for the given position.

    It is not possible to directly identify a sprite, so check if the output
    sprite image object has the expected width and height (which are unique for
    nearly every sprite image). Test for the sprite positions of jumping and
    walking either left or right.

    Args:
        image: A sprite image object that is chosen based on the desired frame.
        dimensions: A tuple containing integers representing the expected width
        and height of the sprite in pixels.
    """
    assert (image.get_width(), image.get_height()) == dimensions
