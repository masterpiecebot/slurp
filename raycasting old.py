from settings import *
import pygame as pg
from typing import NamedTuple
import math
from math import pi as PI


class Ray(NamedTuple):
    start: tuple
    end: tuple
    tile: tuple
    theta: float
    distance: float
    dir: str
    behind: 'typing.Any' = False  # If there's a taller texture behind this one


def castRays(screen, p, m):
    divisions = RESv
    increment = 1 if divisions == 1 else p.fov / (divisions - 1)
    theta = p.theta
    if divisions != 1:
        theta = p.theta - p.fov / 2
    # Generate the rays to be cast
    for i in range(divisions):
        theta %= PI * 2
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
    # Set both depths to infinity in case no wall is found in that direction
    depth_vert, depth_hor = float('inf'), float('inf')
    q = (p.x * m.gridPixelW + OFFSET2D, p.y * m.gridPixelH)
    tan_a = math.tan(angle) + 0.00001

    # VERTICAL WALL FINDER
    x_right = int(angle < PI)
    dx = 2 * x_right - 1
    dy = - dx / tan_a
    x_vert = playerMapX + x_right
    y_vert = p.y - (x_vert - p.x) / tan_a
    for i in range(p.dof):
        tile_vert = x_vert - 1 + x_right, math.floor(y_vert)
        if tile_vert in m.map:
            depth_vert = math.sqrt((x_vert - p.x) ** 2 + (y_vert - p.y) ** 2)
            break
        x_vert += dx
        y_vert += dy

    # HORIZONTAL WALL FINDER
    y_down = int(angle > PI / 2 and angle < PI / 2 * 3)
    dy = 2 * y_down - 1
    dx = - tan_a / dy
    y_hor = playerMapY + y_down
    x_hor = p.x - (y_hor - p.y) * tan_a
    for i in range(p.dof):
        tile_hor = math.floor(x_hor), y_hor - 1 + y_down
        if tile_hor in m.map:
            depth_hor = math.sqrt((x_hor - p.x) ** 2 + (y_hor - p.y) ** 2)
            break
        x_hor += dx
        y_hor += dy

    if depth_hor == depth_vert == float('inf'):
        return False
    elif depth_vert < depth_hor:
        texture = m.map[tile_vert]
        return Ray((p.x, p.y), (x_vert, y_vert), tile_vert, angle, depth_vert, "W" if x_right else "E")
    else:
        texture = m.map[tile_hor]
        return Ray((p.x, p.y), (x_hor, y_hor), tile_hor, angle, depth_hor, "N" if y_down else "S")


def castRay3(screen, p, m, angle):
    # Find which coordinate of the map the player is inside
    playerMapX = math.floor(p.x)
    playerMapY = math.floor(p.y)
    sin_a = math.sin(angle) + 0.00001
    cos_a = math.cos(angle)
    tan_a = math.tan(angle)
    # VERTICAL WALL FINDER
    # Find the x coordinate of the map that the player is facing (plus or minus one)
    x_right = int(angle < PI)  # Is x facing right? 1 or 0
    dx = 2 * x_right - 1  # Which direction is x facing? -1 or 1
    x_vert = playerMapX + x_right  # Map block that x is facing
    # Find the components of the ray, and the appropriate map y coordinate
    depth_vert = (x_vert - p.x) / sin_a  # Distance from player to nearest vert
    y_vert = p.y - depth_vert * cos_a
    delta_depth = dx / sin_a
    dy = - cos_a * delta_depth
    for i in range(p.dof):
        tile_vert = int(x_vert), int(y_vert)
        if tile_vert in m.map:
            break
        x_vert += dx
        y_vert += dy
        depth_vert += delta_depth
    pg.draw.line(screen, "yellow", (p.x * m.gridPixelW, p.y * m.gridPixelH),
                 (x_vert * m.gridPixelW, y_vert * m.gridPixelH), 5)
    # Not written: Draw the ray
    # HORIZONTAL WALL FINDER
    y_down = int(angle > PI / 2 and angle < PI / 2 * 3)
    dy = 2 * y_down - 1
    y_hor = playerMapY + y_down
    depth_hor = (y_hor - p.y) / cos_a
    x_hor = p.x - depth_hor * sin_a
    delta_depth = dy / cos_a
    dx = - tan_a / dy


    for i in range(p.dof):
        tile_hor = int(x_hor), int(y_hor)
        if tile_hor in m.map:
            break
        x_hor += dx
        y_hor += dy
        depth_hor += delta_depth
    pg.draw.line(screen, "black", (p.x * m.gridPixelW, p.y * m.gridPixelH),
                 (x_hor * m.gridPixelW, y_hor * m.gridPixelH), 2)

    if depth_hor < depth_vert:
        return  # Ray(x_hor - p.x, y_hor - p.y, x_hor, y_hor, angle, depth_hor, True, m.map[tile_hor])
    else:
        return  # Ray(x_vert - p.x, y_vert - p.y, x_vert, y_vert, angle, depth_vert, True, m.map[tile_vert])


def castRay2(screen, p, m, angle):
    # Find which coordinate of the map the player is inside
    playerMapX = math.floor(p.x / RESx * m.mapw)
    playerMapY = math.floor(p.y / RESy * m.maph)
    # VERTICAL WALL FINDER
    # Find the x coordinate of the map that the player is facing (plus or minus one)
    xdirection = 2 * int(angle < PI) - 1
    xnearx = playerMapX + xdirection
    apparentx = playerMapX + 0.5 * xdirection + 0.5
    # println("Map X: ",playerMapX," | nearx: ",xnearx," | apparentx: ",apparentx);
    # Find the components of the ray, and the appropriate map y coordinate
    xUnitComp = math.tan(angle)
    yUnitComp = 1 / xUnitComp
    xrayx = apparentx * RESx / m.mapw - p.x
    xrayy = xrayx * yUnitComp
    xneary = round((p.y - xrayy) / RESy * m.maph - 0.5)
    # If there's no wall there, move 1 map.x unit further and check again, up to depth of view
    texturex = -1
    for i in range(p.dof):
        if m.grid[constrain(xneary, 0, m.maph - 1)][constrain(xnearx, 0, m.mapw - 1)] != 0:
            texturex = m.grid[constrain(xneary, 0, m.maph - 1)][
                constrain(xnearx, 0, m.mapw - 1)]  # Save the texture of the map pixel touched
            break
        else:
            xrayx += RESx / m.mapw * xdirection
            xrayy += yUnitComp * RESx / m.mapw * xdirection
            xnearx += xdirection
            xneary = round((p.y - xrayy) / RESy * m.maph - 0.5)
    # Not written: Draw the ray
    # HORIZONTAL WALL FINDER
    ydirection = -2 * int(angle < PI / 2 or angle > PI / 2 * 3) + 1
    yneary = playerMapY + ydirection
    apparenty = playerMapY + 0.5 * ydirection + 0.5
    # Find the components of the ray, and the appropriate map x coordinate
    pass  # Used to have xunitcomp here, but it was more efficient to move it earlier
    yrayy = apparenty * RESy / m.maph - p.y
    yrayx = yrayy * xUnitComp
    ynearx = round((p.x - yrayx) / RESx * m.mapw - 0.5)
    # println("Map Y: ",playerMapY," | neary: ",xneary," | apparenty: ",apparenty)
    # If there's no wall there, move 1 map.y unit further and check again, up to depth of view
    texturey = -1
    for i in range(p.dof):
        if m.grid[constrain(yneary, 0, m.maph - 1)][constrain(ynearx, 0, m.mapw - 1)] != 0:
            texturey = m.grid[constrain(yneary, 0, m.maph - 1)][
                constrain(ynearx, 0, m.mapw - 1)]  # Save the texture of the map pixel touched
            break
        else:
            yrayx += xUnitComp * RESy / m.maph * ydirection
            yrayy += RESy / m.maph * ydirection
            ynearx = round((p.x - yrayx) / RESx * m.mapw - 0.5)
            yneary += ydirection
    # Not written: Draw the ray
    # PICK THE SHORTER RAY
    lenx = math.sqrt(xrayx ** 2 + xrayy ** 2)
    leny = math.sqrt(yrayx ** 2 + yrayy ** 2)

    if lenx < leny:
        if texturex == -1:  return False  # If no wall found in depth of field
        return Ray(xrayx, xrayy, xnearx, xneary, angle, math.sqrt(xrayx ** 2 + xrayy ** 2), True, texturex)
    else:
        if texturey == -1:  return False  # If no wall found in depth of field
        return Ray(yrayx, yrayy, ynearx, yneary, angle, math.sqrt(yrayx ** 2 + yrayy ** 2), False, texturey)


def drawRay(screen, p, m, r, lineNum):
    distance = r.distance #* abs(math.cos((p.theta - r.theta)))
    screen_dist = RESx // 2 / math.tan(p.fov / 2)
    scan_height = screen_dist * 1 / distance
    # scan_height = int(1 / r.distance * HEIGHTSCALE)
    # If rectHeight > screen  height, don't waste time scaling an image super large
    if scan_height > RESy:
        return
    texture_num = m.map[r.tile] - 1
    texture = m.textures[texture_num]
    w, h = texture.get_width(), texture.get_height()
    if m.drawmap:  # Draw ray on 2D map
        pg.draw.line(screen, (153, 153, 165), (p.x * m.gridPixelW + OFFSET2D, p.y * m.gridPixelH),
                     (r.end[0] * m.gridPixelW + OFFSET2D, r.end[1] * m.gridPixelH))
    if r.dir == 'E':
        step = 1 - r.end[1] % 1
        # pg.draw.line(screen, "green", (r.end[0] * m.gridPixelW + OFFSET2D, r.end[1] * m.gridPixelH),
        #              (r.end[0] * m.gridPixelW + OFFSET2D, (r.end[1] + step) * m.gridPixelH), 2)
    elif r.dir == 'W':
        step = r.end[1] % 1
        # pg.draw.line(screen, "green", (r.end[0] * m.gridPixelW + OFFSET2D, r.end[1] * m.gridPixelH),
        #              (r.end[0] * m.gridPixelW + OFFSET2D, (r.end[1] - step) * m.gridPixelH), 2)
    elif r.dir == 'S':
        step = r.end[0] % 1
        # pg.draw.line(screen, "green", (r.end[0] * m.gridPixelW + OFFSET2D, r.end[1] * m.gridPixelH),
        #              ((r.end[0] - step) * m.gridPixelW + OFFSET2D, (r.end[1]) * m.gridPixelH), 2)
    elif r.dir == 'N':
        step = 1 - r.end[0] % 1
        # pg.draw.line(screen, "green", (r.end[0] * m.gridPixelW + OFFSET2D, r.end[1] * m.gridPixelH),
        #              ((r.end[0] + step) * m.gridPixelW + OFFSET2D, (r.end[1]) * m.gridPixelH), 2)
    scanline = math.floor(step * w)
    scanline_texture = m.textureSlices[texture_num][scanline]
    scan_width = RESx / RESv
    darkness = [255 / (1 + r.distance ** 5 * 0.00002)] * 3  # TODO
    # scanlineTexture = scanlineTexture.fill((darkness, darkness, darkness), special_flags=ADD)
    scanline_texture = pg.transform.scale(scanline_texture, (scan_width, scan_height))
    screen.blit(scanline_texture, (lineNum * scan_width, (RESy - scan_height)/2))
    return


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
    scanline = round(percent * (m.textures[r.texture - 1].get_width() - 1))
    scanlineTexture = m.textureSlices[r.texture - 1][scanline]
    texture = m.textures[r.texture - 1]
    # ratio = texture.get_height()/texture.get_width()
    rectHeight = int(1 / r.distance * HEIGHTSCALE)
    darkness = 256 * (RESx - r.distance) / RESx
    # scanlineTexture = scanlineTexture.fill((darkness, darkness, darkness), special_flags=ADD)
    scanlineTexture = pg.transform.scale(scanlineTexture, (RESx / RESv, rectHeight))
    screen.blit(scanlineTexture, (lineNum * (RESx / RESv), RESy - rectHeight >> 1))
