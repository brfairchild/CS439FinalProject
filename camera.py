import pygame

class camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.rect = pygame.Rect(0, 0, screen_width, screen_height)
        self.world_width = world_width
        self.world_height = world_height

    def apply(self, target_rect):
        return target_rect.move(-self.rect.left, -self.rect.top)

    def update(self, target):
        SMOOTHING = 0.1  # adjust for more or less delay

        # Smooth follow
        self.rect.centerx += (target.rect.centerx - self.rect.centerx) * SMOOTHING
        self.rect.centery += (target.rect.centery - self.rect.centery) * SMOOTHING

        # Clamp to world bounds
        self.rect.left = max(0, min(self.rect.left, self.world_width - self.rect.width))
        self.rect.top = max(0, min(self.rect.top, self.world_height - self.rect.height))
