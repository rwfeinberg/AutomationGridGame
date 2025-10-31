import pygame

class Button:

    # size = (width, height)
    # colors = bg_color, text_color
    def __init__(self, x, y, size, clickFunction=None, text="Text", textSize=24, colors=[(120, 120, 120), (0, 0, 0)], hold=False):
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.colors = colors
        self.clickFunction = clickFunction
        self.font = pygame.font.Font('Futura Bold.otf', textSize)
        self.text = text
        self.hold = hold
        self.alreadyPressed = False
        
        self.enabled = True

        self.surf = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.textSurf = self.font.render(self.text, True, colors[1])
    
    
    def __str__(self):
        print(f"{self.text}@{self.x},{self.y}")
        pass
    
    def update(self):
        mousePos = pygame.mouse.get_pos()

        # If hovered
        if self.enabled:
            if self.rect.collidepoint(mousePos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                # If clicked
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    if self.hold:
                        self.clickFunction()
                    elif not self.alreadyPressed:
                        self.clickFunction()
                        self.alreadyPressed = True
                else:
                    self.alreadyPressed = False
    
    def disable(self):
        self.enabled = False

    def draw(self, background):
        # Draw button
        self.surf.fill(self.colors[0])
        self.surf.blit(self.textSurf, [self.rect.width/2 - self.textSurf.get_rect().width/2, self.rect.height/2 - self.textSurf.get_rect().height/2])
        background.blit(self.surf, self.rect)