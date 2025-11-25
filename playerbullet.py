# playerbullet.py

import pygame
import math

class PlayerBullet:
    def __init__(self, x, y, direction_vector, size=32, speed=500):
        self.size = size
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.fill((0, 0, 255)) # Blue color
        
        self.rect = self.image.get_rect(center=(x, y))
        
        hitbox_size = 8
        self.hitbox = pygame.Rect(0, 0, hitbox_size, hitbox_size)
        self.hitbox.center = self.rect.center
        try:
            # Lets not divide by 0
            if direction_vector.length_squared() > 0.0001:
                self.direction = direction_vector.normalize()
            else:
                # If length is zero, use a default direction
                self.direction = pygame.Vector2(0, -1)
        except AttributeError:
            # Catch the error if direction_vector wasn't a vector object at all
            self.direction = pygame.Vector2(0, -1)
            
        self.speed = speed
        self.alive = True
        
        # Friendly bullets delete 
        self.lifespan = 5.0
        self.timer = 0.0

    def update(self, dt, screen_width, screen_height):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.alive = False
            return

        # Move the bullet
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

        # Update the hitbox position
        self.hitbox.center = self.rect.center

        # X
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.direction.x *= -1 # Reverse X direction
            # Keep bullet in bounds
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > screen_width:
                self.rect.right = screen_width
            
        # Y
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            self.direction.y *= -1 # Reverse Y direction
            # Keep bullet in bounds
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height

    def draw(self, surface):
        surface.blit(self.image, self.rect)