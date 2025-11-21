import pygame
import os

class player:
    def __init__(self, x, y, speed=300):
        idle_path = os.path.join("assets", "player", "00.png")
        self.idle_frame = pygame.image.load(idle_path).convert_alpha()

        # Animation
        self.frames = []
        for i in range(1, 7):
            path = os.path.join("assets", "player", f"{i:02}.png")
            image = pygame.image.load(path).convert_alpha()
            self.frames.append(image)

        self.image = self.idle_frame
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed  # Current speed (can be changed anytime)

        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.1

        # Facing direction
        self.facing_right = False

    def set_speed(self, new_speed):
        self.speed = new_speed

    def handle_input(self, keys, dt):
        movement = pygame.Vector2(0, 0)
        direction_keys = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0),
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1)
        }

        moving = False
        for key, vector in direction_keys.items():
            if keys[key]:
                movement += pygame.Vector2(vector)
                moving = True

        # Update facing direction
        if movement.x > 0:
            self.facing_right = True
        elif movement.x < 0:
            self.facing_right = False

        if movement.length() != 0:
            movement = movement.normalize()
            self.rect.center += movement * self.speed * dt

        # Update animation
        if moving:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_speed:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
        else:
            self.image = self.idle_frame

    def draw(self, surface):
        img = pygame.transform.flip(self.image, True, False) if self.facing_right else self.image
        surface.blit(img, self.rect)
