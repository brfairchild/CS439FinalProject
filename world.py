import pygame
from hexgrid import hexgrid

class world:
    def __init__(self, hex_size, width, height):
        self.grid = hexgrid(hex_size)
        self.width = width
        self.height = height

        self.tiles = {}  # {(q,r): walkable_bool}
        self.generate()

    def generate(self):
        for q in range(self.width):
            for r in range(self.height):
                # Make the outer 1-tile border black (not walkable)
                if q == 0 or r == 0 or q == self.width-1 or r == self.height-1:
                    self.tiles[(q, r)] = False  # black / blocked
                else:
                    self.tiles[(q, r)] = True   # grey / walkable

    def draw(self, surface, camera):
        for (q, r), walkable in self.tiles.items():
            x, y = self.grid.hex_to_pixel(q, r)
            screen_rect = camera.apply(pygame.Rect(x, y, 1, 1))
            color = (80, 80, 80) if walkable else (10, 10, 10)
            self.grid.draw_hex(surface, color, screen_rect.x, screen_rect.y)

    def is_walkable(self, x, y):
        for (q, r), walkable in self.tiles.items():
            hx, hy = self.grid.hex_to_pixel(q, r)
            if abs(x - hx) < self.grid.hex_size and abs(y - hy) < self.grid.hex_size:
                return walkable
        return False
