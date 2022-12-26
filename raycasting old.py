from settings import *
import pygame as pg
from typing import NamedTuple
import math
from math import pi as PI

class Ray(NamedTuple):
    endx : float;   endy : float
    gridx : int;    gridy : int
    theta : float
    distance : float
    isVertical : bool
    texture : int

def castRays(screen, p, m):
    divisions = RESv//2
    increment = p.fov/(divisions*2+1);
    for i in range(-divisions, divisions+1):
        theta = p.theta + i*increment
        if theta > PI*2:    theta -= PI*2
        elif theta < 0:     theta += PI*2
        distance = castRay(screen, p, m, theta)
        # TODO: draw rectangles

def castRay(screen, p, m, angle):
    # Find which coordinate of the map the player is inside
    playerMapX = p.x // RESx * m.mapw
    playerMapY = p.y // RESy * m.maph
    # VERTICAL WALL FINDER
    # Find the x coordinate of the map that the player is facing (plus or minus one)
    xdirection = 2*int(angle < PI)-1
    xnearx = playerMapX + xdirection
    apparentx = playerMapX + 0.5*xdirection+ 0.5
    # println("Map X: ",playerMapX," | nearx: ",xnearx," | apparentx: ",apparentx);
    # Find the components of the ray, and the appropriate map y coordinate
    yUnitComp = 1 / math.tan(angle)
    xrayx = apparentx*RESx/m.mapw - p.x
    xrayy = xrayx * yUnitComp
    xneary = round((p.y-xrayy)/RESy*m.maph-0.5)
    # If there's no wall there, move 1 map.x unit further and check again, up to depth of view
    texturex = -1
    for i in range(p.dof):
        if m.grid[constrain(xneary, 0, m.maph-1)][constrain(xnearx, 0, m.mapw-1)] != 0:
            texturex = m.grid[constrain(xneary, 0, m.maph-1)][constrain(xnearx, 0, m.mapw-1)]  # Save the texture of the map pixel touched
            break
        else:
            xrayx += RESx/m.mapw * xdirection
            xrayy += yUnitComp * RESx/m.mapw * xdirection
            xnearx += xdirection
            xneary = round((p.y-xrayy)/RESy*m.maph-0.5)
    # Not written: Draw the ray
    # HORIZONTAL WALL FINDER
    ydirection = -2 * int(angle < PI/2 or angle > PI/2*3) + 1
    yneary = playerMapY + ydirection
    apparenty = playerMapY + 0.5*ydirection + 0.5
    # Find the components of the ray, and the appropriate map x coordinate
    xUnitComp = math.tan(angle)
    yrayy = apparenty*RESy/m.maph - p.y
    yrayx = yrayy * xUnitComp
    ynearx = round((p.x-yrayx)/RESx*m.mapw-0.5)
    #println("Map Y: ",playerMapY," | neary: ",xneary," | apparenty: ",apparenty)
    # If there's no wall there, move 1 map.y unit further and check again, up to depth of view
    texturey = -1
    for i in range(p.dof):
        if m.grid[constrain(yneary, 0, m.maph-1)][constrain(ynearx, 0, m.mapw-1)] != 0:
            texturey = m.grid[constrain(yneary, 0, m.maph-1)][constrain(ynearx, 0, m.mapw-1)]  # Save the texture of the map pixel touched
            break
        else:
            yrayx += xUnitComp * RESy/m.maph * ydirection
            yrayy += RESy/m.maph * ydirection
            ynearx = round((p.x-yrayx)/RESx*m.mapw-0.5)
            yneary += ydirection
    # Not written: Draw the ray
    # PICK THE SHORTER RAY
    lenx = math.sqrt(xrayx**2 + xrayy**2)
    leny = math.sqrt(yrayx**2 + yrayy**2)
    if lenx < leny:
        # TO USE LATER pg.draw.line(screen, (153, 153, 165), (p.x+RESx, p.y), (p.x+RESx + xrayx, p.y - xrayy))
        pg.draw.line(screen, (153, 153, 165), (p.x, p.y), (p.x + xrayx, p.y - xrayy))
        return Ray(xrayx, xrayy, xnearx, xneary, angle, math.sqrt(xrayx**2 + xrayy**2), True, texturex)
    else:
        # TO USE LATER pg.draw.line(screen, (153, 153, 165), (p.x+RESx, p.y), (p.x+RESx - yrayx, p.y + yrayy))
        pg.draw.line(screen, (153, 153, 165), (p.x, p.y), (p.x - yrayx, p.y + yrayy))
        return Ray(yrayx, yrayy, ynearx, yneary, angle, math.sqrt(xrayx**2 + xrayy**2), False, texturey)
    
