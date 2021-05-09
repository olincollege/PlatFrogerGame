"""
Test the PlayerController class to respond appropriately to key inputs.
"""
import pytest
import pygame as pg
from pynput.keyboard import Key, Controller
from game_model import GameModel
from controller import PlayerController

test_model = GameModel()
test_model.new()
test_model.playing = False
test_player_controller = PlayerController(test_model)

jumping_cases = [
    # Check if keydown on the spacebar results in a jump.
    (pg.event.Event(pg.KEYDOWN, key=pg.K_SPACE), 1),
    # Check if keyup on the spacebar results in a jump cut.
    (pg.event.Event(pg.KEYUP, key=pg.K_SPACE), 2),
]

quit_case = [
    # Check if game is quit.
    (pg.event.Event(pg.QUIT), False)
]

move_cases = [
    # Check if keydown on the spacebar results in a jump.
    ("left", 4),
    # Check
]
# Test if jumping occurs correctly.
@pytest.mark.parametrize("pygame_event, flag_value", jumping_cases)
def test_jumping_cases(pygame_event, flag_value):
    """
    Check if the key press to jump and jump cut results in the correct action.

    If the spacebar is pressed down, call the jump method in the Player class,
    and if the the spacebar is released, call the jump_cut method in the class.

    Args:
        pygame_event: A pygame event simulating the key press of the spacebar.
        flag_value: An integer indicating which Player method has been called.
    """
    # Simulate key press.
    pg.event.post(pygame_event) # add the event to the queue

    # Check if correct method is called.
    test_player_controller.events()
    assert test_player_controller.game.player.flag_unit_test == flag_value

# Test if quitting occurs correctly.
@pytest.mark.parametrize("pygame_event, is_running", quit_case)
def test_quit_case(pygame_event, is_running):
    """
    Check if clicking the 'X' to quit the game results in the correct action.

    If the button is pressed, call the quit_game method in the GameModel class.
    This method sets running to False, which stops the game from running.

    Args:
        pygame_event: A pygame event simulating the button click to quit.
        is_running: A boolean indicating if the game is running.
    """
    # Simulate click to exit game.
    pg.event.post(pygame_event) # add the event to the queue

    # Check if game stops running.
    test_player_controller.events()
    assert test_player_controller.game.running == is_running
