import pygame
import time
import tweener
from floutwitch import Floutwitch
from tilemanager import *
from inventorymanager import *
from viewport import ViewPort, check_if_out_of_area
from globals import *
import solid_object
import rooms
import worlds
import fadeinout
import spritemanager

# Remove the import of shop here
# from shop import *

pygame.init()
pygame.font.init()

class Farmbotany:
    def __init__(self):
        # Import Shop inside the __init__ method to avoid circular import
        from shop import Shop
        
        self.screen_width = 680
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_height, self.screen_width), pygame.SRCALPHA)
        pygame.display.set_caption("Farmbotany")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        
        self.internal_surface = pygame.Surface((1000, 1000), pygame.SRCALPHA)
        self.scailing_surface = pygame.Surface((self.screen_height, self.screen_width), pygame.SRCALPHA)
        self.ui_surface = pygame.Surface(pygame.display.get_window_size(), pygame.SRCALPHA)

        self.draw_queue = []
        self.special_draw_queue = []
        
        self.floutwitch = Floutwitch(0, 0, self.internal_surface, self)

        self.fadeinout = fadeinout.FadeInOut(self.screen, self.screen_width, self.screen_height)
        self.fadeinout_start_time = 0
        self.is_fading_out = False
        self.location_after_change_x = 0
        self.location_after_change_y = 0
        self.room_to_change = None
        
        self.text_font = pygame.font.SysFont("Ariel", 30)

        self.solid_objects_list = []
        #self.brick = solid_object.Brick(100, 100)
        #self.brick.append_self_to_list(self.solid_objects_list)
        self.colliding_with_solid_object = False

        self.farm_to_my_room_passage_rect = pygame.Rect(200, 0, 100, 100)
        self.my_room_to_farm_passage_rect = pygame.Rect(200, 0, 100, 100)

        self.viewportx = 0
        self.viewporty = 0

        self.viewport = ViewPort(self.viewportx, self.viewporty)
        
        self.clicked_slot_data = ItemData("1", 0)
        self.clicked_slot_data_list = [self.clicked_slot_data]
        self.clicked_slot_list = []
        self.clicked_slot = Slot(self.clicked_slot_data.id, 1, self.clicked_slot_data.quantity, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], self.clicked_slot_list, 40)

        self.worlds = worlds.Worlds()

        self.farm = rooms.Room(self.worlds.farm.world, self.worlds.farm.sub_world, self.worlds.farm.special_tiles_world, 1, 0, 900, 0, 900, 20, 20)
        self.my_room = rooms.Room(self.worlds.my_room_world.my_room_world, self.worlds.my_room_world.my_room_sub_world, self.worlds.my_room_world.my_special_room_world, 2, 0, 1000, 0, 1000, 30, 30)

        self.current_room = self.farm        
        self.screen_rect = pygame.Rect(self.viewport.pos_x - 10, self.viewport.pos_y - 10, self.screen_height + 20, self.screen_width + 20)

        # Use this to help me for later in case i forget.

        #self.my_tween = tweener.Tween(0, 1, 1000, tweener.Easing.QUAD, tweener.EasingMode.OUT, True, True, 0)
        #self.my_tween.start()

        self.inventory = []
        self.inventory = setup_inventory(12)
        self.slot_selected = 0
        self.slot_list = []
        self.spacement = 40
        initialize_inventory(self.inventory, self.slot_list, 20, 20, 10, 40, self.spacement)

        self.inventory[0].id = "5"
        self.inventory[0].quantity = 1
        self.inventory[3].id = "2"
        self.inventory[2].id = "3"
        self.inventory[3].quantity = 3
        self.inventory[2].quantity = 2

        self.mouse_just_clicked = False
        self.mouse_realeased = False
        self.right_just_clicked = False
        self.page_up_just_clicked = False
        self.page_up_pressed = False
        self.page_down_just_clicked = False
        self.page_down_pressed = False
        self.mouse_wheel_up = False
        self.mouse_wheel_down = False

        self.mouse_pos = 0
        self.slot_class_selected = 0
        self.is_picking_up = False

        # Now Shop is defined and can be used
        self.shop = Shop(500, 500, self.floutwitch, self)

    # Handles the events and stores them in the variables in the main function.
    def _event_handling(self):
        running = True
        mouse_just_clicked = False
        page_up_pressed = False
        page_down_pressed = False
        mouse_realeased = False
        right_just_clicked = False
        mouse_wheel_up = False
        mouse_wheel_down = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_just_clicked = True
                if event.button == 3:
                    right_just_clicked = True
                if event.button == 4:
                    mouse_wheel_up = True
                if event.button == 5:
                    mouse_wheel_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_realeased = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    page_up_pressed = True
                if event.key == pygame.K_PAGEDOWN:
                    page_down_pressed = True
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
            #if event.type == pygame.VIDEORESIZE:
            #    # Update window size
            #    self.window_width, self.window_height = event.w, event.h
            #    # Resize the display surface
            #    self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

        return running, mouse_just_clicked, page_up_pressed, page_down_pressed, mouse_realeased, right_just_clicked, mouse_wheel_up, mouse_wheel_down

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
        if not self.shop.shop_open:
            world_x = mouse_pos[0] + viewport.pos_x
            world_y = mouse_pos[1] + viewport.pos_y
            # Use fixed tilemap offsets (adjust if tilemap has a non-zero origin)
            offset_x = 0  # e.g., 100 if tilemap starts at x=100
            offset_y = 0  # e.g., 200 if tilemap starts at y=200
            pos = position_to_tile_value(world_x, world_y, tile_world_width, tile_world_length, tile_size, offset_x, offset_y)
            pos_x, pos_y = pos  # Unpack tuple
            # Ensure integer indices
            pos_x = int(pos_x)
            pos_y = int(pos_y)


            pos = pos_y * tile_world_width + pos_x
            
            special_slot_data = inventory[special_slot]
            if mouse_just_clicked and check_collision_in_all_tiles(mouse_pos, tile_slot_list) and special_slot_data.id == "3":
                if self.current_room.world[pos_y][pos_x] == "2" and special_tiles_world[pos_x][pos_y] is None:
                    special_slot_data.quantity -= 1
                    special_tiles_world[pos_x][pos_y] = Crop(tile_size, 20, mouse_pos[0], mouse_pos[1], self)

            if pos_x < tile_world_width and pos_y < tile_world_length:
                if isinstance(special_tiles_world[pos_x][pos_y], Crop):
                    if special_tiles_world[pos_x][pos_y].check_for_harvest():
                        special_tiles_world[pos_x][pos_y] = None
                        add_item_to_inventory(inventory, ItemData("4", 1))
                
    def _render_gold(self, gold, font, surface):
        text = font.render(str(gold), True, (255, 255, 255))
        surface.blit(text, (10, 10))

    def _makes_the_axe_work(self, axe_pos_x, axe_pos_y, farmbotany):
        # Note: i feel quite bad for just copying this things, really wish i would make them myself ):

        if axe_pos_x and axe_pos_y:
            world_x = axe_pos_x + farmbotany.viewport.pos_x
            world_y = axe_pos_y + farmbotany.viewport.pos_y
            tile_x, tile_y = position_to_tile_value(world_x, world_y, farmbotany.current_room.tile_world_width, farmbotany.current_room.tile_world_length, farmbotany.current_room.tile_size, farmbotany.viewport.pos_x, farmbotany.viewport.pos_y)
            tile_x = int(round(tile_x))
            tile_y = int(round(tile_y))
            
            if 0 <= tile_x < farmbotany.current_room.tile_world_width and 0 <= tile_y < farmbotany.current_room.tile_world_length and farmbotany.current_room.sub_world[tile_y][tile_x] == "1":
                tile_index = tile_y * farmbotany.current_room.tile_world_width + tile_x
                if tile_index < len(farmbotany.current_room.tiles_world):
                    farmbotany.current_room.world[tile_y][tile_x] = "2"
                    
    def _switch_room(self, start_time, new_room, is_fading_out, floutwitch, x, y):
        if self.is_fading_out:
            current_time = time.time() - start_time
            
            if current_time > .5:
                self.current_room = new_room
                floutwitch.rect.x = x
                floutwitch.rect.y = y

                if current_time > 1:
                    self.paused = False
                    self.is_fading_out = False

            

    def update(self):
        self.running, self.mouse_just_clicked, self.page_up_just_clicked, self.page_down_just_clicked, self.mouse_realeased, self.right_just_clicked, self.mouse_wheel_up, self.mouse_wheel_down = self._event_handling()
        self.colliding_with_solid_object = self._check_for_solid_object_colision(self.solid_objects_list, self.floutwitch.rect)

        self.keys = pygame.key.get_pressed()
        # Assigns the mouse position
        self.mouse_pos = pygame.mouse.get_pos()
        # Check to see if the mouse is clicked.
        self.mouse_clicked = pygame.mouse.get_pressed()[0]
        
        self.solid_objects_list = []
        self.draw_queue = []
        self.special_draw_queue = []
        self.sprite_list = []

        self.floutwitch.actual_rect_update(self.viewport)
        
        if self.floutwitch.rect.x > self.current_room.mincornerx and self.floutwitch.rect.x < self.current_room.maxcornerx and self.floutwitch.rect.x > pygame.display.get_window_size()[0] / 2:
            self.viewportx = self.floutwitch.rect.x - pygame.display.get_window_size()[0] / 2
        if self.floutwitch.rect.y > self.current_room.mincornery and self.floutwitch.rect.y < self.current_room.maxcornery and self.floutwitch.rect.y > pygame.display.get_window_size()[1] / 2:
            self.viewporty = self.floutwitch.rect.y - pygame.display.get_window_size()[1] / 2
        
        self.floutwitch.actual_rect_update(self.viewport)
        
        append_tilemap_to_sprite_data(self.current_room.tile_slot_list, self.sprite_list, self.current_room.world, self.current_room.sub_world, self.current_room.tile_world_width, self.current_room.tile_size)
        update_special_tiles(self.current_room.special_tiles_world, self.current_room.tile_world_width, 
                            self.current_room.tile_size, 0, 0, self.internal_surface, self.special_draw_queue)
        self.floutwitch.update(self.internal_surface, self.viewport, self.current_room.tiles_world,
                                self.current_room.tile_world_width, self.current_room.tile_world_length, self.mouse_pos,
                                self.current_room.tile_slot_list, self.colliding_with_solid_object, self.solid_objects_list)
        self.floutwitch.move(self.keys, self)
        
        self.slot_class_selected = self.inventory[self.slot_selected]

        if not self.shop.shop_open:

            self.floutwitch.axe_action = self.check_if_axe_needs_to_be_used(self.slot_class_selected, self.slot_list, self.mouse_pos, self.mouse_just_clicked)

            # This part is useful when debugging
            #if self.right_just_clicked:
            #    if self.current_room == self.farm:
            #        self.current_room = self.my_room
            #    elif self.current_room == self.my_room:
            #        self.current_room = self.farm    
                
                #hoe_tile = self.current_room.tiles_world[position_to_tile_value(-1 * (self.floutwitch.rect.x - self.viewport.pos_x - 350), -1 * (self.floutwitch.rect.y - self.viewport.pos_y - 150), self.current_room.tile_world_width, self.current_room.tile_world_length, self.current_room.tile_size, self.viewport.pos_x, self.viewport.pos_y)]
                #hoe_tile.id = "4"
                #hoe_tile.sub_id = "2"

            # This part updates the selected slot in the hotbar.
            if self.mouse_wheel_up:
                if self.slot_selected < len(self.inventory) - 1:
                    self.slot_selected += 1
                else:
                    self.slot_selected = 0

            if self.mouse_wheel_down:
                if self.slot_selected > 0:
                    self.slot_selected -= 1
                else:
                    self.slot_selected = 11
        
        axe_pos_x, axe_pos_y = self.floutwitch.make_axe_interaction(self.internal_surface, self.viewport, self)

        if self.current_room == self.farm:
            # Updates the shop.
            self.shop.update(self.internal_surface, self.screen, self.mouse_realeased)
            
            pygame.draw.rect(self.internal_surface, (255, 255, 255), self.farm_to_my_room_passage_rect, 5)

            if self.floutwitch.rect.colliderect(self.farm_to_my_room_passage_rect) and not self.is_fading_out:
                self.paused = True

                self.fadeinout.fade()
                
                self.fadeinout_start_time = time.time()
                self.is_fading_out = True

                self.location_after_change_x = 200
                self.location_after_change_y = 100
                self.room_to_change = self.my_room

        if self.current_room == self.my_room:
            pygame.draw.rect(self.internal_surface, (255, 255, 255), self.my_room_to_farm_passage_rect, 5)

            if self.floutwitch.rect.colliderect(self.my_room_to_farm_passage_rect) and not self.is_fading_out:
                self.paused = True
                
                self.fadeinout.fade()
                
                self.fadeinout_start_time = time.time()
                self.is_fading_out = True

                
                self.location_after_change_x = 200
                self.location_after_change_y = 100
                self.room_to_change = self.farm
        
        
        # Split sprites into those with y_sort=True and y_sort=False
        y_sort_sprites = [sprite for sprite in self.sprite_list if sprite.y_sort]
        no_sort_sprites = [sprite for sprite in self.sprite_list if not sprite.y_sort]

        # Sort only the y_sort=True sprites by top_left_y
        y_sort_sprites = sorted(y_sort_sprites, key=lambda sprite: sprite.botton_right_y)

        # Combine the sorted and unsorted sprites
        self.sprite_list = no_sort_sprites + y_sort_sprites
        self.internal_surface.fill("cadetblue1")
        self.ui_surface.fill((0, 0, 0, 0))
        self.screen_rect = pygame.Rect(self.viewport.pos_x - 10, self.viewport.pos_y - 10, pygame.display.get_window_size()[0] + 20, pygame.display.get_window_size()[1] + 20)

        for tile in self.current_room.tile_slot_list:
            if tile.is_colliding_with_rect(self.screen_rect):
                self.draw_queue.append(tile)

        for row_idx, row in enumerate(self.current_room.special_tiles_world):
            for column_idx, column in enumerate(row):
                if self.current_room.special_tiles_world[row_idx][column_idx]:
                    if self.current_room.special_tiles_world[row_idx][column_idx].is_colliding_with_rect(self.screen_rect):
                        self.special_draw_queue.append(self.current_room.special_tiles_world[row_idx][column_idx])

        #self.my_tween.update()
        #print(self.my_tween.value)

        pygame.draw.rect(self.internal_surface, (255, 255, 255), self.floutwitch.actual_rect, 5)

        # Updates viewport position
        self.viewport.update(self.viewportx, self.viewporty)



        # Checks and collects the wheat if the mouse clicks on top of one.
        self.check_for_wheat_harvest(self.current_room.special_tiles_world, self.mouse_pos, self.current_room.tile_world_width, self.current_room.tile_world_length, self.current_room.tile_slot_list, self.current_room.tile_size, self.inventory, self.mouse_just_clicked, self.slot_selected, self.viewport)

        # Lights up the selected slot.
        light_slot_by_number(self.slot_selected, self.slot_list)

        # This is where most things are drawn.
        spritemanager.update_sprite_list(self.internal_surface, self.sprite_list, self.viewport.pos_x, self.viewport.pos_y, pygame.display.get_window_size())
        #update_tile_map(self.current_room.world, self.current_room.sub_world, self.current_room.tile_slot_list,
        #                self.current_room.tile_world_width, self.current_room.tile_size,
        #                0, 0, self.internal_surface, self.draw_queue)



        for solid_brick in self.solid_objects_list:
            solid_brick.update(self.internal_surface)

        
        # Can be used later when debugging.
        #pygame.draw.circle(self.internal_surface, (255, 255, 255), (axe_pos_x, axe_pos_y), 50, 5)
        
        self._makes_the_axe_work(axe_pos_x, axe_pos_y, self)
        
                

        self._switch_room(self.fadeinout_start_time, self.room_to_change, self.is_fading_out, self.floutwitch, self.location_after_change_x, self.location_after_change_y)
    
        
        
        

        # Creates a viewport rectangle and then subsurfaces it.
        self.viewport_rect = pygame.Rect(self.viewport.pos_x, self.viewport.pos_y, pygame.display.get_window_size()[0], pygame.display.get_window_size()[1])
        #self.viewport_surface = self.internal_surface.subsurface(self.viewport_rect)
        self.viewport_surface = self.internal_surface

        #self.scailing_surface = pygame.transform.scale(self.viewport_surface, pygame.display.get_window_size())
        self.scailing_surface = self.viewport_surface

        self.screen.blit(self.scailing_surface, (0, 0))

    
        # Calculates the UI and some other things here so they appear in front of the everything else.
        self.shop.update_shop_ui(self.ui_surface)
        update_inventory(self.inventory, self.ui_surface, self.slot_list, 10, 10, 10, self.spacement, 20, 10)
        check_for_clicked_slot_interaction(self.mouse_just_clicked, self.right_just_clicked, self.slot_list, self.inventory, self.clicked_slot_data, self.is_picking_up)
        update_clicked_slot(self.clicked_slot_data_list, self.ui_surface, self.clicked_slot_list, 10, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], -30, 20)
        self._render_gold(self.floutwitch.gold, self.text_font, self.ui_surface)
        #pygame.draw.rect()

        self.scailing_surface = pygame.transform.scale(self.ui_surface, pygame.display.get_window_size())

        self.screen.blit(self.ui_surface, (0, 0))        

        self.fadeinout.update(self.screen)

        #pygame.draw.circle(self.screen, (255, 255, 255), (self.mouse_pos[0] - self.viewport.pos_x, self.mouse_pos[1] - self.viewport.pos_y), 10, 5)

        # Makes the "just clicked" of the variables work.
        self.mouse_just_clicked = False
        self.right_just_clicked = False
        self.page_up_just_clicked = False
        self.page_down_just_clicked = False
        
        pygame.display.update() # Udates the screen.
        self.clock.tick(60) # The clock ticks. This is used for the framerate adjustments.

farmbotany = Farmbotany()

setup_surfaces(farmbotany.current_room.tile_size)
initialize_tilemap(farmbotany.worlds.farm.world, farmbotany.worlds.farm.sub_world, farmbotany.farm.tile_world_width, farmbotany.farm.tile_size, farmbotany.viewport.pos_x, farmbotany.viewport.pos_y, farmbotany.farm.tile_slot_list)
initialize_tilemap(farmbotany.worlds.my_room_world.my_room_world, farmbotany.worlds.my_room_world.my_room_sub_world, farmbotany.my_room.tile_world_width, farmbotany.my_room.tile_size, farmbotany.viewport.pos_x, farmbotany.viewport.pos_y, farmbotany.my_room.tile_slot_list)

while farmbotany.running:
    farmbotany.update() # Runs this every frame

pygame.display.quit() # Exits the display
pygame.quit() # Exits pygame.
# Bye-Bye (: