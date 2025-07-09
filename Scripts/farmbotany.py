import pygame
import time
from floutwitch import Floutwitch
from tilemanager import *
from inventorymanager import *
from viewport import ViewPort, check_if_out_of_area
from globals import *
import solid_object

# Remove the import of shop here
# from shop import *

pygame.init()
pygame.font.init()

class Farmbotany:
    def __init__(self):
        # Import Shop inside the __init__ method to avoid circular import
        from shop import Shop
        
        self.screen_width = 400
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_height, self.screen_width))
        pygame.display.set_caption("Farmbotany")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.internal_surface = pygame.Surface((2000, 2000))
        
        self.floutwitch = Floutwitch(0, 0, self.internal_surface)
        
        self.text_font = pygame.font.SysFont("Ariel", 30)

        self.solid_objects_list = []
        self.brick = solid_object.Brick(100, 100)
        self.brick.append_self_to_list(self.solid_objects_list)
        self.colliding_with_solid_object = False

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
        self.spacement = 40
        initialize_inventory(self.inventory, self.slot_list, 20, 20, 20, 50, self.spacement)

        self.inventory[0].id = "5"
        self.inventory[0].quantity = 1
        self.inventory[3].id = "2"
        self.inventory[2].id = "3"
        self.inventory[3].quantity = 3
        self.inventory[2].quantity = 2

        self.mouse_just_clicked = False
        self.mouse_realeased = False
        self.page_up_just_clicked = False
        self.page_up_pressed = False
        self.page_down_just_clicked = False
        self.page_down_pressed = False
        self.mouse_pos = 0
        self.slot_class_selected = 0

        # Now Shop is defined and can be used
        self.shop = Shop(500, 500, self.floutwitch, self)

    # Handles the events and stores them in the variables in the main function.
    def _event_handling(self):
        running = True
        mouse_just_clicked = False
        page_up_pressed = False
        page_down_pressed = False
        mouse_realeased = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_just_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_realeased = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    page_up_pressed = True
                if event.key == pygame.K_PAGEDOWN:
                    page_down_pressed = True

        return running, mouse_just_clicked, page_up_pressed, page_down_pressed, mouse_realeased

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
    
    def _check_for_solid_object_colision(self, solid_objects_list, rect):
        for solid_object in solid_objects_list:
            if solid_object.rect.colliderect(rect):
                return True
        return False

    def check_for_wheat_harvest(self, special_tiles_world, mouse_pos, tile_world_width, tile_world_length, tile_slot_list, tile_size, inventory, mouse_just_clicked, special_slot, viewport):
        pos = position_to_tile_value(mouse_pos[0], mouse_pos[1], tile_world_width, tile_world_length, tile_size,
                                    self.viewport.pos_x, self.viewport.pos_y)

        pos = round(pos)

        special_slot_data = inventory[special_slot]
        if mouse_just_clicked and check_collision_in_all_tiles(mouse_pos, tile_slot_list) and special_slot_data.id == "3":
            if tile_slot_list[pos].id == "2" and special_tiles_world[pos] is None:
                special_slot_data.quantity -= 1
                special_tiles_world[pos] = Crop(tile_size, 2)

#        if check_for_harvest_in_all_crops(special_tiles_world, (mouse_pos[0] - viewport.pos_x, mouse_pos[1] - viewport.pos_y)):
#            print(check_for_harvest_in_all_crops(special_tiles_world, (mouse_pos[0] - viewport.pos_x, mouse_pos[1] - viewport.pos_y)))


        #if special_tiles_world[pos].check_for_harvest()
        if check_for_harvest_in_all_crops(special_tiles_world, (mouse_pos[0] - viewport.pos_x, mouse_pos[1] - viewport.pos_y)):
            special_tiles_world[pos] = None
            add_item_to_inventory(inventory, ItemData("4", 1))
            
    def _render_gold(self, gold, font, surface):
        text = font.render(str(gold), True, (255, 255, 255))
        surface.blit(text, (0, 0))

    def _makes_the_axe_work(self, axe_pos_x, axe_pos_y, farmbotany):
        if axe_pos_x and axe_pos_y:
            tile = position_to_tile_value(axe_pos_x,
                                            axe_pos_y, farmbotany.tile_world_width,
                                            farmbotany.tile_world_length, farmbotany.tile_size, 0, 0)

            tile = round(tile) # Rounds the tile down to prevent some issues.

            if tile is not None and 0 <= tile < len(farmbotany.tiles_world): # Checks if the tile is not None,
                                                                    # is greater or equel to 0 and is 
                                                                    # smaller that the size of the world
                farmbotany.tiles_world[tile].id = "2"
        

    def update(self):
        self.running, self.mouse_just_clicked, self.page_up_just_clicked, self.page_down_just_clicked, self.mouse_realeased = self._event_handling()
        self.colliding_with_solid_object = self._check_for_solid_object_colision(self.solid_objects_list, self.floutwitch.rect)

        self.keys = pygame.key.get_pressed()
        self.mouse_clicked = pygame.mouse.get_pressed()[0]

        self.internal_surface.fill("cadetblue1")

        if self.floutwitch.rect.x > self.mincornerx and self.floutwitch.rect.x < self.maxcornerx and self.floutwitch.rect.x > self.screen_height / 2:
            self.viewportx = -1 * self.floutwitch.rect.x + self.screen_height / 2
        if self.floutwitch.rect.y > self.mincornery and self.floutwitch.rect.y < self.maxcornery and self.floutwitch.rect.y > self.screen_width / 2:
            self.viewporty = -1 * self.floutwitch.rect.y + self.screen_width / 2

        # Updates viewport position
        self.viewport.update(self.viewportx, self.viewporty)

        # Assigns the mouse position
        self.mouse_pos = pygame.mouse.get_pos()

        self.slot_class_selected = self.inventory[self.slot_selected]

        if not self.shop.shop_open:

            self.floutwitch.axe_action = self.check_if_axe_needs_to_be_used(self.slot_class_selected, self.slot_list, self.mouse_pos, self.mouse_just_clicked)

            # This part is useful when debugging
            if self.keys[pygame.K_c]:
                hoe_tile = self.tiles_world[position_to_tile_value(-1 * (self.floutwitch.rect.x - self.viewport.pos_x - 350), -1 * (self.floutwitch.rect.y - self.viewport.pos_y - 150), self.tile_world_width, self.tile_world_length, self.tile_size, self.viewport.pos_x, self.viewport.pos_y)]
                hoe_tile.id = "4"
                hoe_tile.sub_id = "2"

            # This part updates the selected slot in the hotbar.
            if self.page_up_just_clicked:
                if self.slot_selected < len(self.inventory) - 1:
                    self.slot_selected += 1
                else:
                    self.slot_selected = 0

            if self.page_down_just_clicked:
                if self.slot_selected > 0:
                    self.slot_selected -= 1
                else:
                    self.slot_selected = 11

        # Checks and collects the wheat if the mouse clicks on top of one.
        self.check_for_wheat_harvest(self.special_tiles_world, self.mouse_pos, self.tile_world_width, self.tile_world_length, self.tile_slot_list, self.tile_size, self.inventory, self.mouse_just_clicked, self.slot_selected, self.viewport)

        # Lights up the selected slot.
        light_slot_by_number(self.slot_selected, self.slot_list)

        # This is where most things are drawn.
        update_tile_map(self.tiles_world, self.tile_slot_list,
                        self.tile_world_width, self.tile_size,
                        0, 0, self.internal_surface)
        update_special_tiles(self.special_tiles_world, self.tile_world_width, 
                            self.tile_size, 0, 0, self.internal_surface)

        self.floutwitch.update(self.internal_surface, self.viewport, self.tiles_world,
                                self.tile_world_width, self.tile_world_length, self.mouse_pos,
                                self.tile_slot_list, self.colliding_with_solid_object, self.solid_objects_list)
        self.floutwitch.move(self.keys)
        
        axe_pos_x, axe_pos_y = self.floutwitch.make_axe_interaction(self.internal_surface, self.viewport)

        for solid_brick in self.solid_objects_list:
            solid_brick.update(self.internal_surface)

        # Can be used later when debugging.
        #pygame.draw.circle(self.internal_surface, (255, 255, 255), (axe_pos_x, axe_pos_y), 50, 5)

        self._makes_the_axe_work(axe_pos_x, axe_pos_y, self)
        
        # Updates the shop.
        self.shop.update(self.internal_surface, self.screen, self.mouse_realeased)
        
        #self.internal_surface = pygame.transform.scale(self.internal_surface, (1000, 1000))

        # Blits the internal surface with the offset of the viewports. Works a lot better than appling them directly.
        self.screen.blit(self.internal_surface, (self.viewport.pos_x, self.viewport.pos_y))

        # Calculates the UI and some other things here so they appear in front of the everything else.
        self.shop.update_shop_ui(self.screen)
        update_inventory(self.inventory, self.screen, self.slot_list, 10, 10, 10, self.spacement, 30, 10)
        check_for_clicked_slot_interaction(self.mouse_just_clicked, self.slot_list, self.inventory, self.clicked_slot_data)
        update_clicked_slot(self.clicked_slot_data_list, self.screen, self.clicked_slot_list, 30, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], -30, 40)
        self._render_gold(self.floutwitch.gold, self.text_font, self.screen)
        #pygame.draw.circle(self.screen, (255, 255, 255), (self.mouse_pos[0] - self.viewport.pos_x, self.mouse_pos[1] - self.viewport.pos_y), 10, 5)

        # Makes the "just clicked" of the variables work.
        self.mouse_just_clicked = False
        self.page_up_just_clicked = False
        self.page_down_just_clicked = False
        
        pygame.display.update() # Udates the screen.
        self.clock.tick(60) # The clock ticks. This is used for the framerate adjustments.




farmbotany = Farmbotany()

setup_surfaces(farmbotany.tile_size)
initialize_tilemap(farmbotany.tiles_world, farmbotany.tile_world_width, farmbotany.tile_size, farmbotany.viewport.pos_x, farmbotany.viewport.pos_y, farmbotany.tile_slot_list)

while farmbotany.running:
    farmbotany.update() # Runs this every frame

pygame.display.quit() # Exits the display
pygame.quit() # Exits pygame.
# Bye-Bye (: