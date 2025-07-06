import pygame

class FBButton:
    def __init__(self, pos_x, pos_y, size_x, size_y):
        self.rect = pygame.Rect(pos_x, pos_y, size_x, size_y)
        self.state: str = "none"
        self.pressed: bool = False

    def update(self, surface, color, hover_color, pressed_color):
        self.pressed = False

        if self.state == "none":
            pygame.draw.rect(surface, color, self.rect, 0)
        elif self.state == "hover":
            pygame.draw.rect(surface, hover_color, self.rect, 0)
        elif self.state == "pressed":
            pygame.draw.rect(surface, pressed_color, self.rect)
        
        mouse_pos = pygame.mouse.get_pos()
        left_mouse_down = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse_pos):
            self.state = "hover"
            if left_mouse_down:
                self.state = "pressed"
                self.pressed = True
        else:
            self.state = "none"