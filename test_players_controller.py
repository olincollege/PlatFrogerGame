import pytest
import pygame as pg
from game_model import GameModel
from game_view import GameView
from controller import PlayerController
from players_controller import Player
from platform_model import Platform
from settings import *
test_model = GameModel()
test_controller = PlayerController(test_model)
test_view = GameView(test_model)
test_player = Player(test_model)

move_cases = [
    # Test sprite moving Right.
    ("Left", -PLAYER_ACC),
    # Test sprite moving right.
    ("Right", PLAYER_ACC),
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
    # Check if player can jump if irectly on the platform.
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
    # Check if the player is animated correctly when walking to the left.
    (False, True, 2, test_player.game_view.walk_frames_r[1]),
    # Check if the player is animated correctly when walking to the left.
    (False, True, -2, test_player.game_view.walk_frames_l[0]),
    # Check if player is initially sitting towards the left.
    (False, False, 0, test_player.game_view.walk_frames_l[0])
]
# Test if player is initialized correctly.
@pytest.mark.parametrize("attribute,value", initial_player_cases)
def test_player_initialization(attribute, value):
    assert attribute == value

# Test if the player travels in the correct horizontal directions.
@pytest.mark.parametrize("direction,acceleration", move_cases)
def test_move(direction, acceleration):
    test_player.move(direction)
    assert test_player.acc.x == acceleration

# Test if the player jumps only when it is in contact with a platform.
@pytest.mark.parametrize("platform_coordinates, player_coordinates,jumping", jump_cases)
def test_jump(platform_coordinates, player_coordinates,jumping):
    test_player.jumping = False
    test_player.game_model.platforms = pg.sprite.Group()
    p = Platform(test_view, platform_coordinates[0], platform_coordinates[1])
    test_player.game_model.platforms.add(p)
    test_player.rect.bottomleft = player_coordinates
    test_player.jump()
    assert test_player.jumping == jumping

@pytest.mark.parametrize("is_jumping, current_velocity,jump_cut_velocity", jump_cut_cases)
def test_jump_cut(is_jumping, current_velocity,jump_cut_velocity):
    test_player.jumping = is_jumping
    test_player.vel.y = current_velocity
    test_player.jump_cut()
    assert test_player.vel.y == jump_cut_velocity

@pytest.mark.parametrize("current_position, wrapped_position", update_cases)
def test_update(current_position, wrapped_position):
    test_player.pos.x = current_position
    test_player.update()
    assert test_player.pos.x == wrapped_position

@pytest.mark.parametrize("velocity, is_walking", animate_check_walking_cases)
def test_animate_check_walking(velocity, is_walking):
    test_player.vel.x = velocity
    test_player.animate()
    assert test_player.walking == is_walking

@pytest.mark.parametrize("is_jumping, is_walking, velocity, image", animate_check_image_cases)
def test_animate_check_walking(is_jumping, is_walking, velocity, image):
    test_player.jumping = is_jumping
    test_player.walking = is_walking
    test_player.vel.x = velocity
    test_player.last_update = -1000
    test_player.animate()
    print(test_player.last_update)
    assert test_player.image == image
