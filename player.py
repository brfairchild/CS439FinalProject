import pygame
import os

class player:
    def __init__(self, x, y, speed=200):
        # Load idle frame
        idle_path = os.path.join("assets", "player", "00.png")
        self.idle_frame = pygame.image.load(idle_path).convert_alpha()

        # Load movement frames 01-06
        self.frames = []
        for i in range(1, 7):
            path = os.path.join("assets", "player", f"{i:02}.png")
            self.frames.append(pygame.image.load(path).convert_alpha())

        self.image = self.idle_frame
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

        # Animation
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.1

        self.facing_right = False

    def handle_input(self, keys, dt, world_width, world_height):
        movement = pygame.Vector2(0, 0)

        key_map = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0),
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1),
        }

        moving = False
        for key, vector in key_map.items():
            if keys[key]:
                movement += pygame.Vector2(vector)
                moving = True

        # Update facing direction
        if movement.x > 0:
            self.facing_right = True
        elif movement.x < 0:
            self.facing_right = False

        # Move player
        if movement.length() != 0:
            movement = movement.normalize()
            self.rect.center += movement * self.speed * dt

        # Clamp to world bounds
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, world_width)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, world_height)

        # Animate movement
        if moving:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_speed:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
        else:
            self.image = self.idle_frame

    def draw(self, surface, camera):
        img = pygame.transform.flip(self.image, True, False) if self.facing_right else self.image
        surface.blit(img, camera.apply(self.rect))
