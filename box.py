import pygame
import pygame.freetype

class Box:
    def __init__(self, level, closest_x, closest_y, box_size):
        self.level = level
        self.rect = pygame.Rect(closest_x, closest_y, box_size, box_size)
        self.id = f"{self.level},{self.rect.x}{self.rect.y}"
    
    def __str__(self):
        return f"{self.id}"
    
    def draw(self, background, color):
        rect_surf = pygame.Surface(self.rect.size)
        # font = pygame.freetype.Font("arial.ttf", 42)
        # font.render_to(rect_surf, (0, 0), "TEST", (0, 0, 0))
        
        pygame.draw.rect(rect_surf, color, rect_surf.get_rect())
        background.blit(rect_surf, self.rect)
        
        
        
        
        
        
