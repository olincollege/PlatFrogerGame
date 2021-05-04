import pygame as pg
import random
from settings import *
from sprites import *
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
            self.events()

            # Update the game state to reflect the key presses.
            self.update()

            # Draw (render) the changes.
            self.view.draw()

        pg.mixer.music.fadeout(500)

    def events(self):
        """
        Checks events in the game loop and changes attributes based on that
        (i.e. if the event is QUIT, it quits the game by setting playing = False)
        This is a controller element.
        """
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

            if event.type == pg.KEYUP:
               if event.key == pg.K_SPACE:
                   self.player.jump_cut()

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



class GameView:
    def __init__(self, game_model):
        self.game_model = game_model

        # Define game display.
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        #load spritesheet


        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        """
        Helper function for loading data rom outside file (highscore,
        spritesheet, etc.)
        """

        #load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "img")

        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())

            #if the file is empty, try will give an error
            except:
                self.highscore = 0

        # Load sounds.
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'PacificTreeFrog.wav'))

    def draw(self):
        """
        Displays and draws the game loop. This is a view element.
        """

        # Fill display with empty black screen.
        self.screen.fill(BGCOLOUR)

        # Draw all the sprites.
        self.game_model.all_sprites.draw(self.screen)
        self.screen.blit(self.game_model.player.image, self.game_model.player.rect)

        # Show score
        self.draw_text(str(self.game_model.score), 22, WHITE, WIDTH/2, 15)

        # 'Flip' display to show updated view.
        pg.display.flip()

    def show_start_screen(self):
        """
        Displays the game start screen
        """
        #VIEW
        #Start screen music
        pg.mixer.music.load(path.join(self.snd_dir, 'startEndScreen.ogg'))
        pg.mixer.music.play(loops=-1)

        #Title & background displays
        self.screen.fill(LIGHTGREEN)
        self.image = self.spritesheet.get_image(1, 1, 465, 175, scale=0.9)
        self.image.set_colorkey(BLACK)
        self.title_rect = self.image.get_rect()
        self.title_rect.midtop = (WIDTH/2, HEIGHT/5)
        self.screen.blit(self.image, self.title_rect)

        # Draw start screen text
        self.draw_text("Arrows to move, Space to jump", 22, GREEN,
                        WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play", 22, GREEN, WIDTH/2, HEIGHT*3/4)
        self.draw_text(f"High Score: {self.highscore}", 22, GREEN, WIDTH/2, 15)
        pg.display.flip()
        self.game_model.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        """
        Shows the game over screen.
        """
        #Music
        pg.mixer.music.load(path.join(self.snd_dir, 'startEndScreen.ogg'))
        pg.mixer.music.play(loops=-1)

        #Check that game is running before displaying screen
        if not self.game_model.running:
            return

        #GO title display
        self.screen.fill(LIGHTGREEN)
        self.image = self.spritesheet.get_image(1, 178, 410, 96)
        self.image.set_colorkey(BLACK)
        self.title_rect = self.image.get_rect()
        self.title_rect.midtop = (WIDTH/2, HEIGHT/5)
        self.screen.blit(self.image, self.title_rect)

        # Drawing text
        self.draw_text(f"Score: {self.game_model.score}", 22, GREEN,
                        WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play again", 22, GREEN, WIDTH/2,
                        HEIGHT*3/4)

        #Check for high score
        # If there's a high score, display NEW HIGH SCORE, otherwise
        #return the score and the high score
        if self.game_model.score > self.highscore:
            self.highscore = self.game_model.score
            self.draw_text("NEW HIGH SCORE!", 22, GREEN, WIDTH/2, HEIGHT/2 + 40)

            #save high score in file
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.game_model.score))
        else:
            self.draw_text(f"High Score: {self.highscore}", 22, GREEN,
                            WIDTH/2, HEIGHT/2 +40)

        pg.display.flip()
        self.game_model.wait_for_key()
        pg.mixer.music.fadeout(500)

    def draw_text(self, text, font_size, colour, x, y):
        """
        Helper function used for drawing text.

        Params:
            text: a string representing the text we want to draw
            font_size: the size of the font we want to use
            colour: the colour of the font in RGB
            x: the x position of the text on the screen
            y: the y position of the text on the screen
        """
        font = pg.font.Font(self.font_name, font_size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
