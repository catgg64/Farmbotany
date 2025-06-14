import pygame
from floutwitch import Floutwitch
from tilemanager import TileData, setup_tile_data, position_to_tile_value, tile_value_to_position, draw_tilemap, setup_surfaces
from inventorymanager import (setup_item_surfaces, setup_inventory, draw_inventory, ItemData, setup_item_surfaces,
                              position_to_slot_value, Slot, initialize_inventory, update_inventory,
                              check_point_collision_with_all_slots, update_clicked_slot, check_for_clicked_slot_interaction)
from viewport import ViewPort, check_if_out_of_area
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
maxcornerx = 800
mincornery = -2100
maxcornery = 2800

viewport = ViewPort(viewportx, viewporty)

clicked_slot_data = ItemData("1", 0)
clicked_slot_data_list = [clicked_slot_data]
clicked_slot_list = []
clicked_slot = Slot(clicked_slot_data.id, 1, clicked_slot_data.quantity, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], clicked_slot_list, 64)
#initialize_inventory(clicked_slot_data_list, clicked_slot_list, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 64, 64, 0)

tiles_world = []
tiles_world = setup_tile_data(10, 10)
tiles_world[0].id = "3"
tiles_world[0].sub_id = "2"
tile_size = 64

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

def main():
    global running, screen, x, spacement, viewportx, viewporty
    mouse_just_clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_just_clicked = True

    keys = pygame.key.get_pressed()

    screen.fill("cadetblue1")

    if floutwitch.rect.x > mincornerx and floutwitch.rect.x < maxcornerx:
        viewportx = floutwitch.rect.x
    if floutwitch.rect.y > mincornery and floutwitch.rect.y < maxcornery:
        viewporty = floutwitch.rect.y

    viewport.update(viewportx, viewporty)

    draw_tilemap(tiles_world, 10, screen, tile_size, viewport.pos_x, viewport.pos_y)

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
