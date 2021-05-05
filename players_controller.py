from settings import *
import pygame as pg

# Import vectors from pygame math module.
vec = pg.math.Vector2

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

    def __init__(self, game_model, game_view):
        """
        Initializes the Player class
        """

        # Inherit all attributes of pygame Sprite class.
        pg.sprite.Sprite.__init__(self)

        # Pass an instance of the game to the player sprite.
        self.game_model = game_model
        self.game_view = game_view

        #animation attributes
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0

        # Create a player sprite.
        self.image = self.game_view.spritesheet.get_image(83, 346, 64, 50)
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
        self.walk_frames_l = [self.game_view.spritesheet.get_image(83, 346, 64, 50),
                            self.game_view.spritesheet.get_image(413, 178, 66, 50)]

        self.walk_frames_r = [self.game_view.spritesheet.get_image(413, 230, 66, 50),
                            self.game_view.spritesheet.get_image(149, 346, 64, 50)]
        self.jump_r = self.game_view.spritesheet.get_image(403, 282, 80, 90, scale=1.2)
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
        hits = pg.sprite.spritecollide(self, self.game_model.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game_view.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def jump_cut(self):
        """
        Makes the minimum jump velocity -3 for a more natural movement
        """
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self, direction):
        """
        Updates the player in the game loop
        """
        self.animate()

        # Include gravity in the game.
        self.acc = vec(0, PLAYER_GRAVITY)

        if direction == "Left":
            self.acc.x = -PLAYER_ACC
        if direction == "Right":
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