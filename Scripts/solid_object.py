import pygame

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 64, 64)
    
    def append_self_to_list(self, list):
        list.append(self)

    def is_colliding_with_rect(self, rect):
        if self.rect.colliderect(rect):
            return True
        else:
            return False
    
    def update(self, surface):
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 0)


def update_solid_object_tilemap(tilemap, solid_objects_list, tile_size):
    for row_idx, row in enumerate(tilemap):
        for column_idx, column in enumerate(row):
            solid_objects_list.append(Brick(row_idx * tile_size, column_idx * tile_size))