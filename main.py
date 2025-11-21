import pygame
import sys
from player import player
from camera import camera

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CS439_FinalProject_BraydenFairchild")

# World settings (larger than screen)
WORLD_WIDTH = 3000
WORLD_HEIGHT = 2000

# Clock for delta time
clock = pygame.time.Clock()

# Create player
player = player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)

# Create camera
camera = camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)

# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000  # delta time in seconds

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keyboard input
    keys = pygame.key.get_pressed()
    player.handle_input(keys, dt, WORLD_WIDTH, WORLD_HEIGHT)

    # Update camera to follow player
    camera.update(player)

    # Draw
    window.fill((30, 30, 30))  # background color
    player.draw(window, camera)

    # Example: draw world bounds (optional)
    pygame.draw.rect(window, (100, 100, 100), camera.apply(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT)), 5)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
