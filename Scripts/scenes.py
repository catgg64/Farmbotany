import pygame
import tilemanager

class Room:
    def __init__(self, world, sub_world, special_tiles_world):
        self.world = world
        self.sub_world = sub_world
        self.special_tiles_world = special_tiles_world

    #def update(self, surface):
    #    tilemanager.update_tile_map()