from raycasting import *
from player import *
from settings import *
from map import *

import pygame as pg
import sys
import math
from math import pi as PI

## TODO:
# Scale down textures for distant objects
# Add transparent textures

## Ideas:
# Turn off background refresh for trippy effect

# Player Variables
RAD = 20  # Player size (radius)
FOV = PI / 2  # Player field of view (radians)
# X0, Y0 = RESx // 2, RESy // 2
# THETA0 = PI * 1.4  # Player starting view direction (radians from north CW)
X0, Y0, THETA0 = 1.5, 1.5, 0

class Game:

    # Setup
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 50)  # Sets the window location on screen
        pg.init()
        self.sky = pg.image.load("textures\skyxp.png")
        self.screen = pg.display.set_mode(RES, flags=pg.SCALED, vsync=1)
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
        # Draw the sky
        angle = self.p.theta
        offset = math.ceil(angle * 896 / PI)
        width = self.sky.get_width()
        if offset + RESx < width:
            self.screen.blit(self.sky, (0,0), (offset, 0, RESx, RESy/2))
        else:
            self.sky.get_width() - offset
            self.screen.blit(self.sky, (0, 0), (offset, 0, width - offset, RESy / 2))
            self.screen.blit(self.sky, (width - offset, 0), (0, 0, RESx + offset - width, RESy / 2))

        if self.m.drawmap:
            drawMap2D(self.screen, self.m)
            self.p.display()

        castRays(self.screen, self.p, self.m)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    self.m.drawMap()
                    if self.m.drawmap:
                        self.screen = pg.display.set_mode((RESx*2, RESy))
                    else:
                        self.screen = pg.display.set_mode(RES)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            #print(self.p.x, self.p.y, self.p.theta)


if __name__ == '__main__':
    g = Game()
    g.run()
