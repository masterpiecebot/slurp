# Game variables
FPS = 60  # Framerate
RESx, RESy = 768, 768  # Game resolution
RES = RESx, RESy
RESv = 384  # # of vertical scanlines drawn
HEIGHT_SCALE = 450  # Scale for the vertical height of rectangles drawn
OFFSET2D = RESx  # Where to draw the 2D map


# Helper functions from Processing
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def sign(val):
    return 1 if val >= 1 else -1
