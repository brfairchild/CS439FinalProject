import pygame
import sys
import os
from player import player as PlayerClass # just to make call for restart
from attack import attack
from base_bullet import Bullet
from circleburst import CircleBurstPattern
from spiral import SpiralPattern
from playerbullet import PlayerBullet
from boss import Boss 

# Initialize
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CS439_FinalProject_BraydenFairchild")
clock = pygame.time.Clock()


# Game States
GAME_STATE_PLAYING = "playing"
GAME_STATE_GAMEOVER = "game_over"
game_state = GAME_STATE_PLAYING 

# Boss time
BOSS_MOVE_INTERVAL = 5.0
boss_move_timer = 0.0

# Score
score = 0
SCORE_PER_HIT = 100

# Load background
background_path = os.path.join("assets", "map.png")
background_image = pygame.image.load(background_path).convert()

# Initialize Fonts for Game Over Screen
try:
    font_path = pygame.font.match_font('arial')
except:
    font_path = None 

main_font = pygame.font.Font(font_path, 72)
small_font = pygame.font.Font(font_path, 36)
score_font = pygame.font.Font(font_path, 30)

# Global boss
boss = None

# ================================================================== RESET
def reset_game():
    global player, attacks, bullets, friendly_bullets, active_patterns, current_pattern_index, game_state, boss, boss_move_timer, score
    
    player = PlayerClass(SCREEN_WIDTH // 2, SCREEN_HEIGHT)
    boss = Boss(SCREEN_WIDTH, SCREEN_HEIGHT)

    attacks = []
    bullets = []
    friendly_bullets = []
    active_patterns = []
    current_pattern_index = 0
    game_state = GAME_STATE_PLAYING
    boss_move_timer = 0.0
    score = 0
reset_game()


# ================================================================== PATTERN
pattern_sequence = [
    {
        "class": CircleBurstPattern,
        "params": {
            "bullet_speed": 400,
            "duration": 3.0
        }
    },
    {
        "class": SpiralPattern,
        "params": {
            "bullet_speed": 350,
            "duration": 2.0
        }
    },
    {
        "class": CircleBurstPattern,
        "params": {
            "bullet_speed": 200,
            "duration": 2.0
        }
    },
    {
        "class": SpiralPattern,
        "params": {
            "bullet_speed": 200,
            "duration": 2.0
        }
    },
    {
        "class": SpiralPattern,
        "params": {
            "bullet_speed": 400,
            "duration": 2.0
        }
    }
]

# ================================================================== GAME OVER
def draw_game_over_screen(surface):
    s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    s.set_alpha(150)
    s.fill((0, 0, 0))
    surface.blit(s, (0, 0))

    title_text = main_font.render("GAME OVER", True, (255, 0, 0))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    surface.blit(title_text, title_rect)

    final_score_text = small_font.render(f"Final Score: {score}", True, (255, 255, 255))
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(final_score_text, final_score_rect)
    
    instruction_text = small_font.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    surface.blit(instruction_text, instruction_rect)

# Score Draw
def draw_score(surface):
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    surface.blit(score_text, score_rect)


# ================================================================== MAIN LOOP
running = True
while running:
    dt = clock.tick(60) / 1000
    
# ================================================================== EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == GAME_STATE_PLAYING:
            # Check for attack key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.is_attacking:
                    
                    # Adjust player attack towards boss
                    if boss:
                        target_pos_screen = pygame.Vector2(boss.rect.centerx, boss.rect.centery)
                    else:
                        target_pos_screen = pygame.Vector2(SCREEN_WIDTH // 2, 0) # goto the center top of the screen

                    new_attack = attack(player, target_pos_screen)
                    attacks.append(new_attack)
                    new_attack.play_sound_once()
                    player.is_attacking = True

# ================================================================== GAME OVER INPUT
        elif game_state == GAME_STATE_GAMEOVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False


    keys = pygame.key.get_pressed()
    
# ================================================================== GAME LOGIC
    if game_state == GAME_STATE_PLAYING:
        
        # Boss timer
        boss_move_timer += dt
        if boss_move_timer >= BOSS_MOVE_INTERVAL:
            # Move and reset timer
            boss.is_moving = True
            boss_move_timer = 0.0
            
        # Update boss position
        boss.update(dt) 
        
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
        
# ================================================================== PATTERN
        if not active_patterns:
            
            pattern_info = pattern_sequence[current_pattern_index]
            PatternClass = pattern_info["class"]
            
            # Copy boss position
            params = pattern_info["params"].copy() 
            boss_x = boss.rect.centerx
            boss_y = boss.rect.centery
            if PatternClass == CircleBurstPattern:
                 params["x"] = boss_x
                 params["y"] = boss_y
            elif PatternClass == SpiralPattern:
                 params["start_x"] = boss_x
                 params["start_y"] = boss_y


            active_patterns.append(PatternClass(**params))
            
            # Loop to next pattern
            current_pattern_index = (current_pattern_index + 1) % len(pattern_sequence)


        # Update enemy bullets and check collisions
        for bullet in bullets[:]:
            bullet.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT)
            
            if player.alive and player.check_collision(bullet):
                bullets.clear()
                break

            if not player.alive:
                game_state = GAME_STATE_GAMEOVER
                bullets.clear() 
                friendly_bullets.clear()
                active_patterns.clear()
                break 

            # Reflection of friendly bullets
            reflected = False
            for atk in attacks:
                if bullet.check_collision(atk.hitbox):
                    reflected = True
                    break

            if reflected:
# ================================================================== BULLET TOWARDS THE BOSS
                boss_pos = pygame.Vector2(boss.rect.centerx, boss.rect.centery)
                bullet_pos = pygame.Vector2(bullet.rect.centerx, bullet.rect.centery)
                
                direction_to_boss = boss_pos - bullet_pos
                
                if direction_to_boss.length_squared() > 0.0001:
                    final_direction_vector = direction_to_boss.normalize()
                else:
                    final_direction_vector = pygame.Vector2(0, -1) 
                
                
                new_friendly_bullet = PlayerBullet(
                    bullet.rect.centerx,
                    bullet.rect.centery,
                    final_direction_vector
                )
                friendly_bullets.append(new_friendly_bullet)
                bullets.remove(bullet)
            elif not bullet.alive:
                bullets.remove(bullet)

# ================================================================== UPDATE BULLETS
        for f_bullet in friendly_bullets[:]:
            f_bullet.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT)
            
            # Check for collision with the boss and add points and delete the bullet
            if boss.rect.colliderect(f_bullet.hitbox):
                score += SCORE_PER_HIT
                f_bullet.alive = False
            if not f_bullet.alive:
                friendly_bullets.remove(f_bullet)


# ================================================================== DRAWING
    
    if background_image:
        window.blit(background_image, (0, 0))
    else:
        window.fill((30, 30, 30))
        
    if game_state == GAME_STATE_PLAYING:
        boss.draw(window) 
        
        player.draw(window)

        for atk in attacks:
            atk.draw(window)

        for bullet in bullets:
            bullet.draw(window)

        for f_bullet in friendly_bullets:
            f_bullet.draw(window)
            

        draw_score(window) 
            
    elif game_state == GAME_STATE_GAMEOVER:
        if background_image:
            window.blit(background_image, (0, 0))
        else:
            window.fill((30, 30, 30))
            
        draw_game_over_screen(window)

    pygame.display.flip()

pygame.quit()
sys.exit()