from settings import *
import pygame as pg
import math
from math import pi as PI
from math import tau as TAU

# Unchanging Variables:
radius = .2             # Player size (radius)
rotSpd = 0.04           # Rotational speed (radians per frame)
pAccel = 0.0003         # Player acceleration (speeding up from a stop, slowing down)
color = (255, 255, 0)   # Player color


class Player():

    def __init__(self, game, x, y, dir_x, dir_y):
        self.game = game  # Reference to game attributes, mainly screen

        self.dof = 16  # Depth of field (view distance)
        self.fov = 0.66  # Field of view (radians)

        self.x, self.y = x, y  # Player x, y location
        # Normalize direction vector, set player direction looking
        hyp = math.hypot(dir_x, dir_y)
        self.dirX = dir_x / hyp  # Player vision vector
        self.dirY = dir_y / hyp
        self.planeX = -dir_y * self.fov  # Camera plane vector
        self.planeY = dir_x * self.fov
        self.theta = math.atan(dir_x / (dir_y + 0.00001))  # TODO: Remove

        self.pFrameVX, self.pFrameVY = 0, 0  # Velocity in player frame of reference
        self.vx, self.vy = 0, 0  # Player component velocities (x,y)
        self.vmax = 20 / 5000  # Player max speed

    def display(self):
        # Line that points in direction of looking
        # pg.draw.line(self.game.screen, 'yellow', (self.x + OFFSET2D, self.y),
        #              (self.x + OFFSET2D + RESx * math.sin(self.theta),
        #               self.y - RESy * math.cos(self.theta)),2)
        t = math.sqrt(2) * radius
        gridW, gridH = self.game.m.gridW, self.game.m.gridH
        x = self.x * self.game.m.gridW
        y = self.y * self.game.m.gridH
        rw = radius * self.game.m.gridW
        rh = radius * self.game.m.gridW
        points = [[x + OFFSET2D + rw * math.sin(self.theta), y - rh * math.cos(self.theta)],
                  [x + OFFSET2D + rw * math.sin(self.theta + 4 * PI / 5), y - rh * math.cos(self.theta + 4 * PI / 5)],
                  [x + OFFSET2D + rw * math.sin(self.theta + 6 * PI / 5), y - rh * math.cos(self.theta + 6 * PI / 5)]]
        pg.draw.polygon(self.game.screen, 'yellow', points)
        # Draw velocity vector (exaggerated by a factor of 10)
        pg.draw.line(self.game.screen, "red", (x + OFFSET2D, y), (x + OFFSET2D + self.vx * 10, y - self.vy * 10))
        # Draw direction vector
        pg.draw.line(self.game.screen, "yellow", (self.x * self.game.m.gridW + OFFSET2D, self.y * self.game.m.gridH),
                     ((self.x + self.dirX) * self.game.m.gridW + OFFSET2D, (self.y + self.dirY) * self.game.m.gridH))
        # Draw camera plane
        pg.draw.line(self.game.screen, "yellow",
                     ((self.x + self.dirX - self.planeX) * self.game.m.gridW + OFFSET2D,
                      (self.y + self.dirY - self.planeY) * self.game.m.gridH),
                     ((self.x + self.dirX + self.planeX) * self.game.m.gridW + OFFSET2D,
                      (self.y + self.dirY + self.planeY) * self.game.m.gridH))

    def move(self):
        # Get movement keys pressed
        keys = pg.key.get_pressed()
        # UP    = keys[pg.K_w] or keys[pg.K_UP]
        # DOWN  = keys[pg.K_s] or keys[pg.K_DOWN]
        # LEFT  = keys[pg.K_a]
        # RIGHT = keys[pg.K_d]
        # TURNR = keys[pg.K_RIGHT]
        # TURNL = keys[pg.K_LEFT]
        FORWARD = int(keys[pg.K_w] or keys[pg.K_UP]) - int(keys[pg.K_s] or keys[pg.K_DOWN])
        STRAFE = int(keys[pg.K_d]) - int(keys[pg.K_a])
        TURN = int(keys[pg.K_RIGHT]) - int(keys[pg.K_LEFT])
        # Forward / Backwards
        self.x += self.dirX * self.vmax * self.game.delta_time * FORWARD
        self.y += self.dirY * self.vmax * self.game.delta_time * FORWARD
        # Strafing
        self.x += -self.dirY * self.vmax * self.game.delta_time * STRAFE
        self.y += self.dirX * self.vmax * self.game.delta_time * STRAFE
        # Rotating | I change both at the same time because they're co-dependent
        sin = math.sin(rotSpd * TURN)
        cos = math.cos(rotSpd * TURN)
        self.dirX, self.dirY = (self.dirX * cos - self.dirY * sin,
                                self.dirX * sin + self.dirY * cos)
        # Rotating camera plane
        self.planeX, self.planeY = (self.planeX * cos - self.planeY * sin,
                                    self.planeX * sin + self.planeY * cos)

        self.theta = (-math.atan2(self.dirX, self.dirY) + PI)  # TODO: Remove

    def move2(self):
        # Get movement keys pressed
        keys = pg.key.get_pressed()
        UP = keys[pg.K_w]
        DOWN = keys[pg.K_s]
        LEFT = keys[pg.K_a]
        RIGHT = keys[pg.K_d]
        TURNR = keys[pg.K_RIGHT]
        TURNL = keys[pg.K_LEFT]

        # Update frame of reference velocities based on acceleration
        if not RIGHT and not LEFT:
            if self.pFrameVX > 0:
                self.pFrameVX = constrain(self.pFrameVX - pAccel, 0, self.vmax)
            else:
                self.pFrameVX = constrain(self.pFrameVX + pAccel, -self.vmax, 0)
        else:  # If no movement key is pressed, slow down
            self.pFrameVX += pAccel * (int(LEFT) - int(RIGHT))
            self.pFrameVX = constrain(self.pFrameVX, -self.vmax, self.vmax)
        if not UP and not DOWN:
            if self.pFrameVY > 0:
                self.pFrameVY = constrain(self.pFrameVY - pAccel, 0, self.vmax)
            else:
                self.pFrameVY = constrain(self.pFrameVY + pAccel, -self.vmax, 0)
        else:  # If no movement key is pressed, slow down
            self.pFrameVY += pAccel * (int(UP) - int(DOWN))
            self.pFrameVY = constrain(self.pFrameVY, -self.vmax, self.vmax)

        sin = math.sin(self.theta)
        cos = math.cos(self.theta)

        # Calculate component velocities for forward/backward movement plus strafing
        self.vx = (self.pFrameVY * sin - self.pFrameVX * cos) * self.game.delta_time
        self.vy = (self.pFrameVY * cos + self.pFrameVX * sin) * self.game.delta_time
        # pg.draw.line(self.game.screen, "yellow", (self.x, self.y), (self.x + self.vx*1000, self.y))
        # pg.draw.line(self.game.screen, "yellow", (self.x, self.y), (self.x, self.y + self.vy * 1000))

        # Update x, y, and rotation, check for collision
        if self.vx > 0:
            nextx = self.x + self.vx + radius
        else:
            nextx = self.x + self.vx - radius
        if self.vy < 0:
            nexty = self.y - self.vy + radius
        else:
            nexty = self.y - self.vy - radius
        # TODO: check map collission
        self.x = constrain(self.x + self.vx, radius, RESx - radius)
        self.y = constrain(self.y - self.vy, radius, RESx - radius)

        # Update Rotation
        self.theta = self.theta + rotSpd * (int(TURNR) - int(TURNL))
        # Make sure theta stays between 0 and 2PI
        self.theta %= TAU
