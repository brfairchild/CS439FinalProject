import pygame
import math
from base_bullet import Bullet

class CircleBurstPattern:
    def __init__(self, **kwargs):
        spawn_x = kwargs.get("x", 640)
        spawn_y = kwargs.get("y", 80)
        
        self.center = pygame.Vector2(spawn_x, spawn_y) # Use the determined coordinates

        self.timer = 0.0
        self.burst_interval = kwargs.get("burst_interval", 0.5) 
        self.time_since_last_burst = 0.0

        self.bullets_per_circle = kwargs.get("bullets_per_circle", 80)
        self.gap_frequency = kwargs.get("gap_frequency", 7) 
        self.bullet_speed = kwargs.get("bullet_speed", 325)

        self.duration = kwargs.get("duration", 3.0) 
        self.finished = False


    def update(self, dt):
        self.timer += dt
        self.time_since_last_burst += dt
        new_bullets = []

        # End pattern
        if self.timer >= self.duration:
            self.finished = True
            return new_bullets

        # Time for a new burst
        if self.time_since_last_burst >= self.burst_interval:
            self.time_since_last_burst = 0

            angle_step = 360 / self.bullets_per_circle

            for i in range(self.bullets_per_circle):
                if i % self.gap_frequency == 0:
                    continue 

                angle_deg = i * angle_step
                angle_rad = math.radians(angle_deg)

                direction = pygame.Vector2(
                    math.cos(angle_rad),
                    math.sin(angle_rad)
                )

                new_bullet = Bullet(
                    # Bullets originate at self.center
                    self.center.x,
                    self.center.y,
                    direction,
                    speed=self.bullet_speed
                )

                # Play sound once per burst
                if i == 1:
                    new_bullet.play_sound_once()

                new_bullets.append(new_bullet)

        return new_bullets