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
    behind = False                  # If there's a taller texture behind this one

def castRays(screen, p, m):
    divisions = RESv
    increment = 1 if divisions == 1 else p.fov/(divisions-1)
    theta = p.theta
    if divisions != 1:
        theta = p.theta - p.fov/2
    # Generate the rays to be cast
    for i in range(divisions):
        theta %= PI*2
        # Calculate the scanline of the texture to draw
        # Calculate how far along the grid block the end of the ray is
        r = castRay(screen, p, m, theta)
        if r:
            drawRay(screen, p, m, r, i)
        theta += increment

def castRay(screen, p, m, angle):
    # Find which coordinate of the map the player is inside
    playerMapX = math.floor(p.x)
    playerMapY = math.floor(p.y)
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    tan_a = math.tan(angle)
    xUnitComp = tan_a
    yUnitComp = 1 / xUnitComp
    # VERTICAL WALL FINDER
    # Find the x coordinate of the map that the player is facing (plus or minus one)
    xright = int(angle < PI)                            # Is x facing right? 1 or 0
    dx = 2*xright-1                                     # Which direction is x facing? -1 or 1
    x_vert = playerMapX + xdirection                    # Map block that x is facing
    apparentx = playerMapX + 0.5 * xdirection + 0.5     # Vert that x is facing
    # Find the components of the ray, and the appropriate map y coordinate
    depth_vert = (apparentx - p.x) / sin_a                           # Distance from player to nearest vert
    y_vert = p.y - depth_vert * cos_a
    delta_depth = dx / cos_a
    dy = - sin_a * delta_depth
    for i in range(p.dof):
        tile_vert = int(x_vert), int(y_vert)
        if tile_vert in self.game.world
        if m.grid[constrain(xneary, 0, m.maph-1)][constrain(x_vert, 0, m.mapw-1)] != 0:
            texturex = m.grid[constrain(xneary, 0, m.maph-1)][constrain(x_vert, 0, m.mapw-1)]  # Save the texture of the map pixel touched
            break
        else:
            xrayx += RESx/m.mapw * dx
            xrayy += yUnitComp * RESx/m.mapw * dx
            x_vert += dx
            xneary = round((p.y-xrayy)/RESy*m.maph-0.5)
    # Not written: Draw the ray
    # HORIZONTAL WALL FINDER
    ydirection = -2 * int(angle < PI/2 or angle > PI/2*3) + 1
    yneary = playerMapY + ydirection
    apparenty = playerMapY + 0.5 * ydirection + 0.5
    # Find the components of the ray, and the appropriate map x coordinate
    pass # Used to have xunitcomp here, but it was more efficient to move it earlier
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
        if texturex == -1:  return False    # If no wall found in depth of field
        return Ray(xrayx, xrayy, x_vert, xneary, angle, math.sqrt(xrayx**2 + xrayy**2), True, texturex)
    else:
        if texturey == -1:  return False    # If no wall found in depth of field
        return Ray(yrayx, yrayy, ynearx, yneary, angle, math.sqrt(yrayx**2 + yrayy**2), False, texturey)

def castRay2(screen, p, m, angle):
    # Find which coordinate of the map the player is inside
    playerMapX = math.floor(p.x / RESx * m.mapw)
    playerMapY = math.floor(p.y / RESy * m.maph)
    # VERTICAL WALL FINDER
    # Find the x coordinate of the map that the player is facing (plus or minus one)
    xdirection = 2*int(angle < PI)-1
    xnearx = playerMapX + xdirection
    apparentx = playerMapX + 0.5 * xdirection + 0.5
    # println("Map X: ",playerMapX," | nearx: ",xnearx," | apparentx: ",apparentx);
    # Find the components of the ray, and the appropriate map y coordinate
    xUnitComp = math.tan(angle)
    yUnitComp = 1 / xUnitComp
    xrayx = apparentx * RESx / m.mapw - p.x
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
    apparenty = playerMapY + 0.5 * ydirection + 0.5
    # Find the components of the ray, and the appropriate map x coordinate
    pass # Used to have xunitcomp here, but it was more efficient to move it earlier
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
        if texturex == -1:  return False    # If no wall found in depth of field
        return Ray(xrayx, xrayy, xnearx, xneary, angle, math.sqrt(xrayx**2 + xrayy**2), True, texturex)
    else:
        if texturey == -1:  return False    # If no wall found in depth of field
        return Ray(yrayx, yrayy, ynearx, yneary, angle, math.sqrt(yrayx**2 + yrayy**2), False, texturey)


def drawRay(screen, p, m, r, lineNum):
    percent = 0
    if not r.isVertical:
        if m.drawmap:   # Draw ray on 2D map
            pg.draw.line(screen, (153, 153, 165), (p.x + OFFSET2D, p.y), (p.x + OFFSET2D - r.endx, p.y + r.endy))
        step = (p.x - r.endx) - r.gridx * m.gridPixelW
        percent = step / m.gridPixelW
        if p.theta > PI / 2 and p.theta < 3 * PI / 2:
            percent = 1 - percent
    else:
        if m.drawmap:   # Draw ray on 2D map
            pg.draw.line(screen, (153, 153, 165), (p.x + OFFSET2D, p.y), (p.x + OFFSET2D + r.endx, p.y - r.endy))
        step = (p.y - r.endy) - r.gridy * m.gridPixelH
        percent = step / m.gridPixelH
        if p.theta > PI:
            percent = 1 - percent
    scanline = round(percent * (m.textures[r.texture-1].get_width() - 1))
    scanlineTexture = m.textureSlices[r.texture-1][scanline]
    texture = m.textures[r.texture-1]
    ratio = texture.get_height()/texture.get_width()
    rectHeight = int(1 / r.distance * HEIGHTSCALE * ratio)
    darkness = 256 * (RESx - r.distance) / RESx
    # scanlineTexture = scanlineTexture.fill((darkness, darkness, darkness), special_flags=ADD)
    # If rectHeight > screen  height, don't waste time scaling an image super large
    if rectHeight < RESy or True:
        scanlineTexture = pg.transform.scale(scanlineTexture, (RESx/RESv, rectHeight))
        screen.blit(scanlineTexture, (lineNum*(RESx/RESv), RESy/2 - rectHeight*(ratio-1)/ratio))


def drawRayH(screen, p, m, r, lineNum):
    percent = 0
    if not r.isVertical:
        step = (p.x - r.endx) - r.gridx * m.gridPixelW
        percent = step / m.gridPixelW
        if p.theta > PI / 2 and p.theta < 3 * PI / 2:
            percent = 1 - percent
    else:
        step = (p.y - r.endy) - r.gridy * m.gridPixelH
        percent = step / m.gridPixelH
        if p.theta > PI:
            percent = 1 - percent
    scanline = round(percent * (m.textures[r.texture-1].get_width() - 1))
    scanlineTexture = m.textureSlices[r.texture-1][scanline]
    texture = m.textures[r.texture-1]
    # ratio = texture.get_height()/texture.get_width()
    rectHeight = int(1 / r.distance * HEIGHTSCALE)
    darkness = 256 * (RESx - r.distance) / RESx
    # scanlineTexture = scanlineTexture.fill((darkness, darkness, darkness), special_flags=ADD)
    scanlineTexture = pg.transform.scale(scanlineTexture, (RESx/RESv, rectHeight))
    screen.blit(scanlineTexture, (lineNum*(RESx/RESv), RESy - rectHeight >> 1))