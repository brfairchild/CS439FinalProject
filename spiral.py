from base_bullet import Bullet
import pygame
import math

class SpiralPattern:
    def __init__(self, **kwargs):     
        spawn_x = kwargs.get("start_x") or kwargs.get("x") or 640
        spawn_y = kwargs.get("start_y") or kwargs.get("y") or 80
        
        self.center = pygame.Vector2(spawn_x, spawn_y) # Use the determined coordinates

        self.timer = 0.0
        self.spawn_rate = kwargs.get("spawn_rate", 0.05)
        self.time_since_last_spawn = 0.0
        self.total_bullets_fired = 0
        self.max_duration = kwargs.get("duration", 5.0)

        # Sound cooldown
        self.bullet_sound_cooldown = kwargs.get("bullet_sound_cooldown", 0.05)
        self.time_since_last_sound = 0.0
        
        self.finished = False

        # Spin parameters
        self.base_angle_rate = kwargs.get("base_angle_rate", 23.0)
        self.oscillation_frequency = kwargs.get("oscillation_frequency", 0.5)
        self.current_cumulative_angle = 0.0
        self.bullet_speed = kwargs.get("bullet_speed", 250)


    def update(self, dt):
        self.timer += dt
        self.time_since_last_spawn += dt
        self.time_since_last_sound += dt
        new_bullets = []
        
        if self.timer >= self.max_duration:
            self.finished = True
            return new_bullets
            
        # Angle adjustment
        speed_multiplier = math.sin(self.timer * 2 * math.pi * self.oscillation_frequency)
        angle_change = self.base_angle_rate * speed_multiplier * dt * 60 
        self.current_cumulative_angle += angle_change
        
        # Spawn bullets
        if self.time_since_last_spawn >= self.spawn_rate:
            self.time_since_last_spawn = 0
            self.total_bullets_fired += 1
            
            angle_deg_base = self.current_cumulative_angle
            angle_rad_base = math.radians(angle_deg_base)
            
            direction1 = pygame.Vector2(math.cos(angle_rad_base), math.sin(angle_rad_base))
            direction2 = pygame.Vector2(math.cos(angle_rad_base + math.pi), math.sin(angle_rad_base + math.pi))
            
            # Bullets originate at self.center
            new_bullet1 = Bullet(self.center.x, self.center.y, direction1, speed=self.bullet_speed)
            new_bullet2 = Bullet(self.center.x, self.center.y, direction2, speed=self.bullet_speed)
            
            if self.time_since_last_sound >= self.bullet_sound_cooldown:
                new_bullet1.play_sound_once()
                self.time_since_last_sound = 0
            
            new_bullets.append(new_bullet1)
            new_bullets.append(new_bullet2)
            
        return new_bullets