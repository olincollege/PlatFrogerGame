"""
Create a player for the PlatFrogs game.
"""
import pygame as pg
from settings import (BLACK,
                      HEIGHT,
                      WIDTH,
                      PLAYER_JUMP,
                      PLAYER_ACC,
                      PLAYER_GRAVITY,
                      PLAYER_FRICTION,)

from game_view import GameView
from controller import PlayerController
# Import vectors from pygame math module.
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    """
    The frog player class used throughout the game.

    Attributes:
        game: an instance of a Game
        walking: boolean set to True if the player is walking, set to False
        otherwise
        jumping: boolean set to True if the player is jumping, otherwise False
        current_frame: the current frame of animation
        last_update: the latest update of the player (used in animation)
        image: the image of the character (what will be displayed)
        rect: the interactable dimensions of the player image (rectangle)
        rect.center: position of the center of the player sprite
        pos: a vector with the x and y positions of the player sprite
        vel: a vector with the x and y velocities of the player sprite
        acc: a vector with the x and y accelerations of the player sprite
        flag_unit_test: an integer indicating whether a player enters certain
            methods, used for unit testing.
    """

    def __init__(self, game_model):
        """
        Initialize the Player class.

        Args:
            game_model: An instance of a game model.
        """

        # Inherit all attributes of pygame Sprite class.
        pg.sprite.Sprite.__init__(self)

        # Pass an instance of the game to the player sprite.
        self.game_model = game_model

        # Initialize an instance of the game view.
        self.game_view =  GameView(game_model)

        # Animation attributes.
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0

        # Create a player sprite.
        self.image = self.game_view.spritesheet.get_image(83, 346, 64, 50)
        self.image.set_colorkey(BLACK)
        # self.game_view.load_images()
        self.rect = self.image.get_rect()

        # Initialize sprite's position, velocity, and acceleration vectors.
        self.rect.center = (100, HEIGHT - 50)
        self.pos = vec(100, HEIGHT - 50)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        # Initialize a flag used for unit testing the controller.
        self.flag_unit_test = 0

        # Initialize controller instance.
        self.controller = PlayerController(game_model)

    def jump(self):
        """
        Execute necessary actions for jumping movement of player (jump sound,
        moving, etc.)
        """
        # Change value of flag for unit test.
        self.flag_unit_test = 1
        # Check if player sprite is on a platform.
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game_model.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game_view.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def jump_cut(self):
        """
        Allow the player to vary jump height by doing shorter hops if the jump
        key is pressed and released quickly.
        """
        # Change value of flag for unit test.
        self.flag_unit_test = 2

        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def move(self, direction):
        """
        Inform left and right movement of the player sprite based on the input
        message.

        The player's motion is controlled by changing the player's acceleration
        in order to give the player a more realistic motion when moving left
        and right.

        Args:
            direction: A string that is either "Stop", "Left", or "Right" that
            informs the player sprite of the direction it is supposed to
            accelerate.
        """
        if direction == "Stop":
            self.flag_unit_test = 3
            self.acc.x = 0
        if direction == "Left":
            self.flag_unit_test = 4
            self.acc.x = -PLAYER_ACC
        if direction == "Right":
            self.flag_unit_test = 5
            self.acc.x = PLAYER_ACC

    def update(self):
        """
        Update the player in the game loop.

        Define the 'laws of physics' that the player sprite must follow, make
        the sprite wrap around the screen when necessary, and update its
        position accordingly.
        """
        # Run the animation for the player sprite.
        self.animate()

        # Include gravity in the game.
        self.acc = vec(0, PLAYER_GRAVITY)

        # Move the player left and right.
        self.controller.move_test()

        # Instill friction into movement.
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # Update velocity from acceleration.
        self.vel += self.acc

        # Set low velocities to zero.
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # Make sprite wrap around screen.
        if self.pos.x < 0  - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        if self.pos.x > WIDTH  + self.rect.width / 2:
            self.pos.x = 0  - self.rect.width / 2

        # Set sprite position.
        self.rect.midbottom = self.pos

    def animate(self):
        """
        Animate player sprite.

        Define what the sprite will look like in different states, i.e. if it
        is jumping or walking, and which direction it is pointing in.
        """
        # Initialize timer (to be used later).
        now = pg.time.get_ticks()

        # Decide if player is walking.
        if abs(self.vel.x) >= 0.5:
            self.walking = True
        else:
            self.walking = False

        # Jumping animation.
        if self.jumping:

            # Choose left or right jumping frame depending on the player's
            # horizontal velocity.
            if self.vel.x < 0:
                self.image = self.game_view.jump_l
            else:
                self.image = self.game_view.jump_r

        # Walking animation.
        elif self.walking:
            # Alternate between two walking animation frames every 100
            # milliseconds to produce a realistic walking motion.
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) \
                % len(self.game_view.walk_frames_l)
                # Choose left or right walking frame based on the player's
                # horizontal velocity.
                if self.vel.x < 0:
                    self.image = \
                    self.game_view.walk_frames_l[self.current_frame]
                else:
                    self.image = \
                    self.game_view.walk_frames_r[self.current_frame]

        # Ensure that jumping and walking sprites are in the same direction.
        else:
            if self.image == self.game_view.jump_l:
                self.image = self.game_view.walk_frames_l[self.current_frame]
            elif self.image == self.game_view.jump_r:
                self.image = self.game_view.walk_frames_r[self.current_frame]
