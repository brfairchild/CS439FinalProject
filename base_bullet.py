# bullet_base.py

import pygame
import math
import os
import pathlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

class Bullet:
    def __init__(self, x, y, direction_vector, speed=400):
        image_path = os.path.join(BASE_DIR, "assets", "bullet1.png") # 🌟 Pathing fix applied
        bullet_image_size = 32
        
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, (bullet_image_size, bullet_image_size)) 
        except pygame.error as e:
            self.image = pygame.Surface((bullet_image_size, bullet_image_size)).convert_alpha()
            self.image.fill((255, 0, 0)) # Red fallback
            
        self.rect = self.image.get_rect(center=(x, y))
        
        # Hurtbox
        hitbox_size = 8 
        self.hitbox = pygame.Rect(0, 0, hitbox_size, hitbox_size)
        self.hitbox.center = self.rect.center
        
        self.direction = direction_vector.normalize() if direction_vector.length() > 0 else pygame.Vector2(0, -1)
        self.speed = speed
        self.alive = True
        
        # Sound
        sound_path = os.path.join(BASE_DIR, "assets", "bullet.wav")
        try:
            self.sound = pygame.mixer.Sound(sound_path)
        except pygame.error as e:
            print(f"FATAL AUDIO ERROR: Could not load sound from {sound_path}. Pygame error: {e}")
            self.sound = None
        
        self.sound_played = False


    def play_sound_once(self):
        if self.sound and not self.sound_played:
            self.sound.set_volume(0.2)
            self.sound.play()
            self.sound_played = True

    def update(self, dt, screen_width, screen_height):
        # Move the image rect
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

        # Update the hitbox position to match the image's new center
        self.hitbox.center = self.rect.center

        # Check if the bullet is off-screen (for cleanup)
        if (self.rect.left > screen_width or 
            self.rect.right < 0 or 
            self.rect.top > screen_height or 
            self.rect.bottom < 0):
            self.alive = False

    def check_collision(self, attack_rect):
        if self.hitbox.colliderect(attack_rect):
            return self.direction 
        return None

    def draw(self, surface):
        surface.blit(self.image, self.rect)