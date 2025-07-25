import pygame
import tilemanager

class Room:
    def __init__(self, world, sub_world, special_tiles_world, room_id, mincornerx, maxcornerx, mincornery, maxcornery, width, length):
        self.world = world
        self.sub_world = sub_world
        self.special_tiles_world = special_tiles_world
        self.room_id = room_id

        self.mincornerx = mincornerx
        self.maxcornerx = maxcornerx
        self.mincornery = mincornery
        self.maxcornery = maxcornery

        self.tile_world_width = width
        self.tile_world_length = length
        self.tile_size = 64

        self.tiles_world = []
        self.tiles_world = tilemanager.setup_tile_data(self.tile_world_width, self.tile_world_length)

        self.tile_slot_list = []

def update_all_screens_acording_to_new_screen(room_list):
    for room in room_list:
        room.maxcornerx = room.tile_world_width * room.tile_size - pygame.display.get_window_size()[0] / 2
        room.maxcornery = room.tile_world_length * room.tile_size - pygame.display.get_window_size()[1] / 2
        
