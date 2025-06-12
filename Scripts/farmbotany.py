import pygame
from floutwitch import Floutwitch
from tilemanager import TileData, setup_tile_data, position_to_tile_value, tile_value_to_position, draw_tilemap, setup_surfaces
from inventorymanager import (setup_item_surfaces, setup_inventory, draw_inventory, ItemData, setup_item_surfaces,
                              position_to_slot_value, Slot, initialize_inventory, update_inventory, check_point_collision_with_all_slots)

pygame.init()
screen_width = 400
screen_height = 800
screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption("Farmbotany")
clock = pygame.time.Clock()
running = True

tiles_world = []
tiles_world = setup_tile_data(10, 10)
tiles_world[0].id = "3"
tiles_world[0].sub_id = "2"
tile_size = 64

inventory = []
inventory = setup_inventory(12)
slot_list = []
spacement = 50
initialize_inventory(inventory, slot_list, 10, 10, 30, 60, spacement)

inventory[0].id = "2"
inventory[3].id = "2"
inventory[2].id = "2"
inventory[3].quantity = 3
inventory[2].quantity = 2
print(inventory[0].id)

floutwitch = Floutwitch(50, 50)

setup_surfaces(tile_size)

def main():
    global running, screen, x, spacement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    screen.fill("cadetblue1")

    draw_tilemap(tiles_world, 10, screen, tile_size)
    floutwitch.draw(screen)
    floutwitch.move(keys)
    #draw_inventory(inventory, screen, 45, 10, 10)
    update_inventory(inventory, screen, slot_list, 30, 10, 10, spacement, 40)
    print(check_point_collision_with_all_slots(slot_list, pygame.mouse.get_pos()))



    pygame.display.update()
    clock.tick(60)



while running:
    main()


