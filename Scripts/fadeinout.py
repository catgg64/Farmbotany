import pygame
import tweener

class FadeInOut:
    def __init__(self, surface, screen_width, screen_height):
        self.surface = surface
        self.fade_surface = pygame.Surface((screen_height * 2, screen_width * 2), pygame.SRCALPHA)
        self.rect = pygame.Rect(0, 0, screen_height * 2, screen_width * 2)

        self.tween = tweener.Tween(0, 255, 500, tweener.Easing.QUAD, tweener.EasingMode.IN, True, False, 1)
        
        self.transperency = 0


    def update(self, surface):
        self.tween.update()
        self.transperency = self.tween.value        

        self.fade_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.fade_surface, (0, 0, 0, int(self.transperency)), self.rect)
        surface.blit(self.fade_surface, (0, 0))
        
    def fade(self):
        self.tween.start()