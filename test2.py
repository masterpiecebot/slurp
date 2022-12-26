import pygame

screen = pygame.display.set_mode((1024, 512))

texture = pygame.image.load("data/bluemeat.png")
w = texture.get_width()
h = texture.get_height()
#screen.blit(slice, (0,0))
#screen.blit(texture, (0,0))

for i in range(512):
    slice = texture.subsurface(i, 0, 1, 512)
    screen.blit(slice, (i*2, 0))
pygame.display.flip()

while True:
    for i in pygame.event.get():
 
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if i.type == pygame.QUIT:
            pygame.quit()
