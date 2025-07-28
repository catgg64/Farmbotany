import pygame

class SpriteManagerContext:
    def __init__(self, screen):
        self.screen = screen

class SpriteData:
    def __init__(self, surface, top_left_x, top_left_y, bottom_right_x, botton_right_y, y_sort=False, y_sort_x=2763, y_sort_y=2763): # 2763 sets it to the default value. Don't ask me why. Because it's a secret.
        self.surface = surface
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.botton_right_x = bottom_right_x
        self.botton_right_y = botton_right_y
        self.y_sort_x = y_sort_x
        self.y_sort_y = y_sort_y
        if self.y_sort_x == 2763:
            self.y_sort_x = self.botton_right_x
        if self.y_sort_y == 2763:
            self.y_sort_y = self.botton_right_y
        self.y_sort = y_sort

def update_sprite_list(surface, sprite_list, offset_x, offset_y, window_size):
    for sprite in sprite_list:
        if (sprite.botton_right_x + offset_x + 50) > 0 and (sprite.botton_right_y + offset_y + 50) > 0 and (sprite.top_left_x - offset_x - 50) < window_size[0] and (sprite.top_left_y - offset_y - 50) < window_size[1]:
            surface.blit(sprite.surface, (sprite.top_left_x - offset_x, sprite.top_left_y - offset_y))
        
# Sorts a Sprite list dictionary in base of index position.
#def sort_sprite_list(list, sort_idx):
#    for list_part_idx, list_part in enumerate(list):
#        item = list[sort_idx].top_left_y
#        if list_part_idx < len(list):
#            past_item = list[list_part_idx - 1].top_left_y
#            if past_item > item:

