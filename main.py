import pygame
import sys
from player import player  # Make sure player.py is in the same folder or in PYTHONPATH

# Initialize Pygame
pygame.init()

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("CS439_FinalProject_BraydenFairchild")

# Clock for delta time
clock = pygame.time.Clock()

# Create player
player = player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)

# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player.handle_input(keys, dt)

    window.fill((30, 30, 30))
    player.draw(window)
    pygame.display.flip()


pygame.quit()
sys.exit()
