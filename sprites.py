from settings import *
import pygame as pg
from random import choice

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

class Players(pg.sprite.Sprite):
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
    """

    def __init__(self, game):
        """
        Initializes the Player class
        """

        # Inherit all attributes of pygame Sprite class.
        pg.sprite.Sprite.__init__(self)

        # Pass an instance of the game to the player sprite.
        self.game = game

        #animation attributes
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0

        # Create a player sprite.
        self.image = self.game.spritesheet.get_image(83, 346, 64, 50)
        self.image.set_colorkey(BLACK)
        self.load_images()

        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

        # Initialize sprite's position, velocity, and acceleration vectors.
        self.rect.center = (100, HEIGHT - 50)
        self.pos = vec(100, HEIGHT - 50)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        """
        Loads images from the spritesheet for display
        """
        #look left, prep left, jump left, look right, prep right, jump right
        self.walk_frames_l = [self.game.spritesheet.get_image(83, 346, 64, 50),
                            self.game.spritesheet.get_image(413, 178, 66, 50)]

        self.walk_frames_r = [self.game.spritesheet.get_image(413, 230, 66, 50),
                            self.game.spritesheet.get_image(149, 346, 64, 50)]
        self.jump_r = self.game.spritesheet.get_image(403, 282, 80, 90, scale=1.2)
        self.jump_r = pg.transform.flip(self.jump_r, False, False)
        self.jump_r = pg.transform.rotate(self.jump_r, 90)

        self.jump_l = pg.transform.flip(self.jump_r, True, False)


        self.jump_l.set_colorkey(BLACK)
        self.jump_r.set_colorkey(BLACK)

        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)

        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
                    # self.game.spritesheet.get_image(1, 282, 80, 90),
                    # self.game.spritesheet.get_image(149, 346, 64, 50),


    def jump(self):
        """
        Executes necessary actions for jumping movement of player (jump sound,
        moving, etc.)
        """
        # Check if player sprite is on a platform.
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def jump_cut(self):
        """
        Makes the minimum jump velocity -3 for a more natural movement
        """
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        """
        Updates the player in the game loop
        """
        self.animate()

        # Include gravity in the game.
        self.acc = vec(0, PLAYER_GRAVITY)

        # Move player left and right.
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC

        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

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
        Animates characters
        """
        #walking conditions
        now = pg.time.get_ticks()
        if abs(self.vel.x) >= 0.5:
            self.walking = True
        else:
            self.walking = False

        # Jumping animation
        if self.jumping:
            bottom = self.rect.bottom
            if self.vel.x<0:
                self.image = self.jump_l
            else:
                self.image = self.jump_r

        #Walking animation
        elif self.walking:
                if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                    bottom = self.rect.bottom
                    if self.vel.x<0:
                        self.image = self.walk_frames_l[self.current_frame]
                    else:
                        self.image = self.walk_frames_r[self.current_frame]

        #Make sure jumping and walking sprites are in the right direction
        else:
            if self.vel.x<0:
                self.image = self.walk_frames_l[self.current_frame]
            elif self.vel.x>0:
                self.image = self.walk_frames_r[self.current_frame]
            elif self.image == self.jump_l:
                self.image = self.walk_frames_l[self.current_frame]
            elif self.image == self.jump_r:
                self.image = self.walk_frames_r[self.current_frame]


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

    def __init__(self, game, x, y):
        """
        Sets initial conditions for Platform class

        Args:
            game: an instance of a game
            x: the x positon of the platform
            y: the y position of the platform
        """
        self.game = game
        # Inherit all attributes of pygame Sprite class.
        pg.sprite.Sprite.__init__(self)

        # Create platform sprite.
        self.images = [self.game.spritesheet.get_image(215, 346, 136, 40),
                        self.game.spritesheet.get_image(83, 276, 318, 68, scale=0.8)]

        self.image = choice(self.images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        # Set platform positions.
        self.rect.x = x
        self.rect.y = y
