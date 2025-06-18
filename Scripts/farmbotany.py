import pygame
from floutwitch import Floutwitch
#from tilemanager import (TileData, setup_tile_data, position_to_tile_value,
#                        tile_value_to_position, draw_tilemap, setup_surfaces
#                        , initialize_tilemap, update_tile_map, check_collision_in_all_tiles
#                         , SpecialTile, update_special_tiles, Crop)
from tilemanager import *
from inventorymanager import *
from viewport import ViewPort, check_if_out_of_area
from globals import *
import time
# Future Note here:
# I really regret not having the start date of this file
# written down. However, I am 99% sure that it started on
# last Sunday (08/06/2025). Just taking this as a note.

pygame.init()
screen_width = 400
screen_height = 800
screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption("Farmbotany")
clock = pygame.time.Clock()
running = True

viewportx = 0
viewporty = 0
mincornerx = -100
maxcornerx = 0
mincornery = -2100
maxcornery = 0

viewport = ViewPort(viewportx, viewporty)

clicked_slot_data = ItemData("1", 0)
clicked_slot_data_list = [clicked_slot_data]
clicked_slot_list = []
clicked_slot = Slot(clicked_slot_data.id, 1, clicked_slot_data.quantity, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], clicked_slot_list, 64)

tile_world_width = 20
tile_world_length = 20
tile_size = 64
tiles_world = []
special_tiles_world = []
special_tiles_world = Nonefy(tile_world_width * tile_world_length)
tiles_world = setup_tile_data(tile_world_width, tile_world_length)
tiles_world[20].id = "4"
tiles_world[20].sub_id = "2"
tile_slot_list = []

initialize_tilemap(tiles_world, tile_world_width, tile_size, viewport.pos_x, viewport.pos_y, tile_slot_list)

inventory = []
inventory = setup_inventory(12)
slot_list = []
spacement = 60
initialize_inventory(inventory, slot_list, 10, 10, 30, 60, spacement)

inventory[0].id = "2"
inventory[3].id = "2"
inventory[2].id = "3"
inventory[3].quantity = 3
inventory[2].quantity = 2

floutwitch = Floutwitch(0, 0)

setup_surfaces(tile_size)

def check_for_wheat_harvest(special_tiles_world, mouse_pos, tile_world_width, tile_world_length, tile_slot_list, clicked_slot_data, tile_size, inventory, mouse_just_clicked):
    pos = position_to_tile_value(mouse_pos[0], mouse_pos[1], tile_world_width, tile_world_length, tile_size,
                                 viewport.pos_x, viewport.pos_y)

    if mouse_just_clicked and check_collision_in_all_tiles(mouse_pos, tile_slot_list) and clicked_slot_data.id == "3":
        if check_collision_in_all_tiles(mouse_pos, tile_slot_list)[1] == "2" and special_tiles_world[pos] is None:
            clicked_slot_data.quantity -= 1
            special_tiles_world[pos] = Crop(tile_size, 2)

    if check_for_harvest_in_all_crops(special_tiles_world, mouse_pos):
        special_tiles_world[pos] = None
        add_item_to_inventory(inventory, ItemData("4", 1))

class Farmbotany:
    def event_handling(self):
        running = True
        mouse_just_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_just_clicked = True
        return running, mouse_just_clicked



farmbotany = Farmbotany()

def main():
    global running, screen, x, spacement, viewportx, viewporty, tile_slot_list, tile_world_width, tile_world_length
    mouse_just_clicked = False
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         mouse_just_clicked = True

    running, mouse_just_clicked = farmbotany.event_handling()
    keys = pygame.key.get_pressed()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    screen.fill("cadetblue1")

    if floutwitch.rect.x > mincornerx and floutwitch.rect.x < maxcornerx:
        viewportx = floutwitch.rect.x
    if floutwitch.rect.y > mincornery and floutwitch.rect.y < maxcornery:
        viewporty = floutwitch.rect.y

    # Updates viewport position
    viewport.update(viewportx, viewporty)

    mouse_pos = pygame.mouse.get_pos()

    # This part is useful when debugging
    if keys[pygame.K_c]:
        tile = tiles_world[position_to_tile_value(-1 * (floutwitch.rect.x - viewport.pos_x - 350), -1 * (floutwitch.rect.y - viewport.pos_y - 150), tile_world_width, tile_world_length, tile_size, viewport.pos_x, viewport.pos_y)]
        tile.id = "4"
        tile.sub_id = "2"

    check_for_wheat_harvest(special_tiles_world, mouse_pos, tile_world_width, tile_world_length, tile_slot_list, clicked_slot_data, tile_size, inventory, mouse_just_clicked)

    # This is where most things are drawn.
    update_tile_map(tiles_world, tile_slot_list, screen, tile_world_width, tile_size, viewport.pos_x, viewport.pos_y)
    update_special_tiles(special_tiles_world, screen, tile_world_width, tile_size, viewport.pos_x, viewport.pos_y)

    floutwitch.draw(screen, viewport)
    floutwitch.move(keys)

    update_inventory(inventory, screen, slot_list, 30, 10, 10, spacement, 40)

    check_for_clicked_slot_interaction(mouse_just_clicked, slot_list, inventory, clicked_slot_data)

    update_clicked_slot(clicked_slot_data_list, screen, clicked_slot_list, 30, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], -30, 40)

    mouse_just_clicked = False
    pygame.display.update()
    clock.tick(60)


while running:
    main()
