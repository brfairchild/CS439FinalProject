import pygame
import sys
import os 
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

# Load the background
try:
    background_path = os.path.join("assets", "map.png")
    background_image = pygame.image.load(background_path).convert() 
except pygame.error as e:
    background_image = None


# Initializing player near the center of the world
player = player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
# Set up the camera to view the world, clamped to 3000x2000 bounds
camera = camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)

attacks = []

running = True
while running:
    # Frame-rate
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                # Only attack if the previous attack animation is finished
                if not player.is_attacking:
                    
                    mouse_pos_screen = pygame.mouse.get_pos()
                    # Convert screen position to world position so the attack knows where to aim
                    target_pos_world = camera.screen_to_world(mouse_pos_screen) 
                    
                    # Spawn the attack and lock the player's attack state
                    attacks.append(attack(player, target_pos_world)) 
                    player.is_attacking = True

    # Handle continuous key presses for movement
    keys = pygame.key.get_pressed()
    player.handle_input(keys, dt, WORLD_WIDTH, WORLD_HEIGHT)

    for atk in attacks[:]:
        atk.update(dt) 
        if atk.finished:
            attacks.remove(atk)
            player.is_attacking = False 

    # Update the camera position based on the player's movement
    camera.update(player)

    if background_image:
        # Calculate the camera offset (negative of world position)
        camera_offset_x = -camera.state.left
        camera_offset_y = -camera.state.top
        draw_position = (int(camera_offset_x), int(camera_offset_y))
        window.blit(background_image, draw_position) 
    else:
        window.fill((30, 30, 30))

    # Draw 
    player.draw(window, camera)
    for atk in attacks:
        atk.draw(window, camera)

    # Update screen
    pygame.display.flip()

pygame.quit()
sys.exit()