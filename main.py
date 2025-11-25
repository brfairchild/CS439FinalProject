import pygame
import sys
import os 
import pathlib
from player import player
from attack import attack
from base_bullet import Bullet
from spiral import SpiralPattern 
from playerbullet import PlayerBullet

# Initialize the mixer and Pygame
pygame.mixer.pre_init(44100, -16, 2, 512) 
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CS439_FinalProject_BraydenFairchild")

clock = pygame.time.Clock()

# Load the background
try:
    background_path = os.path.join("assets", "map.png")
    background_image = pygame.image.load(background_path).convert() 
except pygame.error as e:
    print(f"Error loading background image: {e}")
    background_image = None


player = player(SCREEN_WIDTH // 2, SCREEN_HEIGHT)

attacks = []
bullets = [] # Enemy 
friendly_bullets = [] # Player
active_patterns = [] 

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if not player.is_attacking:
                    
                    mouse_pos_screen = pygame.mouse.get_pos()
                    target_pos_screen = pygame.Vector2(mouse_pos_screen) 
                    
                    new_attack = attack(player, target_pos_screen) 
                    attacks.append(new_attack)
                    
                    new_attack.play_sound_once()
                    
                    player.is_attacking = True

    keys = pygame.key.get_pressed()
    
    # PATTERN LOGIC 
    if keys[pygame.K_SPACE]:
        if not any(isinstance(p, SpiralPattern) for p in active_patterns):
            
            OFFSET = 100
            
            top_left_x = OFFSET
            top_left_y = OFFSET
            
            top_right_x = SCREEN_WIDTH - OFFSET
            top_right_y = OFFSET
            
            active_patterns.append(SpiralPattern(top_left_x, top_left_y))
            active_patterns.append(SpiralPattern(top_right_x, top_right_y))
    
    player.handle_input(keys, dt, SCREEN_WIDTH, SCREEN_HEIGHT)

    # UPDATE ATTACKS
    for atk in attacks[:]:
        atk.update(dt) 
        if atk.finished:
            attacks.remove(atk)
            player.is_attacking = False 

    # Update Patterns and Spawn New Bullets
    for pattern in active_patterns[:]:
        new_bullets = pattern.update(dt)
        bullets.extend(new_bullets) 
        
        if pattern.finished:
            active_patterns.remove(pattern)

    # Enemy Bullets
    for bullet in bullets[:]:
        bullet.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT) 
        
        reflected_direction = None
        
        # Reflection collision
        for atk in attacks:
            result = bullet.check_collision(atk.hitbox)
            if result is not None:
                reflected_direction = atk.direction 
                break # Stops checking other attacks once a hit is confirmed.
        
        # Reflection or Removal
        if reflected_direction is not None:
            
            # Spawn reflected bullet
            reflected_vector = reflected_direction.copy()
            new_friendly_bullet = PlayerBullet(
                bullet.rect.centerx, 
                bullet.rect.centery, 
                reflected_vector 
            )
            friendly_bullets.append(new_friendly_bullet)
            
            # Remove enemy bullet
            bullets.remove(bullet)
            
        elif not bullet.alive:
            # Remove the enemy bullet if it went off-screen
            bullets.remove(bullet)

    # Clearing player bullet
    for f_bullet in friendly_bullets[:]:
        f_bullet.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        if not f_bullet.alive:
            friendly_bullets.remove(f_bullet)


    # Drawing
    if background_image:
        window.blit(background_image, (0, 0)) 
    else:
        window.fill((30, 30, 30))

    player.draw(window)
    
    for atk in attacks:
        atk.draw(window)

    # Draw Enemy Bullets
    for bullet in bullets:
        bullet.draw(window)
        
    # Draw friendly Bullets
    for f_bullet in friendly_bullets:
        f_bullet.draw(window)

    # Update screen
    pygame.display.flip()

pygame.quit()
sys.exit()