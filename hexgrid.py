import pygame
import math

class hexgrid:
    def __init__(self, hex_size):
        self.hex_size = hex_size
        self.width = hex_size * 2
        self.height = math.sqrt(3) * hex_size

    # Flat-top layout
    def hex_to_pixel(self, q, r):
        x = self.hex_size * 3/2 * q
        y = self.hex_size * math.sqrt(3) * (r + 0.5 * (q % 2))
        return (x, y)

    def draw_hex(self, surface, color, cx, cy):
        points = []
        for i in range(6):
            angle = math.radians(60 * i)
            px = cx + self.hex_size * math.cos(angle)
            py = cy + self.hex_size * math.sin(angle)
            points.append((px, py))

        pygame.draw.polygon(surface, color, points)
