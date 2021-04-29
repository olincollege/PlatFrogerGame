from settings import *
import pygame as pg

# Import vectors from pygame math module.
vec = pg.math.Vector2

class Players(pg.sprite.Sprite):

    def __init__(self, game):
        # Inherit all attributes of pygame Sprite class.
        pg.sprite.Sprite.__init__(self)

        # Pass an instance of the game to the player sprite.
        self.game = game

        # Create a player sprite.
        self.image = pg.Surface((30,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

        # Initialize sprite's position, velocity, and acceleration vectors.
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # Check if player sprite is on a platform.
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:

            # Jump.
            self.vel.y = -PLAYER_JUMP

    def update(self):
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
        if abs(self.vel.x) < 0.01:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # Make sprite wrap around screen.
        if self.pos.x < 0:
            self.pos.x = WIDTH

        if self.pos.x > WIDTH:
            self.pos.x = 0

        # Set sprite position.
        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    """docstring for Platform."""

    def __init__(self, x, y, w, h):
        # Inherit all attributes of pygame Sprite class.
        pg.sprite.Sprite.__init__(self)

        # Create platform sprite.
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        # Set platform positions.
        self.rect.x = x
        self.rect.y = y
