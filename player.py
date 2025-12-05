import pygame
import os

class player:
    def __init__(self, x, y, speed=350):
        # Animation
        idle_path = os.path.join("assets", "player", "00.png")
        self.idle_frame = pygame.image.load(idle_path).convert_alpha()
        self.frames = []
        for i in range(1, 7):
            path = os.path.join("assets", "player", f"{i:02}.png")
            self.frames.append(pygame.image.load(path).convert_alpha())
        self.image = self.idle_frame
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.1
        self.facing_right = False
        self.is_attacking = False 

        # Focus image
        focus_path = os.path.join("assets", "focus.png")
        try:
            self.focus_image = pygame.image.load(focus_path).convert_alpha()
        except pygame.error:
            self.focus_image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(self.focus_image, (0, 255, 0, 128), (25, 25), 25)

        # Focus rotation
        self.focus_angle = 0
        self.focus_rotate_speed = 180  # degrees per second

        # Player state
        self.alive = True
        self.lives = 3

        # Hitbox
        hitbox_size = 24
        self.hitbox = pygame.Rect(0, 0, hitbox_size, hitbox_size)
        self.hitbox.center = self.rect.center

        # Load heart images
        heart_full_path = os.path.join("assets", "heart1.png")
        heart_empty_path = os.path.join("assets", "heart0.png")
        try:
            self.heart_full = pygame.image.load(heart_full_path).convert_alpha()
        except pygame.error:
            self.heart_full = pygame.Surface((32, 32))
            self.heart_full.fill((255, 0, 0))
        try:
            self.heart_empty = pygame.image.load(heart_empty_path).convert_alpha()
        except pygame.error:
            self.heart_empty = pygame.Surface((32, 32))
            self.heart_empty.fill((50, 50, 50))

    def check_collision(self, bullet):
        if self.alive and self.hitbox.colliderect(bullet.hitbox):
            self.lives -= 1
            if self.lives <= 0:
                self.alive = False
            return True
        return False

    def handle_input(self, keys, dt, world_width, world_height):
        if not self.alive:
            return  # Cannot move if dead

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

        if movement.x > 0:
            self.facing_right = True
        elif movement.x < 0:
            self.facing_right = False

        if movement.length() != 0:
            movement = movement.normalize()
            self.rect.center += movement * self.speed * dt

        # Adjust speed when holding shift
        if keys[pygame.K_LSHIFT]:
            self.speed = 100
            self.focus_angle += self.focus_rotate_speed * dt
        else:
            self.speed = 350

        # Keep in screen
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, world_width) 
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, world_height)

        # Keep hitbox centered on player
        self.hitbox.center = self.rect.center

        # Animation
        if moving: 
            self.frame_timer += dt
            if self.frame_timer >= self.frame_speed:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
        else:
            self.image = self.idle_frame

    def draw(self, surface):
        # Draw hearts
        for i in range(3):
            heart_img = self.heart_full if i < self.lives else self.heart_empty
            surface.blit(heart_img, (10 + i * (heart_img.get_width() + 5), 10))

        if self.alive:
            # Draw focus
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT]:
                rotated_focus = pygame.transform.rotate(self.focus_image, self.focus_angle)
                focus_rect = rotated_focus.get_rect(center=self.rect.center)
                surface.blit(rotated_focus, focus_rect)

            # Draw player sprite
            img = pygame.transform.flip(self.image, True, False) if self.facing_right else self.image
            surface.blit(img, self.rect)
        else:
            # Draw a red X if dead
            pygame.draw.line(surface, (255, 0, 0), self.rect.topleft, self.rect.bottomright, 4)
            pygame.draw.line(surface, (255, 0, 0), self.rect.topright, self.rect.bottomleft, 4)
