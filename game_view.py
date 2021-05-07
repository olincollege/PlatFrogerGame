import pygame as pg
import random
from settings import *
from spritesheet_view import *
from players_controller import *
from platform_model import *
from os import path

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

    def load_images(self):
        """
        Loads images from the spritesheet for display
        """
        #look left, prep left, jump left, look right, prep right, jump right
        self.walk_frames_l = [self.spritesheet.get_image(83, 346, 64, 50),
                            self.spritesheet.get_image(413, 178, 66, 50)]
        self.walk_frames_r = [self.spritesheet.get_image(413, 230, 66, 50),
                              self.spritesheet.get_image(149, 346, 64, 50)]
        self.jump_r = self.spritesheet.get_image(403, 282, 80, 90, scale=1.2)
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
