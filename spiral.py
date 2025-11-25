# spiral.py (or patterns/pattern_spiral.py)

from base_bullet import Bullet
import pygame
import math

class SpiralPattern:
    def __init__(self, start_x, start_y):
        self.center = pygame.Vector2(start_x, start_y)
        self.timer = 0.0
        self.spawn_rate = 0.05
        self.time_since_last_spawn = 0.0
        self.total_bullets_fired = 0
        self.max_duration = 15

        # Sound Cooldown Control: Play sound only once per second
        self.bullet_sound_cooldown = 0.05
        self.time_since_last_sound = 0.0
        
        self.finished = False

        # Parameters for slower, reversing spin
        self.base_angle_rate = 23.0  
        self.oscillation_frequency = 0.5
        self.current_cumulative_angle = 0.0
        self.bullet_speed = 250 

    def update(self, dt):
        self.timer += dt
        self.time_since_last_spawn += dt
        self.time_since_last_sound += dt
        new_bullets = []
        
        if self.timer >= self.max_duration:
            self.finished = True
            return new_bullets
            
        # Dynamic angle agjustment
        speed_multiplier = math.sin(self.timer * 2 * math.pi * self.oscillation_frequency)
        angle_change = self.base_angle_rate * speed_multiplier * dt * 60 
        self.current_cumulative_angle += angle_change
        
        
        # Spawn
        if self.time_since_last_spawn >= self.spawn_rate:
            self.time_since_last_spawn = 0
            self.total_bullets_fired += 1
            
            angle_degrees_base = self.current_cumulative_angle 
            angle_rad_base = math.radians(angle_degrees_base)
            
            # Bullet 1
            direction1 = pygame.Vector2(math.cos(angle_rad_base), math.sin(angle_rad_base))
            # Bullet 2
            angle_rad_offset = math.radians(angle_degrees_base + 180)
            direction2 = pygame.Vector2(math.cos(angle_rad_offset), math.sin(angle_rad_offset))
            
            # Create bullets
            new_bullet1 = Bullet(self.center.x, self.center.y, direction1, speed=self.bullet_speed)
            new_bullet2 = Bullet(self.center.x, self.center.y, direction2, speed=self.bullet_speed)
            
            # Only play the sound if the cooldown has elapsed
            if self.time_since_last_sound >= self.bullet_sound_cooldown:
                new_bullet1.play_sound_once() 
                self.time_since_last_sound = 0
            
            new_bullets.append(new_bullet1)
            new_bullets.append(new_bullet2)
            
        return new_bullets