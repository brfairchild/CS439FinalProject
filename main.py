import pygame
import sys
import os
from player import player
from attack import attack
from base_bullet import Bullet
from circleburst import CircleBurstPattern
from spiral import SpiralPattern
from playerbullet import PlayerBullet


# Initialize
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CS439_FinalProject_BraydenFairchild")

clock = pygame.time.Clock()


# Load background
background_path = os.path.join("assets", "map.png")
background_image = pygame.image.load(background_path).convert()



# Initialize player
player = player(SCREEN_WIDTH // 2, SCREEN_HEIGHT)
attacks = []
bullets = []  # Enemy
friendly_bullets = []  # Player
active_patterns = []




# Pattern sequence
pattern_sequence = [
    {
        "class": CircleBurstPattern,
        "params": {
            "x": SCREEN_WIDTH // 2,
            "y": 80,
            "bullet_speed": 400,
            "duration": 3.0
        }
    },
    {
        "class": SpiralPattern,
        "params": {
            "start_x": SCREEN_WIDTH // 2,
            "start_y": 80,
            "bullet_speed": 350,
            "duration": 2.0
        }
    }
]
current_pattern_index = 0



# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not player.is_attacking:
                # Always aim at top-center
                target_pos_screen = pygame.Vector2(SCREEN_WIDTH // 2, 0)
                new_attack = attack(player, target_pos_screen)
                attacks.append(new_attack)
                new_attack.play_sound_once()
                player.is_attacking = True

    keys = pygame.key.get_pressed()

    # Spawn next pattern if none active
    if not active_patterns:
        pattern_info = pattern_sequence[current_pattern_index]
        PatternClass = pattern_info["class"]
        params = pattern_info.get("params", {})

        # Instantiate the pattern with all parameters
        active_patterns.append(PatternClass(**params))
        # Move to next pattern in sequence
        current_pattern_index = (current_pattern_index + 1) % len(pattern_sequence)

    # Player input
    player.handle_input(keys, dt, SCREEN_WIDTH, SCREEN_HEIGHT)


    # Update attacks
    for atk in attacks[:]:
        atk.update(dt)
        if atk.finished:
            attacks.remove(atk)
            player.is_attacking = False

    # Update patterns and spawn bullets
    for pattern in active_patterns[:]:
        new_bullets = pattern.update(dt)
        bullets.extend(new_bullets)
        if pattern.finished:
            active_patterns.remove(pattern)

    # Update enemy bullets and check collisions
    for bullet in bullets[:]:
        bullet.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT)
        # Check collision with player
        if player.alive and player.check_collision(bullet):

            # Clear all bullets when player is hit
            bullets.clear()
            break

        # Reflection
        reflected = False
        for atk in attacks:
            if bullet.check_collision(atk.hitbox):
                reflected = True
                break

        if reflected:
            reflected_vector = -bullet.direction
            new_friendly_bullet = PlayerBullet(
                bullet.rect.centerx,
                bullet.rect.centery,
                reflected_vector
            )
            friendly_bullets.append(new_friendly_bullet)
            bullets.remove(bullet)
        elif not bullet.alive:
            bullets.remove(bullet)

    # Update friendly bullets
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

    for bullet in bullets:
        bullet.draw(window)

    for f_bullet in friendly_bullets:
        f_bullet.draw(window)

    pygame.display.flip()

pygame.quit()
sys.exit()
