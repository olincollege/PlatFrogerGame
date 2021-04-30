from settings import *
import pygame as pg
from random import choice

# Import vectors from pygame math module.
vec = pg.math.Vector2
class Spritesheet:
    #utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height, scale=1):
        # grab an image out of a larger spreadsheet

        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        image = pg.transform.scale(image, (round(width * scale), round(height * scale)))
        return image

class Players(pg.sprite.Sprite):

    def __init__(self, game):
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
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        #look left, prep left, jump left, look right, prep right, jump right
        self.walk_frames_l = [self.game.spritesheet.get_image(83, 346, 64, 50),
                            self.game.spritesheet.get_image(413, 178, 66, 50)]

        self.walk_frames_r = [self.game.spritesheet.get_image(413, 230, 66, 50),
                            self.game.spritesheet.get_image(149, 346, 64, 50)]
        self.jump_r = self.game.spritesheet.get_image(403, 282, 80, 90)
        self.jump_l = self.game.spritesheet.get_image(1, 282, 80, 90)

        self.jump_l.set_colorkey(BLACK)
        self.jump_r.set_colorkey(BLACK)

        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)

        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
                    # self.game.spritesheet.get_image(1, 282, 80, 90),
                    # self.game.spritesheet.get_image(149, 346, 64, 50),


    def jump(self):
        # Check if player sprite is on a platform.
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
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
        if abs(self.vel.x) < 0.02:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # Make sprite wrap around screen.
        if self.pos.x < 0:
            self.pos.x = WIDTH

        if self.pos.x > WIDTH:
            self.pos.x = 0

        # Set sprite position.
        self.rect.midbottom = self.pos

    def animate(self):
        """
        Animates characters
        """
        #walking conditions
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # Walking animation
        if self.walking:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x<0:
                    self.image = self.walk_frames_l[self.current_frame]
                else:
                    self.image = self.walk_frames_r[self.current_frame]


class Platform(pg.sprite.Sprite):
    """docstring for Platform."""

    def __init__(self, game, x, y):
        self.game = game
        # Inherit all attributes of pygame Sprite class.
        pg.sprite.Sprite.__init__(self)

        # Create platform sprite.
        self.images = [self.game.spritesheet.get_image(215, 346, 136, 40),
                        self.game.spritesheet.get_image(83, 276, 318, 68)]

        self.image = choice(self.images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        # Set platform positions.
        self.rect.x = x
        self.rect.y = y
