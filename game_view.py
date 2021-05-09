"""
View class for displaying the PlatFrogs game.
"""
from os import path
import pygame as pg
from settings import (WIDTH,
                      HEIGHT,
                      TITLE,
                      FONT_NAME,
                      SPRITESHEET,
                      HS_FILE,
                      BGCOLOUR,
                      WHITE,
                      LIGHTGREEN,
                      GREEN,
                      BLACK,)
from spritesheet_view import Spritesheet


class GameView:
    """
    A view of the PlatFrogs Game.

    Attributes:
        game_model: An instance of a GameModel class.
        screen: A pygame display surface that creates a display window for the
            game.
        font_name: A pygame module for rendering the text fonts.
        dir: A path to the current directory of the file.
        spritesheet: An instance of a Spritesheet class.
        highscore: An integer containing the highest score across all games run
            in this instance.
        snd_dir: A path to the folder containing the sound files.
        jump_sound: A pygame sound object that plays the sound when the player
            sprite jumps.
        image: A pygame Surface object containing the image for a particular
            sprite.
        title_rect: A pygame rectangle containing the title.
        walk_frames_l: A list of two pygame Surface objects containing the
            image for the player sprite walking to the left.
        walk_frames_r: A list of two pygame Surface objects containing the
            image for the player sprite walking to the right.
        jump_l: A pygame Surface object containing the image for the player
            sprite jumping to the left.
        jump_r: A pygame Surface object containing the image for the player
            sprite jumping to the right.
    """
    def __init__(self, game_model):
        """
        Initialize the GameView class.

        Args:
            game_model: An instance of a GameModel.
        """
        # Initialize game window.
        pg.init()

        # Initialize sounds & screen
        pg.mixer.init()

        # Pass an instance of the game model.
        self.game_model = game_model

        # Define game display.
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.font_name = pg.font.match_font(FONT_NAME)

        # Specify path to current directory.
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "img")
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        #load high score
        with open(path.join(self.dir, HS_FILE), 'w') as file_object:
            try:
                self.highscore = int(file_object.read())

            #if the file is empty, try will give an error
            except IOError:
                self.highscore = 0

        # Load sounds.
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'PacificTreeFrog.wav'))
        self.image = self.spritesheet.get_image(1, 1, 465, 175, scale=0.9)

        # Extract two images each for each of the walking frames.
        self.walk_frames_l = [self.spritesheet.get_image(83, 346, 64, 50),
                            self.spritesheet.get_image(413, 178, 66, 50)]
        self.walk_frames_r = [self.spritesheet.get_image(413, 230, 66, 50),
                              self.spritesheet.get_image(149, 346, 64, 50)]

        # Extract image for right jump frame and reorient in correct direction.
        self.jump_r = self.spritesheet.get_image(403, 282, 80, 90, scale=1.2)
        self.jump_r = pg.transform.flip(self.jump_r, False, False)
        self.jump_r = pg.transform.rotate(self.jump_r, 90)

        # Define the image for the left jump frame as a reflection of the right
        # jump frame.
        self.jump_l = pg.transform.flip(self.jump_r, True, False)

        # Ensure the image rectangles for all the frames are transparent.
        self.jump_l.set_colorkey(BLACK)
        self.jump_r.set_colorkey(BLACK)

        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)

        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)

    def draw(self):
        """
        Display and draw the game loop.

        Fill the display with the background color, draw all the sprite objects
        on the screen, and flip the display to show the changes.
        """

        # Fill display with empty light-blue screen.
        self.screen.fill(BGCOLOUR)

        # Draw all the sprites.
        self.game_model.all_sprites.draw(self.screen)
        self.screen.blit(self.game_model.player.image, self.game_model.player.rect)

        # Show score
        self.draw_text(str(self.game_model.score), 22, WHITE, (WIDTH/2, 15))

        # 'Flip' display to show updated view.
        pg.display.flip()

    def show_start_screen(self):
        """
        Display the game start screen.

        Play the start screen music, the game title, and draw the instructions
        to play as well as the current highscore (initialized to zero).
        """
        # Start screen music.
        pg.mixer.music.load(path.join(self.snd_dir, 'startEndScreen.ogg'))
        pg.mixer.music.play(loops=-1)

        # Title & background displays.
        self.screen.fill(LIGHTGREEN)
        # Display title.
        self.image = self.spritesheet.get_image(1, 1, 465, 175, scale=0.9)
        self.image.set_colorkey(BLACK)
        title_rect = self.image.get_rect()
        title_rect.midtop = (WIDTH/2, HEIGHT/5)
        self.screen.blit(self.image, title_rect)

        # Draw start screen text.
        self.draw_text("Arrows to move, Space to jump", 22, GREEN,
                        (WIDTH/2, HEIGHT/2))
        self.draw_text("Press any key to play", 22, GREEN, (WIDTH/2, HEIGHT*3/4))
        self.draw_text(f"High Score: {self.highscore}", 22, GREEN, (WIDTH/2, 15))
        pg.display.flip()

        # Exit start screen and begin game once key is pressed.
        self.game_model.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        """
        Display the game over screen.

        Play the game over screen music and display the game over title, the
        updated high score as well a prompt to play again.
        """
        # Game over screen music.
        pg.mixer.music.load(path.join(self.snd_dir, 'startEndScreen.ogg'))
        pg.mixer.music.play(loops=-1)

        # Check that game is running before displaying screen.
        if not self.game_model.running:
            return

        # Display Game Over title.
        self.screen.fill(LIGHTGREEN)
        self.image = self.spritesheet.get_image(1, 178, 410, 96)
        self.image.set_colorkey(BLACK)
        title_rect = self.image.get_rect()
        title_rect.midtop = (WIDTH/2, HEIGHT/5)
        self.screen.blit(self.image, title_rect)

        # Display current score and prompt to play again.
        self.draw_text(f"Score: {self.game_model.score}", 22, GREEN,
                        (WIDTH/2, HEIGHT/2))
        self.draw_text("Press any key to play again", 22, GREEN, (WIDTH/2,
                        HEIGHT*3/4))

        # Check for high score
        # If there's a high score, display NEW HIGH SCORE, otherwise
        # return the score and the high score.
        if self.game_model.score > self.highscore:
            self.highscore = self.game_model.score
            self.draw_text("NEW HIGH SCORE!", 22, GREEN, (WIDTH/2, HEIGHT/2 + 40))

            #save high score in file
            with open(path.join(self.dir, HS_FILE), 'w') as file_object:
                file_object.write(str(self.game_model.score))
        else:
            self.draw_text(f"High Score: {self.highscore}", 22, GREEN,
                            (WIDTH/2, HEIGHT/2 +40))

        pg.display.flip()

        # Exit game over screen and restart game once key is pressed.
        self.game_model.wait_for_key()
        pg.mixer.music.fadeout(500)

    def draw_text(self, text, font_size, colour, coords):
        """
        Helper function used for drawing text.

        Args:
            text: A string representing the text to draw.
            font_size: An integer containing the size of the font to use.
            colour: A tuple representing the colour of the font in RGB.
            coords: A tuple containing the coordinates of the position of the
                text on the screen.
        """
        # Set font.
        font = pg.font.Font(self.font_name, font_size)

        # Define a surface with the specified text, colour, and font.
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()

        # Position and display the text.
        text_rect.midtop = coords
        self.screen.blit(text_surface, text_rect)
