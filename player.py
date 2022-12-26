from settings import *
import pygame as pg
import math
from math import pi as PI
from math import tau as TAU

# Unchanging Variables:
radius = 20            # Player size (radius)
rotSpd = 0.04          # Rotational speed (radians per frame)
pAccel = 0.02           # Player acceleration (speeding up from a stop, slowing down)
color = (255, 255, 0)  # Player color

class Player():

    def __init__(self, game, x, y, theta):
        self.game = game            # Reference to game attributes, mainly screen
        
        self.dof = 16               # Depth of field (view distance)
        self.fov = PI/2             # Field of view (radians)
        self.vmax = 35/100          # Player max speed

        self.x, self.y = x, y       # Player x, y location
        self.theta = theta          # Player rotation

        self.pFrameVX, self.pFrameVY = 0, 0     # Velocity in player frame of reference
        self.vx, self.vy = 0, 0                 # Player component velocities (x,y)

    def display(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x + OFFSET2D, self.y),
                     (self.x + OFFSET2D + RESx * math.sin(self.theta),
                      self.y - RESy * math.cos(self.theta)),2)
        pg.draw.circle(self.game.screen, 'green', (self.x + OFFSET2D, self.y), radius)

        pg.draw.line(self.game.screen, "yellow", (self.x + OFFSET2D, self.y), (self.x + OFFSET2D + self.vx * 10, self.y - self.vy*10))

    def move2(self):
        keys = pg.key.get_pressed()
        UP    = keys[pg.K_w]
        DOWN  = keys[pg.K_s]
        LEFT  = keys[pg.K_a]
        RIGHT = keys[pg.K_d]
        TURNR = keys[pg.K_RIGHT]
        TURNL = keys[pg.K_LEFT]
        
        sin = math.sin(self.theta)
        cos = math.cos(self.theta)

        dx, dy = 0,0
        speed = 1 * self.game.delta_time
        sps = speed * sin
        spc = speed * cos

        dx, dy = 0, 0
        if UP:
            dx += spc
            dy += sps
        if DOWN:
            dx -= spc
            dy -= sps
        if LEFT:
            dx += sps
            dy -= spc
        if RIGHT:
            dx -= sps
            dy += spc

        self.x += dx
        self.y += dy

        if TURNL:
            self.theta -= rotSpd * self.game.delta_time
        if TURNR:
            self.theta += rotSpd * self.game.delta_time
        self.theta %= TAU

    def move(self):
        # Get movement keys pressed
        keys = pg.key.get_pressed()
        UP    = keys[pg.K_w]
        DOWN  = keys[pg.K_s]
        LEFT  = keys[pg.K_a]
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
            self.pFrameVY += pAccel * (int(UP)-int(DOWN))
            self.pFrameVY = constrain(self.pFrameVY, -self.vmax, self.vmax)
        
        sin = math.sin(self.theta)
        cos = math.cos(self.theta)

        # Calculate component velocities for forward/backward movement plus strafing
        self.vx = (self.pFrameVY * sin - self.pFrameVX * cos) * self.game.delta_time
        self.vy = (self.pFrameVY * cos + self.pFrameVX * sin) * self.game.delta_time
        #pg.draw.line(self.game.screen, "yellow", (self.x, self.y), (self.x + self.vx*1000, self.y))
        #pg.draw.line(self.game.screen, "yellow", (self.x, self.y), (self.x, self.y + self.vy * 1000))

        # Update x, y, and rotation, check for collision
        if self.vx > 0:     nextx = self.x + self.vx + radius
        else:               nextx = self.x + self.vx - radius
        if self.vy < 0:     nexty = self.y - self.vy + radius
        else:               nexty = self.y - self.vy - radius
        # TODO: check map collission
        self.x = constrain(self.x + self.vx, radius, RESx - radius)
        self.y = constrain(self.y - self.vy, radius, RESx - radius)

        # Update Rotation
        self.theta = self.theta + rotSpd * (int(TURNR) - int(TURNL))
        # Make sure theta stays between 0 and 2PI
        self.theta %= TAU
        
