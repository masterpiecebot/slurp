import pygame
import os
from math import pi


# Game variables
FPS = 60            # Framerate
RESx = 768          # Game resolution
RESy = 768
RESv = 256          # # of vertical scanlines drawn
HEIGHTSCALE = 20000 # Scale for the vertical height of rectangles drawn
screen = pygame.display.set_mode((RESx*2,RESy))

# Map variables
mapName = "map.png"      # Map Filename
#map                      # Map image loaded from file in setup()
#texture                  # Wall texture
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
mapw = len(crudeMap[0])     # Dimensions of map in blocks, set after map is loaded
maph = len(crudeMap)
gridPixelW = RESx / mapw      # Width and height of one grid block
gridPixelH = RESy / maph

# Texture Variables
textureList = [
  "brick5.png",
  "bluemeat.png"
]
textures = []           # Textures used by the game
textureSlices = []      # A list of vertical slices of each texture, to be used by scanlines

# Player Variables
p = ""                  # Player variable, uninitialized
RAD = 20                # Player size (radius)
FOV = pi/2              # Player field of view (radians)
THETA0 = pi * 1.4       # Player starting view direction (radians from north CW)

# Helper functions from Processing
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

# Pygame Initialization
def setup():
    global p
    
    pygame.init()
    pygame.display.set_caption('slurp')
    logo = pygame.image.load("data/logo.png")
    pygame.display.set_icon(logo)
    p = Player(RESx/2, RESy/2, THETA0)
    #map = loadImage("map.png")  # Load the image into the program  
    setupTextures()            # Load textures

def setupTextures():
    for i in range(len(textureList)):
        texture = pygame.image.load(os.path.join('data', textureList[i]))
        textures.append(texture)
        textureSlices.append([])
        height = texture.get_height()
        for j in range(texture.get_width()):
          slice = texture.subsurface(j, 0, 1, height)
          textureSlices[i].append(slice)

def draw():
    screen.fill((100,100,100))
    #TODO rawMap2D(crudeMap)
    #TODO p.move()
    #TODO castRays(p, crudeMap, FOV, RESv)
    p.display()
    #TODO textSize(40)
    #TODO fill(#FFFFFF)
    #TODO text(constrain(ceil(frameRate),0,60), RESx*2 - 50, RESy)
    pygame.display.flip()

#TODO void keyPressed()   p.setMove(keyCode, true)  
#TODO void keyReleased()  p.setMove(keyCode, false) 

class Player:
  pColor = (255, 255, 0)                    # Player color
  dof = 16                                  # Depth of field (view distance)
  vmax = 5                                  # Player max speed
  rotSpd = 0.04                             # Rotational speed (radians per frame)
  radius = RAD                              # Player size (radius)
  pAccel = 0.3                              # Player acceleration (speeding up from a stop, slowing down)
  
  isLeft, isRight, isUp, isDown = False, False, False, False   # Player movement states (key pressed)
  isTurnR, isTurnL = False, False           # Camera movement states (key pressed)
  x, y = 0, 0                               # Player x, y location
  theta, pFrameVX, pFrameVY = 0, 0, 0       # Player rotation, velocity in player frame of reference
  vx, vy = 0, 0                             # Player component velocities (x,y)
 
  def __init__(self, xx, yy, tt):
    self.x = xx
    self.y = yy
    self.theta = tt 
  
 
  def display(self):
    # Display a triangle with rotation
    # TODO: Add rotation
    #pushMatrix()
    #translate(x+RESx,y)
    #rotate(theta)
    pygame.draw.circle(screen, self.pColor, (0,0), self.radius*2)
    pygame.draw.polygon(screen, self.pColor, [[0-self.radius/2, 0+self.radius/2], [0+self.radius/2, 0+self.radius/2], [0, 0-self.radius]])
    #popMatrix()
    pygame.draw.circle(screen, (0,0,0), (self.x+RESx,self.y),5)
  
 
  def move(self):
    # Accelerate or decelerate depending on whether keys are held
    if (not isRight and not isLeft):    # If no movement key is pressed, slow down
        self.pFrameVX = constrain(self.pFrameVX - self.pAccel, 0, self.vmax)
    else:
        self.pFrameVX = constrain(self.pFrameVX + self.pAccel*(int(self.isLeft) - int(self.isRight)), -self.vmax, self.vmax)
    
    if (not isUp and not isDown):       # If no movement key is pressed, slow down
        self.pFrameVY = constrain(self.pFrameVY - self.pAccel, 0, self.vmax)
    else:
        self.pFrameVY = constrain(self.pFrameVY + self.pAccel*(int(self.isUp) - int(self.isDown)), -self.vmax, self.vmax)
    
      
    # Calculate component velocities for forward/backward movement plus strafing
    vx = pFrameVY * sin(theta) - pFrameVX * cos(theta)
    vy = pFrameVY * cos(theta) + pFrameVX * sin(theta)
    # Update x, y, and rotation, check for collision
    nextx, nexty = 0,0
    if (vx > 0):   nextx = x+vx+radius  
    else:          nextx = x+vx-radius  
    if (vy < 0):   nexty = y-vy+radius  
    else:          nexty = y-vy-radius 
    xcol = mapCollision(nextx, y, crudeMap)
    ycol = mapCollision(x, nexty, crudeMap)
    if (xcol):
        vx = 0
    if (ycol):
        vy = 0
    
    x = constrain(x + vx, radius, RESx - radius)
    y = constrain(y - vy, radius, RESy - radius)
    
    theta = theta + rotSpd*(int(isTurnR) - int(isTurnL))
    # Make sure theta stays between 0 and 2PI
    if (theta > TWO_PI):  theta -= TWO_PI  
    elif (theta < 0):  theta += TWO_PI 
  
 
  def setMove(k, b):
    # set the player as moving up, down, left, or right.
    # can use Arrow Keys or WASD
    match k: 
      case ord('W'):
          isUp = b
          return True
      case ord('S'):
          isDown = b
          return True
      case ord('A'):
          isLeft = b
          return True
      case ord('D'):
          isRight = b
          return True
      case pygame.K_UP:
          return false
      case pygame.K_DOWN:
          return false
      case pygame.K_LEFT:
          isTurnL = b
          return True
      case pygame.K_RIGHT:
          isTurnR = b
          return True
    return false

setup()
while True:
    draw()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
