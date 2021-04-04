import pygame as pg
import game_functions as gf
from settings import Settings
from maze import Maze, GridPoint
from character import Pacman, Blinky, Inky, Pinky, Clyde
from os import path
from timer import Timer

HS_FILE = "HighScores.txt"

# ===================================================================================================
# class Game
# ===================================================================================================
class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("PacMan Portal")
        self.font = pg.font.SysFont(None, 48)
        self.text = self.font.render('500', True, (255,255,255), (0,0,0))
        self.textRect = self.text.get_rect()
        self.textRect.center = (400, 200)

        self.maze = Maze(game=self)

        self.pacman = Pacman(game=self)
        self.ghosts = [Blinky(game=self), Pinky(game=self), Clyde(game=self), Inky(game=self)]
        for ghost in self.ghosts:
            ghost.set_ghosts(self.ghosts)
        self.finished = False
        self.title = True
        self.scorescreendisplay = False
        self.white = (255,255,255)
        self.score = 0
        self.intro = [pg.image.load('images/intro' + str(x) + '.png') for x in range(0, 4)]
        self.timer = Timer(self.intro, wait=200)

    def to_grid(self, index):
        row = index // 11
        offset = index % 11
        ss = self.maze.location(row, offset)
        return ss

    def to_pixel(self, grid): pixels = []

    def intro(self):
        image = self.timer.imagerect()
        self.rect = image.get_rect()
        self.rect.centerx, self.rect.centery = self.pt.x + 5, self.pt.y + 5
        self.screen.blit(image, self.rect)

    def play(self):
        while not self.finished:
            gf.check_events(game=self)
            # self.screen.fill(self.settings.bg_color)
            self.maze.update()
            for ghost in self.ghosts: ghost.update()
            self.pacman.update()
            pg.display.flip()

    def textset(self, text, posx, posy, color):
        self.texttodisplay = self.font.render(text, True, color, (0,0,0))
        self.screen.blit(self.texttodisplay, (posx, posy))

    def title_screen(self):
        while self.title:
            self.screen.fill((0,0,0))
            self.textset('PAC-MAN', 360, 200, self.white)
            self.textset('Press SPACE to begin', 270, 270, self.white)
            self.textset('Press \'H\' to view high scores', 220, 650, self.white)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.title = False
                        self.play()
                    elif event.key == pg.K_h:
                        self.title = False
                        self.scorescreendisplay = True
                        self.score_screen()
            images_intro = [pg.image.load('images/intro' + str(i) + '.png') for i in range(4)]
            timer = Timer(frames=images_intro, wait=50)

    def score_screen(self):
        while self.scorescreendisplay:
            self.screen.fill((0,0,0))
            self.textset('High Scores:', 360, 69, self.white)
            self.textset('Press esc to exit', 320, 760, self.white)
            with open('HighScores.txt', 'r') as f:
                lines = f.readlines()
            numbers = [int(e.strip()) for e in lines]
            numbers.sort(reverse=True)
            for i in range(8):
                self.textset(f'{numbers[i]}', 470, 120+i*80, self.white)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.scorescreendisplay = False
                        self.title = True
                        self.title_screen()

    def savescore(self):
        f = open("HighScores.txt", "a")
        f.write(str(self.score))
        f.write("\n")


def main():
    game = Game()
    game.title_screen()


if __name__ == '__main__': main()

