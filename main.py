import pygame
import sys
from player import player
from attack import attack
from camera import camera

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CS439_FinalProject_BraydenFairchild")

WORLD_WIDTH = 3000
WORLD_HEIGHT = 2000

clock = pygame.time.Clock()

# Create player and camera
player = player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
camera = camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)

attacks = []

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.handle_input(keys, dt, WORLD_WIDTH, WORLD_HEIGHT)

    # Spawn attack if space pressed
    if keys[pygame.K_SPACE]:
        attacks.append(attack(player.rect.centerx, player.rect.centery, player.facing_right))

    # Update attacks
    for atk in attacks[:]:
        atk.update(dt)
        if atk.finished:
            attacks.remove(atk)

    camera.update(player)

    # Draw
    window.fill((30, 30, 30))
    player.draw(window, camera)
    for atk in attacks:
        atk.draw(window, camera)

    pygame.display.flip()

pygame.quit()
sys.exit()
