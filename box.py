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
        # Make box grey
        self.surf.fill(color)

        # Write level to box
        font = pygame.freetype.Font("Futura Bold.otf", 42)
        fontsurf, fontrect = font.render(str(self.level), (0, 0, 0))
        self.surf.blit(fontsurf, fontsurf.get_rect(center=(self.size//2, self.size//2)))

        # Draw box on map
        background.blit(self.surf, self.rect)
    
    # Increase level and re-draw
    def upgrade(self, background, color):
        self.level += 1
        self.draw(background, color)
        
        
        
        
        
        
