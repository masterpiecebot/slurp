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

crudeMap2 = [[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]

# Game Textures
# Textures have a filename, height in game, and #TODO
# Height of 1 is half height, height of 2 is full height, height of 3 is higher. Textures should have appropriate h/w ratios.
textureList = [
  ["brick5.png", 2],
  ["bluemeat.png", 1]
]

class Map():

    def __init__(self):
        self.grid = crudeMap            # Array of wall values
        self.mapw = len(self.grid[0])   # Width of map
        self.maph = len(self.grid)      # Height of map
        self.gridW = RESx / self.mapw   # Unit grid width on minimap
        self.gridH = RESy / self.maph   # Unit grid height on minimap

        self.textures = []              # Textures used by the game
        self.textureSlices = []         # A list of vertical slices of each texture, to be used by scanlines

        self.drawmap = False            # Whether or not the minimap will be displayed.

        # Load map into dictionary, which makes for faster coordinate lookup.
        self.map = {}
        for i in range(len(crudeMap)):
            for j in range(len(crudeMap[0])):
                if crudeMap[i][j] != 0:
                    self.map.update({(j, i): crudeMap[i][j]})

        # Load Textures, slice them for faster drawing of scanlines later
        for i in range(len(textureList)):
            texture = pg.image.load(os.path.join('textures', textureList[i][0])).convert_alpha()
            self.textures.append(texture)
            self.textureSlices.append([])
            height = texture.get_height()
            for j in range(texture.get_width()):
              slice = texture.subsurface(j, 0, 1, height)
              self.textureSlices[i].append(slice)

    def drawMap(self):      # Turns minimap on or off
        self.drawmap = not self.drawmap

    # Draw Minimap
    def drawMap2D(self, screen):
        for i in range(self.maph):
            for j in range(self.mapw):
                if self.grid[i][j] != 0:
                    image = pg.transform.scale(self.textures[self.grid[i][j]-1], (RESx//self.mapw, RESy//self.maph))
                    screen.blit(image, (j * RESx/self.mapw + OFFSET2D, i * RESy/self.maph))