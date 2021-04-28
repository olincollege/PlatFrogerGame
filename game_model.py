import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # Initialize game window.
        pg.init()

        # Initialize sounds.
        pg.mixer.init()

        # Define game display.
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)

        # Start the game clock.
        self.clock = pg.time.Clock()

        # Start running the program loop (NOT the game loop).
        self.running = True

    def new(self):
        # Start a new game.

        # Create sprite groups.
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        # Define player sprite.
        self.player = Players(self)
        self.all_sprites.add(self.player)

        # Define platform sprites from list.
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Start running the game loop.
        self.playing = True

        # Game loop.
        while self.playing:
            # Set delay for fixed time gap for each iteration of game loop (in
            # this case, 60 iterations (frames) per second).
            self.clock.tick(FPS)

            # Input and process user's key presses.
            self.events()

            # Update the game state to reflect the key presses.
            self.update()

            # Draw (render) the changes.
            self.draw()

    def events(self):
        # Events in game loop.
        #CONTROLLER

        # Check each event in list of past, non-executed events.
        for event in pg.event.get():

            # Check for end of program.
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            # Check for space key for jumping.
            if event.type == pg.KEYDOWN:
               if event.key == pg.K_SPACE:
                   self.player.jump()

    def update(self):
        # Update Game Loop.
        #CONTROLLER

        # Update all the sprites based on changes in sprites.py
        self.all_sprites.update()

        # Program player sprites to jump on platforms.
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)

            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0


    def draw(self):
        # Draw game loop.
        #VIEW

        # Fill display with empty black screen.
        self.screen.fill(BLACK)

        # Draw all the sprites.
        self.all_sprites.draw(self.screen)

        # 'Flip' display to show updated sprites.
        pg.display.flip()

    def show_start_screen(self):
        # Show game start screen.
        #VIEW
        pass

    def show_go_screen(self):
        # Show game over screen.
        #VIEW
        pass
