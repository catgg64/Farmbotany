import pygame
import tilemanager

class Room:
    def __init__(self, world, sub_world, special_tiles_world, room_id):
        self.world = world
        self.sub_world = sub_world
        self.special_tiles_world = special_tiles_world
        self.room_id = room_id

        self.mincornerx = 0
        self.maxcornerx = 1800
        self.mincornery = 0
        self.maxcornery = 800
