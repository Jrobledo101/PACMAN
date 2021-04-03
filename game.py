import pygame as pg
import game_functions as gf
from settings import Settings
from maze import Maze, GridPoint
from character import Pacman, Blinky, Inky, Pinky, Clyde
from os import path

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

    def to_grid(self, index):
        row = index // 11
        offset = index % 11
        ss = self.maze.location(row, offset)
        return ss

    def to_pixel(self, grid): pixels = []

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
            self.textset('PAC-MAN Portal', 330, 200, self.white)
            self.textset('Press SPACE to begin', 310, 270, self.white)
            self.textset('Press \'H\' to view high scores', 250, 650, self.white)
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

    def score_screen(self):
        while self.scorescreendisplay:
            self.screen.fill(self.settings.bg_color)
            self.textset('High Scores:', 500, 50, self.white)
            self.textset('Press esc to exit', 470, 750, self.white)
            with open('HighScores.txt', 'r') as f:
                lines = f.readlines()
            numbers = [int(e.strip()) for e in lines]
            numbers.sort(reverse=True)
            for i in range(8):
                self.textset(f'{numbers[i]}', 580, 100+i*80, self.white)
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


def main():
    game = Game()
    game.title_screen()


if __name__ == '__main__': main()

