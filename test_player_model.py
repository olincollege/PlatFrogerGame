"""
Test all the class methods in the Player class in the player_model file.
"""
import pytest
import pygame as pg
from game_model import GameModel
from game_view import GameView
from controller import PlayerController
from player_model import Player
from platform_model import Platform
from settings import WIDTH, HEIGHT, PLAYER_ACC
test_model = GameModel()
test_controller = PlayerController(test_model)
test_view = GameView(test_model)
test_player = Player(test_model)

move_cases = [
    # Test sprite moving Right.
    ("Left", -PLAYER_ACC),
    # Test sprite moving right.
    ("Right", PLAYER_ACC),
    # Test sprite that has stopped (both keys pressed).
    ("Stop", 0)
]

initial_player_cases = [
    # Check that player is not walking when game is initialized.
    (test_player.walking, False),
    # Check that player is not jumping when game is initialized.
    (test_player.jumping, False),
    # Check that player is initialized at x correct position.
    (test_player.pos.x, 100),
    # Check that player is initialized at y correct position.
    (test_player.pos.y, HEIGHT - 50),
    # Check that the player is not moving horizontally.
    (test_player.vel.x, 0),
    # Check that the player is not moving vertically.
    (test_player.vel.y, 0),
    # Check that the player initially has zero horizontal acceleration.
    (test_player.acc.x, 0),
    # Check that the player initially has zero vertical acceleration.
    (test_player.acc.y, 0),
]

jump_cases = [
    # Check if player can jump if directly on the platform.
    ((50, 100), (50, 100), True),
    # Check if player can jump if slightly above the platform.
    ((100, 200), (100, 150), False),
    # Check if player can jump if on the platform but in a  different position.
    ((100, 200), (150, 200), True),
    # Check if player can jump if it significantly horizontally displaced.
    ((100, 200), (20, 200), False),
    # Check if player can jump if it below the platform.
    ((50, 100), (50, 300), False),
]

jump_cut_cases = [
    # Check if player can jump cut if in the air and fast enough.
    (True, -20, -3),
    # Check if player can jump cut if in the air and too slow.
    (True, -1, -1),
    # Check if player can jump cut if not in the air (so vertical velocity is zero).
    (False, 0, 0),
    # Check if player can jump cut if in the air and descending
    (False, 20, 20),

]

update_cases = [
    # Check if player wraps to the left if outside the screen to the right.
    (600, 0 - test_player.rect.width / 2),
    # Check if player wraps to the right if outside the screen to the left.
    (-100, WIDTH + test_player.rect.width / 2),
    # Check if player wraps horizontally if inside the screen.
    (100, 100),
]

animate_check_walking_cases = [
    # Check if player is walking if it is above the threshold horizontal speed.
    (2, True),
    # Check if player is walking in opposite direction.
    (-2, True),
    # Check if player is walking if at rest.
    (0, False),
    # Check if player is walking if it is below the threshold horizontal speed.
    (0.4, False),
]


animate_check_image_cases = [
    # Check if the player is animated correctly when jumping to the right.
    (True, False, 2, test_player.game_view.jump_r),
    # Check if the player is animated correctly when jumping to the left.
    (True, False, -2, test_player.game_view.jump_l),
    # Check if the player is animated correctly when walking to the right.
    (False, True, 2, test_player.game_view.walk_frames_r[0]),
    # Check if the player is animated correctly when walking to the left.
    (False, True, -2, test_player.game_view.walk_frames_l[1]),
    # Check if player is initially sitting towards the left.
    (False, False, 0, test_player.game_view.walk_frames_l[1])
]
# Test if player is initialized correctly.
@pytest.mark.parametrize("attribute,value", initial_player_cases)
def test_player_initialization(attribute, value):
    """
    Check that the player attributes have been initialized correctly.

    The player should have an initial velocity and acceleration of zero and be
    placed in a specified position. It should also neither be jumping nor
    walking.

    Args:
        attribute: The public attribute of the Player class to be initialized.
        value: The value this attribute is supposed to be initialized to.
    """
    assert attribute == value

# Test if the player travels in the correct horizontal directions.
@pytest.mark.parametrize("direction,acceleration", move_cases)
def test_move(direction, acceleration):
    """
    Check that the player moves with the desired acceleration according to key
    presses.

    The player either moves left, right, or stops if both keys are pressed.

    Args:
        direction: A string containing the direction the player is to move
        based on key presses (either "Left", "Right", or "Stop").
        acceleration: An integer containing the expected acceleration of the
        player sprite for the specified direction.
    """
    # Start moving the player in the specified direction.
    test_player.move(direction)
    # Check for correct acceleration.
    assert test_player.acc.x == acceleration

# Test if the player jumps only when it is in contact with a platform.
@pytest.mark.parametrize("platform_coordinates, player_coordinates,jumping", jump_cases)
def test_jump(platform_coordinates, player_coordinates,jumping):
    """
    Check if a player can jump only in valid situations, i.e. when the player
    and platform are in contact.

    Place the player and platform in various positions, and determine which
    configurations should be valid and which ones shouldn't.

    Args:
        platform_coordinates: A tuple containing the coordinates of the top-
        left of the platform sprite.
        player_coordinates: A tuple containing the coordinates of the bottom-
        left of the player sprite.
        jumping: A boolean that indicates whether or not a player is currently
        jumping.
    """
    # Initialize the player to be not jumping.
    test_player.jumping = False

    # Define a platform sprite at the specified coordinates.
    test_player.game_model.platforms = pg.sprite.Group()
    platform = Platform(test_view, *platform_coordinates)
    test_player.game_model.platforms.add(platform)

    # Place the player at the specified coordinates.
    test_player.rect.bottomleft = player_coordinates

    # Check if the jump method correctly determines if the player is allowed to
    # jump in that particular situation.
    test_player.jump()
    assert test_player.jumping == jumping

@pytest.mark.parametrize("is_jumping, current_velocity,jump_cut_velocity", jump_cut_cases)
def test_jump_cut(is_jumping, current_velocity,jump_cut_velocity):
    """
    Check if the player can jump cut at specific stages of the jump.

    The ability to jump cut is determined by whether the player is jumping and
    whether they are just taking off. In these cases, releasing the spacebar
    quickly results in a shorter hop as opposed to a full jump.

    Args:
        is_jumping: A boolean that determines whether a player is currently
        jumping or not.
        current_velocity: An integer containing the initial vertical velocity
        of the player.
        jump_cut_velocity: An integer containing the vertical velocity of the
        player after the jump cut.
    """
    # Initialize jump to desired state.
    test_player.jumping = is_jumping
    test_player.vel.y = current_velocity

    # Check if the method executes a jump cut only in valid situations.
    test_player.jump_cut()
    assert test_player.vel.y == jump_cut_velocity

@pytest.mark.parametrize("current_position, wrapped_position", update_cases)
def test_update(current_position, wrapped_position):
    """
    Check if the player sprite wraps around the screen horizontally if it goes
    off the screen.

    Args:
        current_position: An integer containing the initial x position of the
        player.
        wrapped_position: An integer containing the x position of the player
        after it has been wrapped around the screen if required.
    """
    # Initialize the player's current position.
    test_player.pos.x = current_position

    # Check if it wraps around appropriately when the player state is updated.
    test_player.update()
    assert test_player.pos.x == wrapped_position

@pytest.mark.parametrize("velocity, is_walking", animate_check_walking_cases)
def test_animate_check_walking(velocity, is_walking):
    """
    Check if the player is walking based on its horizontal velocity.

    If the player's speed is less than a given threshold, the velocity rounds
    down to zero and the player is no longer walking.
    Args:
        velocity: An integer containing the velocity of the player sprite in
        the x direction.
        is_walking: A boolean determining if the player is currently walking.
    """
    # Set the player's current velocity.
    test_player.vel.x = velocity

    # Check if the player walking is determined correctly.
    test_player.animate()
    assert test_player.walking == is_walking

@pytest.mark.parametrize("is_jumping, is_walking, velocity, image", animate_check_image_cases)
def test_animate_check_image(is_jumping, is_walking, velocity, image):
    """
    Check if the player sprite is displayed as it is supposed to be considering
    its current state.

    E.g.- if jumping and the sprite has a positive velocity, an image of the
    sprite jumping in the right direction should be displayed on the screen.

    Args:
        is_jumping: A boolean determining if the player is currently jumping.
        is_walking: A boolean determining if the player is currently walking.
        velocity: An integer containing the velocity of the player sprite in
        the x direction.
        image: A pygame Surface object that is an attribute of the player class
        and contains the specific animation to be shown on screen.
    """
    # Set the player sprite's state as desired.
    test_player.jumping = is_jumping
    test_player.walking = is_walking
    test_player.vel.x = velocity

    # Set this to a large negative value to enter walking animation.
    test_player.last_update = -1000

    # Check if the animate method displays the correct frames.
    test_player.animate()
    assert test_player.image == image
