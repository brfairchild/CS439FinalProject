import pygame

class camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.rect = pygame.Rect(0, 0, screen_width, screen_height)
        self.world_width = world_width
        self.world_height = world_height

    def apply(self, target_rect):
        # Move whatever we draw relative to the camera's position
        return target_rect.move(-self.rect.left, -self.rect.top)

    def update(self, target):
        # How smooth the camera follows
        SMOOTHING = 0.07  # lower = more delay, higher = tighter follow

        # Smooth follow
        self.rect.centerx += (target.rect.centerx - self.rect.centerx) * SMOOTHING
        self.rect.centery += (target.rect.centery - self.rect.centery) * SMOOTHING

        # Clamp camera to world boundaries
        self.rect.left = max(0, min(self.rect.left, self.world_width - self.rect.width))
        self.rect.top = max(0, min(self.rect.top, self.world_height - self.rect.height))
