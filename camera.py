import pygame

class camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.state = pygame.Rect(0, 0, screen_width, screen_height) 
        
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height

    def apply(self, target_rect):
        # Moves the target rect by the negative of the camera's offset.
        offset_x = int(self.state.left)
        offset_y = int(self.state.top)
        return target_rect.move(-offset_x, -offset_y)
    
    def screen_to_world(self, screen_pos):
        screen_x, screen_y = screen_pos
        # The world position is the screen position plus the camera's offset
        world_x = screen_x + self.state.left
        world_y = screen_y + self.state.top
        # Using Vector2 is useful for math calculations
        return pygame.Vector2(world_x, world_y)

    def update(self, target):
        SMOOTHING = 0.05
        target_left_x = target.rect.centerx - self.screen_width // 2
        target_top_y = target.rect.centery - self.screen_height // 2


        self.state.left += (target_left_x - self.state.left) * SMOOTHING
        self.state.top += (target_top_y - self.state.top) * SMOOTHING

        # Clamp
        max_x = self.world_width - self.screen_width
        max_y = self.world_height - self.screen_height
        self.state.left = max(0, min(self.state.left, max_x))
        self.state.top = max(0, min(self.state.top, max_y))
        self.state.left = int(self.state.left)
        self.state.top = int(self.state.top)