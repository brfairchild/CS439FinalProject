import pygame
import os

class Boss(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.MOVEMENT_SPEED = 50
        self.TARGET_Y = 80
        

        boss_png = os.path.join("assets", "boss.png")
        
        try:
            # Load the image
            original_image = pygame.image.load(boss_png).convert_alpha()
            
            # Define desired size for the boss (e.g., 100x100)
            self.width = 100
            self.height = 100
            
            # Scale the image
            self.image = pygame.transform.scale(original_image, (self.width, self.height))
            
        except pygame.error as e:
            self.width = 100
            self.height = 100
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill((255, 0, 0))
        
        self.rect = self.image.get_rect()
        
        # Movement
        self.current_target = 0
        self.targets = [
            screen_width // 2,
            screen_width - (self.width // 2) - 50,
            (self.width // 2) + 50
        ]
        
        # Set initial position to center top
        self.rect.centerx = self.targets[0]
        self.rect.y = self.TARGET_Y
        self.health = 100
        self.alive = True
        
        self.is_moving = False

    def update(self, dt):
        if not self.alive or not self.is_moving:
            return
            
        target_x = self.targets[self.current_target]
        
        # Calculate the vector towards the target
        direction_x = target_x - self.rect.centerx
        distance = abs(direction_x)
        
        # Checks if boss is close to the target position and sets the next one if he is
        if distance < 5:
            # Switch target
            if self.current_target == 0:
                self.current_target = 1
            elif self.current_target == 1:
                self.current_target = 2
            elif self.current_target == 2:
                self.current_target = 1
                
            # Stop movement after reaching the target
            self.is_moving = False  
            
        else:
            # Move towards the target
            move_amount = self.MOVEMENT_SPEED * dt
            # Move Right
            if direction_x > 0: # Move Right
                self.rect.centerx += min(move_amount, distance)
                
            # Move Left
            else:
                self.rect.centerx -= min(move_amount, distance)

    def draw(self, surface):
        surface.blit(self.image, self.rect)