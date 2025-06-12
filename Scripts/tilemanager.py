import pygame
import os

tiles = {
    "1": [{"name": "grass", "texture": "Sprites/tile_set.png", "requires_rect": True, "rect_x": 16, "rect_y": 48, "size_x": 16, "size_y": 16}],
    "2": [{"name": "dirt", "texture": "Sprites/tile_set.png", "requires_rect": True, "rect_x": 64, "rect_y": 48, "size_x": 16, "size_y": 16}],
    "3": [{"name": "empty", "texture": "Sprites/tile_set.png", "requires_rect": True, "rect_x": 48, "rect_y": 16,"size_x": 16, "size_y": 16}]
}
#
# class TileData:
#     def __init__(self,  id):
#         self.id = id
#
#
# def setup_tile_data(weight, length):
#     tile_list = [None] * weight * length
#     for x in range(0, weight * length):
#         tile_list[x] = TileData("0")
#     return tile_list
#
# def position_to_tile_value(x, y, weight, length, tile_size):
#     result = round((x / tile_size)) + round((y / tile_size))
#
#     return result
#
# def tile_value_to_position(tile_value, width, tile_size):
#     x = round(tile_value & width) * tile_size
#     y = round(tile_value // width) * tile_size
#
#     return (x, y)
#
# def draw_tilemap(tile_list, width, screen, tile_size):
#     for tile in tile_list:
#         if tiles[tile.id][0]["requires_rect"] == False:
#             print("stamp")
#             print(tile_value_to_position(tile_list.index(tile), width, tile_size))
#             screen.blit(pygame.image.load(tiles[tile.id][0]["texture"]), tile_value_to_position(tile_list.index(tile), width, tile_size))
#         if tiles[tile.id][0]["requires_rect"] == True:
#             rect = pygame.Rect([tiles[tile.id][0]["rect_x"], tiles[tile.id][0]["rect_y"], tiles[tile.id][0]["size_x"], tiles[tile.id][0]["size_y"]])
#             screen.blit(pygame.image.load(tiles[tile.id][0]["texture"]).subsurface(rect), tile_value_to_position(tile_list.index(tile), width, tile_size))
#
#
def setup_surfaces(tile_exspansion):
    for tile_id, tile_data in tiles.items():
        for tile in tile_data:
            try:
                # Verify file exists
                if not os.path.exists(tile["texture"]):
                    raise FileNotFoundError(f"Sprite sheet {tile['texture']} not found")
                # Load image into a Surface

                surface = pygame.image.load(tile["texture"]).convert_alpha()

                if tile["requires_rect"]:
                    rect = pygame.Rect(tile["rect_x"], tile["rect_y"], tile["size_x"], tile["size_y"])
                    # Verify rect is valid
                    if not surface.get_rect().contains(rect):
                        raise ValueError(f"Rectangle {rect} is outside sprite sheet bounds {surface.get_rect()}")
                    tile["surface"] = surface.subsurface(rect)
                else:
                    tile["surface"] = surface
                del tile["texture"]  # Remove path to avoid misuse
                tile["surface"] = pygame.transform.scale(tile["surface"], (tile_exspansion, tile_exspansion))
            except (pygame.error, FileNotFoundError, ValueError) as e:
                print(f"Error loading texture for tile {tile_id}: {e}")
                tile["surface"] = pygame.Surface((16, 16))  # Fallback surface
                tile["surface"].fill((255, 0, 0))  # Red for debugging
                del tile["texture"]

class TileData:
    def __init__(self, sub_id, id):
        self.id = id
        self.sub_id = sub_id

def setup_tile_data(width, length):
    return [TileData("1", "1") for _ in range(width * length)]  # Use valid ID "1"

def position_to_tile_value(x, y, width, length, tile_size):
    grid_x = x // tile_size
    grid_y = y // tile_size
    if 0 <= grid_x < width and 0 <= grid_y < length:
        return grid_y * width + grid_x
    return -1

def tile_value_to_position(tile_value, width, tile_size):
    x = (tile_value % width) * tile_size
    y = (tile_value // width) * tile_size
    return (x, y)

def draw_tilemap(tile_list, width, screen, tile_size):
    drawn_tiles = 0
    for index, tile in enumerate(tile_list):
        if tile.id not in tiles:
            print(f"Warning: Tile ID {tile.id} not found at index {index}")
            continue
        tile_data = tiles[tile.id][0]
        sub_id_tile_data = tiles[tile.sub_id][0]
        pos = tile_value_to_position(index, width, tile_size)
        screen.blit(sub_id_tile_data["surface"], pos)
        screen.blit(tile_data["surface"], pos)

        drawn_tiles += 1
        # Debug: Print first few tile positions
        #if index < 5:
        #    print(f"Drawing tile {tile.id} at {pos}")
    #print(f"Total tiles drawn: {drawn_tiles}")