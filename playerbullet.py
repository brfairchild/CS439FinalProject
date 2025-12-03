import pygame
import math
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class PlayerBullet:
    def __init__(self, x, y, direction_vector, size=32, speed=500):
        self.size = size

        # Load player/reflected bullet image
        image_path = os.path.join(BASE_DIR, "assets", "bulletplayer.png")
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, (self.size, self.size))
        except pygame.error:
            # Fallback if image fails
            self.image = pygame.Surface((self.size, self.size)).convert_alpha()
            self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect(center=(x, y))

        # Hitbox
        hitbox_size = 8
        self.hitbox = pygame.Rect(0, 0, hitbox_size, hitbox_size)
        self.hitbox.center = self.rect.center

        try:
            if direction_vector.length_squared() > 0.0001:
                self.direction = direction_vector.normalize()
            else:
                self.direction = pygame.Vector2(0, -1)
        except AttributeError:
            self.direction = pygame.Vector2(0, -1)

        self.speed = speed
        self.alive = True

        # Lifespan
        self.lifespan = 5.0
        self.timer = 0.0

    def update(self, dt, screen_width, screen_height):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.alive = False
            return

        # Move bullet
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

        # Update hitbox
        self.hitbox.center = self.rect.center

        # Remove if off-screen
        if (self.rect.right < 0 or self.rect.left > screen_width or
            self.rect.bottom < 0 or self.rect.top > screen_height):
            self.alive = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
