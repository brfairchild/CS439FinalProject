import pygame
import os

class attack:
    def __init__(self, x, y, facing_right):
        # Load and scale attack frames 0-8
        self.frames = []
        for i in range(9):
            path = os.path.join("assets", "player", "attack", f"{i}.png")
            img = pygame.image.load(path).convert_alpha()
            # Scale by 2
            width = img.get_width() * 2
            height = img.get_height() * 2
            img = pygame.transform.scale(img, (width, height))
            self.frames.append(img)

        self.facing_right = facing_right
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.05  # seconds per frame

        # Position in front of player
        offset = 100  # distance in front of player
        self.rect = self.frames[0].get_rect()
        if facing_right:
            self.rect.center = (x + offset, y)
        else:
            self.rect.center = (x - offset, y)

        self.finished = False
        self.hitbox = self.rect.copy()

    def update(self, dt):
        # Update animation
        self.frame_timer += dt
        if self.frame_timer >= self.frame_speed:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True  # attack animation done

    def draw(self, surface, camera):
        img = self.frames[self.current_frame]
        # Flip only if facing left
        img = pygame.transform.flip(img, True, False) if not self.facing_right else img
        surface.blit(img, camera.apply(self.rect))
        # Optional: draw hitbox for debugging
        # pygame.draw.rect(surface, (255, 0, 0), camera.apply(self.hitbox))
