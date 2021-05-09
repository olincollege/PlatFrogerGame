"""
Test select methods of the GameModel class.
"""
import pytest
import pygame as pg
from game_model import GameModel
from game_view import GameView
from player_model import Player
from settings import HEIGHT

test_model = GameModel()
test_player = Player(test_model)
test_view = GameView(test_model)

model_cases = [
    # Start running the program loop (NOT the game loop).
    ((test_model.running), (True)),
    # Starting score.
    ((test_model.score), (0)),
    # Define playing.
    ((test_model.playing), (True)),
]

test_model.new()
platform_gen_cases = [
    # Check if correct number of platforms are initialized.
    (test_model.platforms, 5),
    # Check if correct number of total sprites are initialized.
    (test_model.all_sprites, 6),
]

score_screen_cases = [
    # Check if screen scrolls at correct speed if player is within top quarter.
    (HEIGHT + 100, 10),
]

wait_cases = [
    # Check if keyup results in correct flag.
    (pg.event.Event(pg.KEYUP), 1),
    # Check if quit results in correct flag.
    (pg.event.Event(pg.QUIT), 2),
]

quit_case = [
    # Check if game stops running if method is called.
    (False)
]
# Test if display screen is initialzed correctly.
@pytest.mark.parametrize("actual_value,expected_value", model_cases)
def test_display_initialization(actual_value,expected_value):
    """
    Check that the various initial model properties have been initialized to
    the correct values.

    The game running state and playing state should have been initialized to
    True, and the initial score should be zero.

    Args:
        actual_value: A tuple containing the initialized display property.
        expected_value: A tuple containing the expected value for the property.
    """
    assert actual_value == expected_value

# Test if sprite groups are initialized correctly.
@pytest.mark.parametrize("sprite_group,expected_length", platform_gen_cases)
def test_new(sprite_group,expected_length):
    """
    Check if the correct number of sprites have been initialized.

    The length of the sprite group containing the sprites should be as
    expected.

    Args:
        sprite_group: A pygame sprite group object storing the sprites.
        expected_length: An integer for the expected length of the group.
    """
    assert len(sprite_group) == expected_length

# Test if the wait function works correctly.
@pytest.mark.parametrize("key_press,flag", wait_cases)
def test_wait(key_press,flag):
    """
    Check if the key press results in the corresponding exit from the function.

    Either continue without making any changes if key press, otherwise if quit,
    exit the game.

    Args:
        key_press: A pygame event object that simulates a key press.
        flag: An integer signalling the appropriate part of the method that has
            been executed.
    """
    pg.event.post(key_press)
    test_model.wait_for_key()
    assert test_model.flag == flag

# Test if the game is quit correctly.
@pytest.mark.parametrize("is_running", quit_case)
def test_quit(is_running):
    """
    Check if the expected change to the running state of the game is made.

    Args:
        is_running: A boolean indicating if the game is running.
    """
    test_model.running = True
    test_model.quit_game()
    assert test_model.running == is_running
