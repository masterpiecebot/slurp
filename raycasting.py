from settings import *
import pygame as pg
from typing import NamedTuple
import math
from math import pi as PI


class Ray(NamedTuple):
    start: tuple
    end: tuple
    tile: tuple
    distance: float
    dir: str
    behind: 'typing.Any' = False  # If there's a taller texture behind this one

class RayCaster():

    def __init__(self, screen, p, m):
        self.screen = screen
        self.p = p
        self.m = m

    def cast_rays(self):
        screen, p, m = self.screen, self.p, self.m
        # Find which coordinate of the map the player is inside
        playerMapX = math.floor(p.x)
        playerMapY = math.floor(p.y)
        q = (p.x * m.gridW + OFFSET2D, p.y * m.gridH) # Player location to draw
        for scanline in range(RESv):
            cameraX = 2 * scanline / (RESv-1) - 1
            rayDirX = p.dirX + p.planeX * cameraX
            rayDirY = p.dirY + p.planeY * cameraX
            # Set both depths to infinity in case no wall is found in that direction
            depth_vert, depth_hor = float('inf'), float('inf')

            # VERTICAL WALL FINDER
            x_right = int(rayDirX > 0)      # Whether player looking east, value  0 / 1
            dx = 2 * x_right - 1            # Whether player looking east, value -1 / 1. Used as unit step for raycast
            dy = dx * rayDirY / rayDirX     # Unit step for raycast
            x_vert = playerMapX + x_right   # Nearest vertical grid line that player is looking towards
            y_vert = (x_vert - p.x) * rayDirY / rayDirX + p.y            # Y coord at intersection of ray and near vert
            while 0 <= x_vert <= m.mapw and 0 <= y_vert <= m.maph:       # If ray has not left the map yet
                tile_vert = x_vert - 1 + x_right, math.floor(y_vert)     # Find tile player is looking at
                if tile_vert in m.map:                                   # If tile can be found in dict of valid walls
                    depth_vert = math.hypot(x_vert - p.x, y_vert - p.y)  # Calculate distance ray traveled
                    break                                                # If wall found, you can stop looking
                x_vert += dx                # If no wall found, advance ray one unit step to next gridline
                y_vert += dy

            # HORIZONTAL WALL FINDER
            y_down = int(rayDirY > 0)       # Whether player looking south, value  0 / 1
            dy = 2 * y_down - 1             # Whether player looking south, value -1 / 1. Used as unit step for raycast
            dx = dy * rayDirX / rayDirY     # Unit step for raycast
            y_hor = playerMapY + y_down     # Nearest horizontal grid line that player is looking towards
            x_hor = (y_hor - p.y) * dx / dy + p.x                       # X coord at intersection of ray and near horiz
            while 0 <= x_hor <= m.mapw and 0 <= y_hor <= m.maph:        # If ray has not left the map yet
                tile_hor = math.floor(x_hor), y_hor - 1 + y_down        # Find tile player is looking at
                if tile_hor in m.map:                                   # If tile can be found in dict of valid walls
                    depth_hor = math.hypot(x_hor - p.x, y_hor - p.y)    # Calculate distance ray traveled
                    break                                               # If wall found, you can stop looking
                x_hor += dx                 # If no wall found, advance ray one unit step to next gridline
                y_hor += dy

            if depth_hor == depth_vert == float('inf'):     # If no wall found either way, skip ray
                continue
            # Establish ending location as the shorter ray
            if depth_vert < depth_hor:
                x, y, tile, depth = (x_vert, y_vert, tile_vert, depth_vert)
                dir = 'W' if x_right == 1 else 'E'
            else:
                x, y, tile, depth = (x_hor, y_hor, tile_hor, depth_hor)
                dir = 'N' if y_down == 1 else 'S'
            texture = m.map[tile]
            if m.drawMap:   # Draw on minimap, for testing purposes
                pg.draw.line(screen, "gray", q, (x * m.gridW + OFFSET2D, y * m.gridH))
            # Draw the ray
            r = Ray((p.x, p.y), (x, y), tile, depth, dir)
            self.draw_ray(r, scanline)

    def draw_ray(self, r, lineNum):
        screen, p, m = self.screen, self.p, self.m
        distance = r.distance # * abs(math.cos((p.theta - r.theta)))
        screen_dist = RESx // 2 / math.tan(p.fov / 2)
        scan_height = screen_dist * 1 / distance
        # scan_height = int(1 / r.distance * HEIGHTSCALE)
        # If rectHeight > screen  height, don't waste time scaling an image super large
        if scan_height > RESy:
            return
        texture_num = m.map[r.tile] - 1
        texture = m.textures[texture_num]
        w, h = texture.get_width(), texture.get_height()
        # if m.drawmap:  # Draw ray on 2D map
        #     pg.draw.line(screen, (153, 153, 165), (p.x * m.gridW + OFFSET2D, p.y * m.gridH),
        #                  (r.end[0] * m.gridW + OFFSET2D, r.end[1] * m.gridH))
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

    def draw_ray_h(self, screen, p, m, r, lineNum):
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
        rectHeight = int(1 / r.distance * HEIGHT_SCALE)
        darkness = 256 * (RESx - r.distance) / RESx
        # scanlineTexture = scanlineTexture.fill((darkness, darkness, darkness), special_flags=ADD)
        scanlineTexture = pg.transform.scale(scanlineTexture, (RESx / RESv, rectHeight))
        screen.blit(scanlineTexture, (lineNum * (RESx / RESv), RESy - rectHeight >> 1))
