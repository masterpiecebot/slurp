from raycasting import *
from player import *
from settings import *
from map import *

import pygame as pg
import sys
import math
from math import pi as PI

# Player Variables
RAD = 20  # Player size (radius)
FOV = PI / 2  # Player field of view (radians)
# X0, Y0 = RESx // 2, RESy // 2
# THETA0 = PI * 1.4  # Player starting view direction (radians from north CW)
X0, Y0, THETA0 = 375.818106502971, 403.6225436374409, 0.3950444078461259

class Game:

    # Setup
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.m = Map()
        self.p = Player(self, X0, Y0, THETA0)  # Player container

    # Main functions
    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        self.p.move()

    def draw(self):
        self.screen.fill('black')
        if DISPLAYMAP:
            drawMap2D(self.screen, self.m)
            self.p.display()
            pg.draw.rect(self.screen, "black", pg.Rect(0, 0, RESx, RESy))
        else:
            pg.draw.rect(self.screen, "black", pg.Rect(0, 0, RES[0], RES[1]))
        castRays(self.screen, self.p, self.m)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    pass

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            #print(self.p.x, self.p.y, self.p.theta)


if __name__ == '__main__':
    g = Game()
    g.run()
