"""
Create the PlatFrogs game and manage and track the game state.
"""
from os import path
import random
import pygame as pg
from settings import HEIGHT, WIDTH, FPS, PLATFORM_LIST
from player_model import Player
from platform_model import Platform
from game_view import GameView


# House In a Forest by https://opengameart.org/users/horrorpen
# forest by https://opengameart.org/users/syncopika

class GameModel:
    """
    Class in charge of running the game.

    Attributes:
        clock: An integer containing the time that has passed since this object
            was created.
        running: A boolean that determines if the game is running.
        view: An instance of a GameView class.
        score: An integer storing the score of a particular game.
        all_sprites: A sprite group that contains all the sprites (player and
            platform) in the game.
        platforms: A sprite group that contains all current platform sprites in
            the game.
        player: An instance of a Player class.
        playing: A boolean determining whether a current game is being played.
        flag: An integer that is used for unit testing the wait_for_key method.
    """

    def __init__(self):
        """
        Set initial conditions for the GameModel class.
        """

        # Start the game clock.
        self.clock = pg.time.Clock()

        # Start running the program loop (NOT the game loop).
        self.running = True

        # Initialize an instance of a game view.
        self.view = GameView(self)

        # Starting score.
        self.score = 0

        # Create sprite groups.
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()

        # Define player sprite.
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # Define playing.
        self.playing = True

        # Flag for unit testing wait_for_key method.
        self.flag = 0

    def new(self):
        """
        Start a new game.

        Initialize score to 0, load the player and platform sprites, and start
        playing the game music.
        """

        # Reinitialize starting score.
        self.score = 0

        # Create sprite groups.
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()

        # Define player sprite.
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # Define platform sprites from list.
        for plat in PLATFORM_LIST:
            platform = Platform(self.view, *plat)
            self.all_sprites.add(platform)
            self.platforms.add(platform)

        # Load music.
        pg.mixer.music.load(path.join(self.view.snd_dir, 'forest.ogg'))
        pg.mixer.music.play(loops=-1)


    def update(self):
        """
        Update the game loop.

        Update the sprites based on changes, program player sprite to jump on
        platforms, scroll the screen, randomly generate new platforms and check
        when the player sprite falls of the screen and dies.

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

                # Enable player sprite to rest on a platform.
                if self.player.pos.x < lowest.rect.right and \
                self.player.pos.x > lowest.rect.left:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # If player reaches top fourth of screen, scroll.
        if self.player.rect.top  <= HEIGHT/4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)

                # Delete platforms that go off the screen.
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # Randomly spawn new platforms to keep same average number.
        while len(self.platforms) < 6:

            width = random.randrange(0,400)
            platform = Platform(self.view, random.randrange(0, WIDTH-width),
                        random.randrange(-60, -30))

            self.platforms.add(platform)
            self.all_sprites.add(platform)

        # Check if player sprite falls of screen, and end the game accordingly.
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

    def wait_for_key(self):
        """
        Wait for key to be pressed before starting game.

        Stay in the method until any key is pressed, or the player quits the
        game.
        """
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                # Check for player quitting game.
                if event.type == pg.QUIT:
                    self.flag = 2
                    waiting = False
                    self.running = False

                # Check for key press.
                if event.type == pg.KEYUP:
                    self.flag = 1
                    waiting = False

    def quit_game(self):
        """
        Quit the game when called.
        """
        if self.playing:
            self.playing = False
        self.running = False
