# Game variables
FPS = 60            # Framerate
RESx, RESy = 768, 768          # Game resolution
RES = RESx*2, RESy
RESv = 256          # # of vertical scanlines drawn
HEIGHTSCALE = 20000 # Scale for the vertical height of rectangles drawn
OFFSET2D = RESx        # Where to draw the 2D map
DISPLAYMAP = True

# Helper functions from Processing
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))