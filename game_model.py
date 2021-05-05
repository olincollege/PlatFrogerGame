import pygame as pg
import random
from settings import *
from spritesheet_view import *
from players_controller import *
from platform_model import *
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

    def __init__(self, controller):
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

        # Define the controller.
        self.controller  = controller

    def new(self, view):
        """
        Starts a new game.

        Args:
            view: an instance of a GameView
        """
        self.view = view

        #starting score
        self.score = 0
        # Create sprite groups.
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()

        # Define player sprite.
        self.player = Players(self, self.view)
        self.all_sprites.add(self.player)

        # Define platform sprites from list.
        for plat in PLATFORM_LIST:
            p = Platform(self.view, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        # load music. We could do different music themes, maybe creepy forest
        # after a certain score with background change.
        pg.mixer.music.load(path.join(self.view.snd_dir, 'forest.ogg'))
        self.run()

    def run(self):
        """
        Runs the game loop
        """
        pg.mixer.music.play(loops=-1)
        # Start running the game loop.
        self.playing = True

        # Game loop.
        while self.playing:
            # Set delay for fixed time gap for each iteration of game loop (in
            # this case, 60 iterations (frames) per second).
            self.clock.tick(FPS)

            # Input and process user's key presses.
            self.controller.events()

            # Update the game state to reflect the key presses.
            self.update()

            # Draw (render) the changes.
            self.view.draw()

        pg.mixer.music.fadeout(500)



    def update(self):
        """
        Updates the game loop
        """
        #CONTROLLER

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
            # print("while loop")
            # #check for collisions
            # #try 10 attempts and if its not possible, dont try again until screen scrolls
            #
            # for plat in self.platforms:
            #     print("for loop")
            #     if p.rect.midright[0] > plat.rect.midleft[0] - 5:
            #         print("a")
            #         platform_is_valid = False
            #         break
            #     elif p.rect.midtop[1] > plat.rect.midbottom[1] - 5:
            #         print("b")
            #         platform_is_valid = False
            #         break
            #     # elif p.rect.midleft[0] > plat.rect.midright[0]:
            #     #     print("c")
            #     #     platform_is_valid = False
            #     #     break
            #     # elif p.rect.midbottom[1] < plat.rect.midtop[1]:
            #     #     print("d")
            #     #     platform_is_valid = False
            #     #     break
            #     else:
            #         platform_is_valid = True
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
