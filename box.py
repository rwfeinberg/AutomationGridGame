import pygame
import pygame.freetype

class Box:
    def __init__(self, level, closest_x, closest_y, box_size):
        self.level = level
        self.size = box_size
        self.surf = pygame.Surface((box_size, box_size))
        self.rect = self.surf.get_rect(topleft=(closest_x, closest_y))
        self.id = f"{self.level},{self.rect.x}{self.rect.y}"
    
    def __str__(self):
        return f"{self.id}"
    
    def draw(self, background, color):
        # font = pygame.freetype.Font("arial.ttf", 42)
        # font.render_to(rect_surf, (0, 0), "TEST", (0, 0, 0))
        self.surf.fill(color)
        background.blit(self.surf, self.rect)
        
        
        
        
        
        
