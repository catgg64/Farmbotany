import pygame

class FBButton:
    def __init__(self, pos_x, pos_y, size_x, size_y, text):

        pygame.font.init()

        self.text_font = pygame.font.SysFont("Ariel", 30)

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.rect = pygame.Rect(pos_x, pos_y, size_x, size_y)
        self.state: str = "none"
        self.pressed: bool = False
        self.text = text

    def update(self, surface, color, hover_color, pressed_color, mouse_realeased):
        self.pressed = False


        if self.state == "none":
            pygame.draw.rect(surface, color, self.rect, 0)
        elif self.state == "hover":
            pygame.draw.rect(surface, hover_color, self.rect, 0)
        elif self.state == "pressed":
            pygame.draw.rect(surface, pressed_color, self.rect)
        
        mouse_pos = pygame.mouse.get_pos()
        left_mouse_down = pygame.mouse.get_pressed()[0]
        
        text = self.text_font.render(str(self.text), True, (255, 255, 255))
        surface.blit(text, (self.pos_x + self.size_x / 2, self.pos_y + self.size_y / 2))

        if self.rect.collidepoint(mouse_pos):
            self.state = "hover"
            if mouse_realeased:
                self.state = "pressed"
                self.pressed = True
        else:
            self.state = "none"