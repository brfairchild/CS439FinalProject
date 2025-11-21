import pygame
import sys


pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("CS439_FinalProject_BraydenFairchild")


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((30, 30, 30))

    # Update Screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
