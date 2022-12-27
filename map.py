from settings import *
import pygame as pg
import os

# Map variables
mapName = "map.png"      # Map Filename
MAPCOLOR = (0, 100, 47)  # Color of blocks in 2D topdown mode
crudeMap = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,2,2,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,2,2,0,0,0,1,1,1,1,1,1,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
  [1,0,0,0,0,0,0,0,2,0,0,0,1,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
  [1,0,0,0,0,0,0,1,1,1,1,1,1,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,1,0,0,0,0,0,0,2,2,0,0,1],
  [1,0,0,0,1,0,0,0,0,0,0,2,2,0,0,1],
  [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]  ]

# Game Textures
# Textures have a filename, height in game, and #TODO
# Height of 1 is half height, height of 2 is full height, height of 3 is higher. Textures should have appropriate h/w ratios.
textureList = [
  ["brick5.png", 2],
  ["bluemeat.png", 1]
]

class Map():

    def __init__(self):
        self.grid = crudeMap
        self.mapw = len(self.grid[0])
        self.maph = len(self.grid)
        self.gridPixelW = RESx / self.mapw
        self.gridPixelH = RESy / self.maph

        self.textures = []      # Textures used by the game
        self.textureSlices = [] # A list of vertical slices of each texture, to be used by scanlines

        self.drawmap = True

        # Load Textures
        for i in range(len(textureList)):
            texture = pg.image.load(os.path.join('textures', textureList[i][0])).convert_alpha()
            self.textures.append(texture)
            self.textureSlices.append([])
            height = texture.get_height()
            for j in range(texture.get_width()):
              slice = texture.subsurface(j, 0, 1, height)
              self.textureSlices[i].append(slice)

    def drawMap(self):
        self.drawmap = not self.drawmap

def drawMap2D(screen, m):
    for i in range(m.maph):
        for j in range(m.mapw):
            if m.grid[i][j] != 0:
                image = pg.transform.scale(m.textures[m.grid[i][j]-1], (RESx//m.mapw, RESy//m.maph))
                screen.blit(image, (j * RESx/m.mapw + OFFSET2D, i * RESy/m.maph))