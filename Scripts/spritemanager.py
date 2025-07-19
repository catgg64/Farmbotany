import pygame

class SpriteManagerContext:
    def __init__(self, screen):
        self.screen = screen

class SpriteData:
    def __init__(self, surface, top_left_x, top_left_y, bottom_right_x, botton_right_y):
        self.surface = surface
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.botton_right_x = bottom_right_x
        self.botton_right_y = botton_right_y

def update_sprite_list(surface, sprite_list, offset_x, offset_y, window_size):
    for sprite in sprite_list:
        if sprite.botton_right_x + offset_x > 0 and sprite.botton_right_y + offset_y > 0 and (sprite.top_left_x - offset_x - 50) < window_size[1] and (sprite.top_left_y - offset_y - 50) < window_size[0]:
            surface.blit(sprite.surface, (sprite.top_left_x - offset_x, sprite.top_left_y - offset_y))
