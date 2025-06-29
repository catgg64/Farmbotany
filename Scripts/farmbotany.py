import pygame
from floutwitch import Floutwitch
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
mincornerx = 0
maxcornerx = 1000
mincornery = 0
maxcornery = 2100

viewport = ViewPort(viewportx, viewporty)
internal_surface = pygame.Surface((screen_height, screen_width))

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
tile_slot_list = []

initialize_tilemap(tiles_world, tile_world_width, tile_size, viewport.pos_x, viewport.pos_y, tile_slot_list)

inventory = []
inventory = setup_inventory(12)
slot_selected = 0
slot_list = []
spacement = 60
initialize_inventory(inventory, slot_list, 10, 10, 30, 60, spacement)

inventory[0].id = "5"
inventory[0].quantity = 1
inventory[3].id = "2"
inventory[2].id = "3"
inventory[3].quantity = 3
inventory[2].quantity = 2

floutwitch = Floutwitch(0, 0, internal_surface)

setup_surfaces(tile_size)

def check_for_wheat_harvest(special_tiles_world, mouse_pos, tile_world_width, tile_world_length, tile_slot_list, tile_size, inventory, mouse_just_clicked, special_slot):
    pos = position_to_tile_value(mouse_pos[0], mouse_pos[1], tile_world_width, tile_world_length, tile_size,
                                 viewport.pos_x, viewport.pos_y)

    special_slot_data = inventory[special_slot]
    if mouse_just_clicked and check_collision_in_all_tiles(mouse_pos, tile_slot_list) and special_slot_data.id == "3":
        if check_collision_in_all_tiles(mouse_pos, tile_slot_list)[0] == "2" and special_tiles_world[pos] is None:
            special_slot_data.quantity -= 1
            special_tiles_world[pos] = Crop(tile_size, 2)

    if check_for_harvest_in_all_crops(special_tiles_world, mouse_pos):
        special_tiles_world[pos] = None
        add_item_to_inventory(inventory, ItemData("4", 1))

class Farmbotany:

    # Handles the events and stores them in the variables in the main function.
    def event_handling(self):
        running = True
        mouse_just_clicked = False
        page_up_pressed = False
        page_down_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_just_clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    page_up_pressed = True
                if event.key == pygame.K_PAGEDOWN:
                    page_down_pressed = True

        return running, mouse_just_clicked, page_up_pressed, page_down_pressed

    # Checks specifically for special slots (no longer being used. Ignore this.)
    def check_for_special_slot_interaction(self):
        my_special_slot = 0
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                my_special_slot += event.y

        return my_special_slot


    def check_if_axe_needs_to_be_used(self, clicked_slot_data, slot_list, point, mouse_just_clicked):
        if check_point_collision_with_all_slots(slot_list, point) is None and clicked_slot_data.id == "5" and mouse_just_clicked:
            return True
        return False


farmbotany = Farmbotany()
random_image = pygame.image.load("Sprites/tile_set.png")

def main():
    global running, screen, x, spacement, viewportx, viewporty, tile_slot_list, tile_world_width, tile_world_length, slot_selected, inventory
    mouse_just_clicked = False

    running, mouse_just_clicked, page_up_just_clicked, page_down_just_clicked = farmbotany.event_handling()

    keys = pygame.key.get_pressed()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    internal_surface.fill("cadetblue1")

    #print(floutwitch.rect.x, viewportx)
    #print(floutwitch.rect.x > mincornerx, floutwitch.rect.x < maxcornerx, floutwitch.rect.x > screen_width / 2)

    if floutwitch.rect.x > mincornerx and floutwitch.rect.x < maxcornerx and floutwitch.rect.x > screen_height / 2:
        viewportx = -1 * floutwitch.rect.x + screen_height / 2
        print("ÇLKJÇLKJÇ")
    if floutwitch.rect.y > mincornery and floutwitch.rect.y < maxcornery and floutwitch.rect.y > screen_width / 2:
        viewporty = -1 * floutwitch.rect.y + screen_width / 2

    # Updates viewport position
    viewport.update(viewportx, viewporty)

    # Assigns the mouse position
    mouse_pos = pygame.mouse.get_pos()

    slot_class_selected = inventory[slot_selected]

    floutwitch.axe_action = farmbotany.check_if_axe_needs_to_be_used(slot_class_selected, slot_list, mouse_pos, mouse_just_clicked)

    # This part is useful when debugging
    if keys[pygame.K_c]:
        hoe_tile = tiles_world[position_to_tile_value(-1 * (floutwitch.rect.x - viewport.pos_x - 350), -1 * (floutwitch.rect.y - viewport.pos_y - 150), tile_world_width, tile_world_length, tile_size, viewport.pos_x, viewport.pos_y)]
        hoe_tile.id = "4"
        hoe_tile.sub_id = "2"

    # This part updates the selected slot in the hotbar.
    if page_up_just_clicked:
        if slot_selected < len(inventory) - 1:
            slot_selected += 1
        else:
            slot_selected = 0

    if page_down_just_clicked:
        if slot_selected > 0:
            slot_selected -= 1
        else:
            slot_selected = 11

    # Checks and collects the wheat if the mouse clicks on top of one.
    check_for_wheat_harvest(special_tiles_world, mouse_pos, tile_world_width, tile_world_length, tile_slot_list, tile_size, inventory, mouse_just_clicked, slot_selected)

    # Lights up the selected slot.
    light_slot_by_number(slot_selected, slot_list)

    # This is where most things are drawn.
    update_tile_map(tiles_world, tile_slot_list, tile_world_width, tile_size, 0, 0, internal_surface)
    update_special_tiles(special_tiles_world, tile_world_width, tile_size, 0, 0, internal_surface)

    floutwitch.update(internal_surface, viewport, tiles_world, tile_world_width, tile_world_length, mouse_pos, tile_slot_list)
    floutwitch.move(keys)
    axe_pos_x, axe_pos_y = floutwitch.make_axe_interaction(internal_surface, viewport)

    #print(position_to_tile_value(axe_pos_x,
    #                                   axe_pos_y, tile_world_width,
    #                                   tile_world_length, tile_size, viewport.pos_x, viewport.pos_y))

    # Can be used later when debugging.
    pygame.draw.circle(internal_surface, (255, 255, 255), (axe_pos_x, axe_pos_y), 50, 5)

    if axe_pos_x and axe_pos_y:
        tile = position_to_tile_value(axe_pos_x,
                                           axe_pos_y, tile_world_width,
                                           tile_world_length, tile_size, viewport.pos_x, viewport.pos_y)

        if tile:
            tiles_world[tile].id = "2"

    update_inventory(inventory, internal_surface, slot_list, 30, 10, 10, spacement, 40)
    check_for_clicked_slot_interaction(mouse_just_clicked, slot_list, inventory, clicked_slot_data)
    update_clicked_slot(clicked_slot_data_list, internal_surface, clicked_slot_list, 30, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], -30, 40)

    # Makes the "just clicked" of the variables work.
    mouse_just_clicked = False
    page_up_just_clicked = False
    page_down_just_clicked = False

    screen.blit(internal_surface, (viewport.pos_x, viewport.pos_y))
    pygame.display.update()
    clock.tick(60)


while running:
    main()
