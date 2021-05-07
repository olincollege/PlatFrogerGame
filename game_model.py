import pygame as pg
import random
from settings import *
from spritesheet_view import Spritesheet
from player_model import Player
from platform_model import Platform
from game_view import GameView
from os import path

# House In a Forest by https://opengameart.org/users/horrorpen
# forest by https://opengameart.org/users/syncopika

class GameModel:
    """
    Class in charge of running the game

    Attributes:
        screen: sets the screen size and what is displayed on it
        clock: the game clock- keeps track of how much time has passed
        running: used to start the program loop
        font_name: the font used for text
    """

    def __init__(self):
        """
        Sets initial conditions for the GameModel class
        """

        # Initialize game window.
        pg.init()

        # Initialize sounds & screen
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)

        # Start the game clock.
        self.clock = pg.time.Clock()

        # Start running the program loop (NOT the game loop).
        self.running = True

    def new(self):
        """
        Starts a new game.

        Args:
            view: an instance of a GameView
        """
        self.view = GameView(self)

        #starting score
        self.score = 0
        # Create sprite groups.
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()

        # Define player sprite.
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # Define platform sprites from list.
        for plat in PLATFORM_LIST:
            p = Platform(self.view, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        # load music.
        pg.mixer.music.load(path.join(self.view.snd_dir, 'forest.ogg'))



    def update(self):
        """
        Updates the game loop
        """


        # Update all the sprites based on changes in sprites.py
        self.all_sprites.update()

        # Program player sprites to jump on platforms.
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)

            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit

                if self.player.pos.x < lowest.rect.right and \
                self.player.pos.x > lowest.rect.left:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        #if player reaches top fourth of screen, scroll
        if self.player.rect.top  <= HEIGHT/4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        #spawn new platforms to keep same avg number
        while len(self.platforms) < 6:

            width = random.randrange(0,400)
            p = Platform(self.view, random.randrange(0, WIDTH-width),
                        random.randrange(-60, -30))

            self.platforms.add(p)
            self.all_sprites.add(p)

        # If we die
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False




    def wait_for_key(self):
        """
        Waits for key to be pressed before starting game (start screen)
        """
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def quit_game(self):
        if self.playing:
            self.playing = False
        self.running = False
