import pygame
import os
import math

class attack:
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    def __init__(self, player_ref, target_world_pos): 
        self.player_ref = player_ref
        self.target_world_pos = target_world_pos
        
        # Load and play the sound
        sound_path = os.path.join("assets", "player", "attack", "wosh.mp3")
        try:
            self.sound = pygame.mixer.Sound(sound_path)
            self.sound.play()
        except pygame.error as e:
            print(f"Could not load or play sound: {e}")
            self.sound = None


        self.frames = []
        for i in range(9):
            path = os.path.join("assets", "player", "attack", f"{i}.png")
            img = pygame.image.load(path).convert_alpha()
            width = img.get_width() * 2
            height = img.get_height() * 2
            img = pygame.transform.scale(img, (width, height))
            self.frames.append(img)

        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.05 
        self.finished = False
        self.angle = 0
        self.offset_distance = 100

        player_center = pygame.Vector2(self.player_ref.rect.center)
        target_vec = self.target_world_pos - player_center
        
        if target_vec.length() == 0:
            direction_vec = pygame.Vector2(1, 0)
        else:
            direction_vec = target_vec.normalize()
            
        # First Angle calculation (in degrees)
        self.angle = math.degrees(math.atan2(-target_vec.y, target_vec.x))
        self.rect = self.frames[0].get_rect()
        self.rect.centerx = player_center.x + direction_vec.x * self.offset_distance
        self.rect.centery = player_center.y + direction_vec.y * self.offset_distance

        self.hitbox = self.rect.copy()

    def update(self, dt):
        player_center = pygame.Vector2(self.player_ref.rect.center)
        # Vector from player's current position to the mouse
        target_vec = self.target_world_pos - player_center
        
        if target_vec.length() != 0:
            direction_vec = target_vec.normalize()

            # Update the attack's center position
            self.rect.centerx = player_center.x + direction_vec.x * self.offset_distance
            self.rect.centery = player_center.y + direction_vec.y * self.offset_distance
            self.angle = math.degrees(math.atan2(-target_vec.y, target_vec.x))
        
        self.frame_timer += dt
        if self.frame_timer >= self.frame_speed:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True 

    def draw(self, surface, camera):
        original_image = self.frames[self.current_frame]
        rotated_image = pygame.transform.rotate(original_image, self.angle)
        
        # Recalculate the position to center
        new_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, camera.apply(new_rect))