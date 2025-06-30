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


class Farmbotany:
    # Initializes the Farmbotany Class.
    def __init__(self):
        self.screen_width = 400
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_height, self.screen_width))
        pygame.display.set_caption("Farmbotany")
        self.clock = pygame.time.Clock()
        self.running = True
        self.internal_surface = pygame.Surface((1000, 1000))
        self.floutwitch = Floutwitch(0, 0, self.internal_surface)

        self.viewportx = 0
        self.viewporty = 0
        self.mincornerx = 0
        self.maxcornerx = 1000
        self.mincornery = 0
        self.maxcornery = 2100

        self.viewport = ViewPort(self.viewportx, self.viewporty)
        
        self.clicked_slot_data = ItemData("1", 0)
        self.clicked_slot_data_list = [self.clicked_slot_data]
        self.clicked_slot_list = []
        self.clicked_slot = Slot(self.clicked_slot_data.id, 1, self.clicked_slot_data.quantity, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], self.clicked_slot_list, 64)

        self.tile_world_width = 20
        self.tile_world_length = 20
        self.tile_size = 64
        self.tiles_world = []
        self.special_tiles_world = []
        self.special_tiles_world = Nonefy(self.tile_world_width * self.tile_world_length)
        self.tiles_world = setup_tile_data(self.tile_world_width, self.tile_world_length)
        self.tile_slot_list = []

        self.inventory = []
        self.inventory = setup_inventory(12)
        self.slot_selected = 0
        self.slot_list = []
        self.spacement = 60
        initialize_inventory(self.inventory, self.slot_list, 10, 10, 30, 60, self.spacement)

        self.inventory[0].id = "5"
        self.inventory[0].quantity = 1
        self.inventory[3].id = "2"
        self.inventory[2].id = "3"
        self.inventory[3].quantity = 3
        self.inventory[2].quantity = 2

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
    
    def check_for_wheat_harvest(self, special_tiles_world, mouse_pos, tile_world_width, tile_world_length, tile_slot_list, tile_size, inventory, mouse_just_clicked, special_slot):
        pos = position_to_tile_value(mouse_pos[0], mouse_pos[1], tile_world_width, tile_world_length, tile_size,
                                    farmbotany.viewport.pos_x, farmbotany.viewport.pos_y)

        special_slot_data = inventory[special_slot]
        if mouse_just_clicked and check_collision_in_all_tiles(mouse_pos, tile_slot_list) and special_slot_data.id == "3":
            if check_collision_in_all_tiles(mouse_pos, tile_slot_list)[0] == "2" and special_tiles_world[pos] is None:
                special_slot_data.quantity -= 1
                special_tiles_world[pos] = Crop(tile_size, 2)

        if check_for_harvest_in_all_crops(special_tiles_world, mouse_pos):
            special_tiles_world[pos] = None
            add_item_to_inventory(inventory, ItemData("4", 1))




farmbotany = Farmbotany()
random_image = pygame.image.load("Sprites/tile_set.png")

setup_surfaces(farmbotany.tile_size)
initialize_tilemap(farmbotany.tiles_world, farmbotany.tile_world_width, farmbotany.tile_size, farmbotany.viewport.pos_x, farmbotany.viewport.pos_y, farmbotany.tile_slot_list)

def main():
    global running, screen, x, spacement, viewportx, viewporty, tile_slot_list, tile_world_width, tile_world_length, slot_selected, inventory
    mouse_just_clicked = False

    farmbotany.running, mouse_just_clicked, page_up_just_clicked, page_down_just_clicked = farmbotany.event_handling()

    keys = pygame.key.get_pressed()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    farmbotany.internal_surface.fill("cadetblue1")

    if farmbotany.floutwitch.rect.x > farmbotany.mincornerx and farmbotany.floutwitch.rect.x < farmbotany.maxcornerx and farmbotany.floutwitch.rect.x > farmbotany.screen_height / 2:
        farmbotany.viewportx = -1 * farmbotany.floutwitch.rect.x + farmbotany.screen_height / 2
    if farmbotany.floutwitch.rect.y > farmbotany.mincornery and farmbotany.floutwitch.rect.y < farmbotany.maxcornery and farmbotany.floutwitch.rect.y > farmbotany.screen_width / 2:
        farmbotany.viewporty = -1 * farmbotany.floutwitch.rect.y + farmbotany.screen_width / 2

    # Updates viewport position
    farmbotany.viewport.update(farmbotany.viewportx, farmbotany.viewporty)

    # Assigns the mouse position
    mouse_pos = pygame.mouse.get_pos()

    slot_class_selected = farmbotany.inventory[farmbotany.slot_selected]

    farmbotany.floutwitch.axe_action = farmbotany.check_if_axe_needs_to_be_used(slot_class_selected, farmbotany.slot_list, mouse_pos, mouse_just_clicked)

    # This part is useful when debugging
    if keys[pygame.K_c]:
        hoe_tile = farmbotany.tiles_world[position_to_tile_value(-1 * (farmbotany.floutwitch.rect.x - farmbotany.viewport.pos_x - 350), -1 * (farmbotany.floutwitch.rect.y - farmbotany.viewport.pos_y - 150), farmbotany.tile_world_width, farmbotany.tile_world_length, farmbotany.tile_size, farmbotany.viewport.pos_x, farmbotany.viewport.pos_y)]
        hoe_tile.id = "4"
        hoe_tile.sub_id = "2"

    # This part updates the selected slot in the hotbar.
    if page_up_just_clicked:
        if farmbotany.slot_selected < len(farmbotany.inventory) - 1:
            farmbotany.slot_selected += 1
        else:
            farmbotany.slot_selected = 0

    if page_down_just_clicked:
        if farmbotany.slot_selected > 0:
            farmbotany.slot_selected -= 1
        else:
            farmbotany.slot_selected = 11

    # Checks and collects the wheat if the mouse clicks on top of one.
    farmbotany.check_for_wheat_harvest(farmbotany.special_tiles_world, mouse_pos, farmbotany.tile_world_width, farmbotany.tile_world_length, farmbotany.tile_slot_list, farmbotany.tile_size, farmbotany.inventory, mouse_just_clicked, farmbotany.slot_selected)

    # Lights up the selected slot.
    light_slot_by_number(farmbotany.slot_selected, farmbotany.slot_list)

    # This is where most things are drawn.
    update_tile_map(farmbotany.tiles_world, farmbotany.tile_slot_list, farmbotany.tile_world_width, farmbotany.tile_size, 0, 0, farmbotany.internal_surface)
    update_special_tiles(farmbotany.special_tiles_world, farmbotany.tile_world_width, farmbotany.tile_size, 0, 0, farmbotany.internal_surface)

    farmbotany.floutwitch.update(farmbotany.internal_surface, farmbotany.viewport, farmbotany.tiles_world, farmbotany.tile_world_width, farmbotany.tile_world_length, mouse_pos, farmbotany.tile_slot_list)
    farmbotany.floutwitch.move(keys)
    axe_pos_x, axe_pos_y = farmbotany.floutwitch.make_axe_interaction(farmbotany.internal_surface, farmbotany.viewport)

    #print(position_to_tile_value(axe_pos_x,
    #                                   axe_pos_y, farmbotany.tile_world_width,
    #                                   farmbotany.tile_world_length, farmbotany.tile_size, farmbotany.viewport.pos_x, farmbotany.viewport.pos_y))

    # Can be used later when debugging.
    pygame.draw.circle(farmbotany.internal_surface, (255, 255, 255), (axe_pos_x, axe_pos_y), 50, 5)

    if axe_pos_x and axe_pos_y:
        tile = position_to_tile_value(axe_pos_x,
                                           axe_pos_y, farmbotany.tile_world_width,
                                           farmbotany.tile_world_length, farmbotany.tile_size, 0, 0)

        tile = round(tile)

        if tile is not None and 0 <= tile < len(farmbotany.tiles_world):
            farmbotany.tiles_world[tile].id = "2"
        
    
    # Makes the "just clicked" of the variables work.
    mouse_just_clicked = False
    page_up_just_clicked = False
    page_down_just_clicked = False

    farmbotany.screen.blit(farmbotany.internal_surface, (farmbotany.viewport.pos_x, farmbotany.viewport.pos_y))
    
    # Calculates the UI and some other things here so they appear in front of the everything else.
    update_inventory(farmbotany.inventory, farmbotany.screen, farmbotany.slot_list, 30, 10, 10, farmbotany.spacement, 40)
    check_for_clicked_slot_interaction(mouse_just_clicked, farmbotany.slot_list, farmbotany.inventory, farmbotany.clicked_slot_data)
    update_clicked_slot(farmbotany.clicked_slot_data_list, farmbotany.screen, farmbotany.clicked_slot_list, 30, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], -30, 40)

    pygame.display.update()
    farmbotany.clock.tick(60)

while farmbotany.running:
    main()
