import pygame

class Brick:
    def __init__(self, x, y, size_x, size_y):
        self.rect = pygame.Rect(x, y, size_x, size_y)
    
    def append_self_to_list(self, list):
        list.append(self)

    def is_colliding_with_rect(self, rect):
        if self.rect.colliderect(rect):
            return True
        else:
            return False
    
    def update(self, surface, pos_x, pos_y, offset_x, offset_y):
        sim_rect = pygame.Rect(pos_x - offset_x, pos_y - offset_y, self.rect.bottom, self.rect.right)
        pygame.draw.rect(surface, (100, 100, 100), sim_rect, 5)


def update_solid_object_tilemap(tilemap, solid_objects_list, tile_size):
    for row_idx, row in enumerate(tilemap):
        for column_idx, column in enumerate(row):
            solid_objects_list.append(Brick(row_idx * tile_size, column_idx * tile_size))