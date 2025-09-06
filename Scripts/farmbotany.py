import pygame
import time
import tweener
from floutwitch import Floutwitch
from tilemanager import *
from inventorymanager import *
from viewport import ViewPort, check_if_out_of_area
from utils import *
import solid_object
import rooms
import worlds
import fadeinout
import spritemanager

# This isets the window's initial position.
os.environ["SDL_VIDEO_WINDOW_POS"] = "400, 30"

pygame.init()
pygame.font.init()


class Farmbotany:
    def __init__(self):
        from shop import Shop

        self.screen_width = 680
        self.screen_height = 720
        # Create a minimal, invisible window for loading
        self.screen = pygame.display.set_mode((1, 1), pygame.NOFRAME)
        pygame.display.set_caption("Farmbotany")
        
        # Load and set icon
        try:
            icon = pygame.image.load("icon.png")
            pygame.display.set_icon(icon)
        except pygame.error as e:
            print(f"Error loading icon: {e}")
        
        try:
            pygame.display.set_icon(icon)
        except pygame.error as e:
            print(f"Error setting icon: {e}")

        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False


        self.internal_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.ui_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)

        self.draw_queue = []
        self.special_draw_queue = []
        
        self.floutwitch = Floutwitch(500, 500, self.internal_surface, self)
        self.text_font = pygame.font.Font("Fonts/HelvetiPixel.ttf", 30)

        self.solid_objects_list = []
        self.colliding_with_solid_object = False

        self.viewportx = 0
        self.viewporty = 0
        self.viewport = ViewPort(self.viewportx, self.viewporty)
        
        self.clicked_slot_data = ItemData("1", 0)
        self.clicked_slot_data_list = [self.clicked_slot_data]
        self.clicked_slot_list = []
        self.clicked_slot = Slot(self.clicked_slot_data.id, 1, self.clicked_slot_data.quantity, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], self.clicked_slot_list, 40)

        self.frames = 0

        self.worlds = worlds.Worlds()
        self.farm = rooms.Room(self.worlds.farm.world, self.worlds.farm.sub_world, self.worlds.farm.special_tiles_world, 1, 0, self.worlds.farm.tile_world_width * 64, 0, self.worlds.farm.tile_world_heigt * 64, 20, 20)
        self.my_room = rooms.Room(self.worlds.my_room_world.my_room_world, self.worlds.my_room_world.my_room_sub_world, self.worlds.my_room_world.my_special_room_world, 2, 0, self.worlds.my_room_world.tile_world_width * 64, 0, self.worlds.my_room_world.tile_world_heigt * 64, 30, 30)

        self.current_room = self.farm
        self.room_list = [self.farm, self.my_room]
        setup_surfaces(self.current_room.tile_size)

        self.screen_rect = pygame.Rect(self.viewport.pos_x - 10, self.viewport.pos_y - 10, self.screen_width + 20, self.screen_width + 20)
        self.update_tilemap_terrain = True

        self.farm_to_my_room_passage_rect = pygame.Rect(200, 0, 100, 100)
        self.my_room_to_farm_passage_rect = pygame.Rect(200, self.my_room.tile_world_length * self.my_room.tile_size - 100, 100, 100)
        
        self.inventory = []
        self.inventory = setup_inventory(12)
        self.slot_selected = 0
        self.slot_list = []
        self.spacement = 40
        initialize_inventory(self.inventory, self.slot_list, 20, 20, 10, 40, self.spacement)
        
        self.inventory[0].id = "5"
        self.inventory[0].quantity = 1
        self.inventory[1].id = "6"
        self.inventory[1].quantity = 1
        self.inventory[2].id = "7"
        self.inventory[2].quantity = 1
        self.inventory[4].id = "2"
        self.inventory[3].id = "3"
        self.inventory[4].quantity = 3
        self.inventory[3].quantity = 15

        self.start_collecting_tick = False
        self.is_collecting = False
        self.collecting_time = .25
        self.collecting_animation_time = 0

        self.mouse_just_clicked = False
        self.mouse_realeased = False
        self.right_just_clicked = False
        self.page_up_just_clicked = False
        self.page_up_pressed = False
        self.page_down_just_clicked = False
        self.page_down_pressed = False
        self.mouse_wheel_up = False
        self.mouse_wheel_down = False
        self.space_just_pressed = False
        self.space_just_pressed = False
        self.e_just_pressed = False
        self.window_changed_size = False
        self.right_released = False

        self.mouse_pos = 0
        self.slot_class_selected = 0
        self.is_picking_up = False

        self.shop = Shop(960, 1020, self.floutwitch, self)

        # Switch to full window after loading
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.SRCALPHA, pygame.RESIZABLE, vsync=1)

        self.fadeinout = fadeinout.FadeInOut(self.screen, self.screen_width, self.screen_height)
        pygame.display.set_caption("Farmbotany")
        self.fadeinout_start_time = 0
        self.is_fading_out = False
        self.location_after_change_x = 0
        self.location_after_change_y = 0
        self.room_to_change = None
        
        self.music = pygame.mixer.music.load("Sounds/Music/Wallpaper.mp3")    
        pygame.mixer.music.play(-1)
        
        self.scailing_surface = self.internal_surface
        self.scaled_ui_surface = self.ui_surface

    # Handles the events and stores them in the variables in the main function.
    def _event_handling(self):
        self.running = True
        self.mouse_just_clicked = False
        self.page_up_pressed = False
        self.page_down_pressed = False
        self.mouse_realeased = False
        self.right_just_clicked = False
        self.mouse_wheel_up = False
        self.mouse_wheel_down = False
        self.e_just_pressed = False
        self.right_released = False

        space_just_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_just_clicked = True
                if event.button == 3:
                    self.right_just_clicked = True
                if event.button == 4:
                    self.mouse_wheel_up = True
                if event.button == 5:
                    self.mouse_wheel_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_realeased = True
                if event.button == 3:
                    self.right_released = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    self.page_up_pressed = True
                if event.key == pygame.K_PAGEDOWN:
                    self.page_down_pressed = True
                if event.key == pygame.K_SPACE:
                    self.space_just_pressed = True
                if event.key == pygame.K_SPACE:
                    self.space_just_pressed = True
                if event.key == pygame.K_e:
                    self.e_just_pressed = True
            if event.type == pygame.VIDEORESIZE:
                # Update window size
                self.window_width, self.window_height = event.w, event.h
                # Resize the display surface
                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        
    # Checks specifically for special slots (no longer being used. Ignore this.)
    def check_for_special_slot_interaction(self):
        my_special_slot = 0
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                my_special_slot += event.y

        return my_special_slot


    def check_if_hoe_needs_to_be_used(self, clicked_slot_data, slot_list, point, mouse_just_clicked):
        if check_point_collision_with_all_slots(slot_list, point) is None and clicked_slot_data.id == "5":
            if mouse_just_clicked or pygame.key.get_pressed()[pygame.K_c]:
                return True
        return False
    
    
    def check_if_pickaxe_needs_to_be_used(self, clicked_slot_data, slot_list, point, mouse_just_clicked):
        if check_point_collision_with_all_slots(slot_list, point) is None and clicked_slot_data.id == "6":
            if mouse_just_clicked or pygame.key.get_pressed()[pygame.K_c]:
                return True
        return False
    
    def check_if_watercan_needs_to_be_used(self, clicked_slot_data, slot_list, point, mouse_just_clicked):
        if check_point_collision_with_all_slots(slot_list, point) is None and clicked_slot_data.id == "7":
            if mouse_just_clicked or pygame.key.get_pressed()[pygame.K_c]:
                return True
        return False
    
    def _check_for_solid_object_colision(self, solid_objects_list, rect):
        for solid_object in solid_objects_list:
            if solid_object.colliderect(rect):
                return True
        return False

    def check_for_wheat_harvest(self, special_tiles_world, mouse_pos, tile_world_width, tile_world_length, tile_slot_list, tile_size, inventory, mouse_just_clicked, special_slot, viewport, right_mouse_just_clicked, adjesent_tile):
        if not self.shop.shop_open:
            world_x = mouse_pos[0] + viewport.pos_x
            world_y = mouse_pos[1] + viewport.pos_y
            # Use fixed tilemap offsets (adjust if tilemap has a non-zero origin)
            offset_x = 0  # e.g., 100 if tilemap starts at x=100
            offset_y = 0  # e.g., 200 if tilemap starts at y=200
            #pos = position_to_tile_value(world_x, world_y, tile_world_width, tile_world_length, tile_size, offset_x, offset_y)
            #pos_x, pos_y = pos  # Unpack tuple
            # Ensure integer indices
            #pos_x = int(pos_x)
            #pos_y = int(pos_y)
            pos_x = adjesent_tile[0]
            pos_y = adjesent_tile[1]
            mouse_pos = position_to_tile_value(world_x, world_y, tile_world_width, tile_world_length, tile_size, offset_x, offset_y)
            mouse_pos_x, mouse_pos_y = mouse_pos  # Unpack tuple
            # Ensure integer indices
            mouse_pos_x = int(mouse_pos_x)
            mouse_pos_y = int(mouse_pos_y)

            pos = pos_y * tile_world_width + pos_x
            
            grow_time = 10

            special_slot_data = inventory[special_slot]
            if not self.is_collecting:
                if self.keys[pygame.K_c]:
                    if special_slot_data.id == "3":
                        if tiles[self.current_room.world[pos_y][pos_x]][0]["plantable"]:
                            if special_tiles_world[pos_x][pos_y] is None:
                                special_slot_data.quantity -= 1
                                special_tiles_world[pos_x][pos_y] = Crop(tile_size, grow_time, mouse_pos[0], mouse_pos[1], self, "Sprites/wheat_growing.png", "Sprites/wheat.png", ItemData("4", 1), self.current_room.world)
                                self.start_collecting_tick = True
                else:
                    if pygame.mouse.get_pressed()[0]:
                        if special_slot_data.id == "3":
                            if tiles[self.current_room.world[mouse_pos_y][mouse_pos_x]][0]["plantable"] and self.floutwitch_to_mouse_distance[0] <= 1 and self.floutwitch_to_mouse_distance[0] >= -1 and self.floutwitch_to_mouse_distance[1] <= 1 and self.floutwitch_to_mouse_distance[1] >= -1 and self.floutwitch.can_move:
                                if special_tiles_world[mouse_pos_x][mouse_pos_y] is None:
                                    special_slot_data.quantity -= 1
                                    special_tiles_world[mouse_pos_x][mouse_pos_y] = Crop(tile_size, grow_time, mouse_pos[0], mouse_pos[1], self, "Sprites/wheat_growing.png", "Sprites/wheat.png", ItemData("4", 1), self.current_room.world)
                                    self.start_collecting_tick = True
            
            done = False

            if pos_x < tile_world_width and pos_y < tile_world_length:
                if self.keys[pygame.K_c]:
                    if (self.floutwitch.can_move or (self.floutwitch.animation == "collecting" and time.time() - self.floutwitch.anim_time > 0.50)):
                        if isinstance(special_tiles_world[pos_x][pos_y], Crop):
                            if special_tiles_world[pos_x][pos_y].check_for_harvest(self.keys[pygame.K_c]):
                                special_tiles_world[pos_x][pos_y].collect(special_tiles_world, inventory, pos_x, pos_y)
                                self.floutwitch.start_collecting_animation()
                                done = True
            if not done:
                if mouse_pos_x < tile_world_width and mouse_pos_y < tile_world_length:
                    if pygame.mouse.get_pressed()[2]:
                        if (self.floutwitch.can_move or (self.floutwitch.animation == "collecting" and time.time() - self.floutwitch.anim_time > 0.50)):
                            if isinstance(special_tiles_world[mouse_pos_x][mouse_pos_y], Crop):
                                if special_tiles_world[mouse_pos_x][mouse_pos_y].check_for_harvest(pygame.mouse.get_pressed()[2]) and self.floutwitch_to_mouse_distance[0] <= 1 and self.floutwitch_to_mouse_distance[0] >= -1 and self.floutwitch_to_mouse_distance[1] <= 1 and self.floutwitch_to_mouse_distance[1] >= -1:
                                    special_tiles_world[mouse_pos_x][mouse_pos_y].collect(special_tiles_world, inventory, mouse_pos_x, mouse_pos_y)
                                    self.floutwitch.start_collecting_animation()
        
    def _render_gold(self, gold, font, surface):
        text = font.render(str(gold), True, (255, 255, 255))
        surface.blit(text, (10, 10))

    def _makes_the_hoe_work(self, hoe_pos_x, hoe_pos_y, farmbotany, hoe_anim_frames, hoe_animation_speed):
        # Note: i feel quite bad for just copying this things, really wish i would make them myself ):

        if hoe_anim_frames == hoe_animation_speed * 6:
            if hoe_pos_x and hoe_pos_y:
                world_x = hoe_pos_x + farmbotany.viewport.pos_x
                world_y = hoe_pos_y + farmbotany.viewport.pos_y
                tile_x, tile_y = position_to_tile_value(world_x, world_y, farmbotany.current_room.tile_world_width, farmbotany.current_room.tile_world_length, farmbotany.current_room.tile_size, farmbotany.viewport.pos_x, farmbotany.viewport.pos_y)
                tile_x = int(round(tile_x))
                tile_y = int(round(tile_y))
                
                if tiles[farmbotany.current_room.sub_world[tile_y][tile_x]][0]["hoable"] == True:
                    if 0 <= tile_x < farmbotany.current_room.tile_world_width and 0 <= tile_y < farmbotany.current_room.tile_world_length:
                        tile_index = tile_y * farmbotany.current_room.tile_world_width + tile_x
                        if tile_index < len(farmbotany.current_room.tiles_world):
                            farmbotany.current_room.world[tile_y][tile_x] = "2"
                            self.update_tilemap_terrain = True
    
    def _makes_the_pickaxe_work(self, pickaxe_pos_x, pickaxe_pos_y, farmbotany, pickaxe_anim_frames, pickaxe_animation_speed):
        # Note: i feel quite bad for just copying this things, really wish i would make them myself ):

        if pickaxe_anim_frames == pickaxe_animation_speed * 6:
            if pickaxe_pos_x and pickaxe_pos_y:
                world_x = pickaxe_pos_x + farmbotany.viewport.pos_x
                world_y = pickaxe_pos_y + farmbotany.viewport.pos_y
                tile_x, tile_y = position_to_tile_value(world_x, world_y, farmbotany.current_room.tile_world_width, farmbotany.current_room.tile_world_length, farmbotany.current_room.tile_size, farmbotany.viewport.pos_x, farmbotany.viewport.pos_y)
                tile_x = int(round(tile_x))
                tile_y = int(round(tile_y))

                #if isinstance(farmbotany.current_room.special_tiles_world[tile_x][tile_y], Crop):
                #    farmbotany.current_room.special_tiles_world[tile_x][tile_y].erase(farmbotany.current_room.special_tiles_world, tile_x, tile_y)
                #else:
                #    if tiles[farmbotany.current_room.world[tile_y][tile_x]][0]["child"] == "75":
                farmbotany.current_room.world[tile_y][tile_x] = "3"
                self.update_tilemap_terrain = True

    def _makes_the_watercan_work(self, watercan_pos_x, watercan_pos_y, farmbotany, watercan_anim_frames, watercan_animation_speed):
        # Note: i feel quite bad for just copying this things, really wish i would make them myself ):

        if watercan_anim_frames == watercan_animation_speed * 6:
            if watercan_pos_x and watercan_pos_y:
                world_x = watercan_pos_x + farmbotany.viewport.pos_x
                world_y = watercan_pos_y + farmbotany.viewport.pos_y
                tile_x, tile_y = position_to_tile_value(world_x, world_y, farmbotany.current_room.tile_world_width, farmbotany.current_room.tile_world_length, farmbotany.current_room.tile_size, farmbotany.viewport.pos_x, farmbotany.viewport.pos_y)
                tile_x = int(round(tile_x))
                tile_y = int(round(tile_y))
                if tiles[farmbotany.current_room.world[tile_y][tile_x]][0]["child"] == "2":
                    farmbotany.current_room.world[tile_y][tile_x] = "75"
                    farmbotany.current_room.world_water_status[tile_y][tile_x] = farmbotany.frames
                    self.update_tilemap_terrain = True

    def _switch_room(self, start_time, new_room, is_fading_out, floutwitch, x, y):
        if self.is_fading_out:
            current_time = time.time() - start_time
            self.fadeinout.fade()        
            
            if current_time > .5:
                self.current_room = new_room
                floutwitch.rect.x = x
                floutwitch.rect.y = y

                if current_time > 1:
                    self.paused = False
                    self.is_fading_out = False
                    update_special_tiles_value(self.current_room.special_tiles_world, self.current_room.tile_size, self.frames, self.viewport.pos_x, self.viewport.pos_y, pygame.display.get_window_size()[0], pygame.display.get_window_size()[1], 10)
    
    def _update_selected_hotbar_slot(self, if_not):
        if not if_not:
            if self.mouse_wheel_down or self.page_down_just_clicked:
                if self.slot_selected < len(self.inventory) - 1:
                    self.slot_selected += 1
                else:
                    self.slot_selected = 0

            if self.mouse_wheel_up or self.page_up_just_clicked:
                if self.slot_selected > 0:
                    self.slot_selected -= 1
                else:
                    self.slot_selected = 11

    def update(self):
        self._event_handling()
        self.colliding_with_solid_object = self._check_for_solid_object_colision(self.solid_objects_list, self.floutwitch.rect)

        self.frames += 1

        self.keys = pygame.key.get_pressed()
        # Assigns the mouse position
        self.mouse_pos = pygame.mouse.get_pos()
        # Check to see if the mouse is clicked.
        self.mouse_clicked = pygame.mouse.get_pressed()[0]

        self.solid_objects_list = []
        self.draw_queue = []
        self.special_draw_queue = []
        self.sprite_list = []
        self.true_no_y_sort_sprite_list = []

        if self.start_collecting_tick:
            self.start_collecting_tick = False
            self.is_collecting = True
            self.collecting_animation_time = time.time()
        
        if time.time() - self.collecting_animation_time >= self.collecting_time:
            self.is_collecting = False
            self.collecting_animation_time = 0

        #surface_to_window_ratio = (self.screen_width / pygame.display.get_window_size()[0], self.screen_height / pygame.display.get_window_size()[1])
        surface_to_window_ratio = (1, 1)
        self.acurate_position = (self.mouse_pos[0] * surface_to_window_ratio[0], self.mouse_pos[1] * surface_to_window_ratio[1])

        using_tool = self.floutwitch.hoe.in_animation or self.floutwitch.pickaxe.in_animation or self.floutwitch.in_animation
        

        append_all_rect_to_solid_object_list(self.current_room.sub_world, self.current_room.tile_size, self.solid_objects_list)

        self.floutwitch.actual_rect_update(self.viewport)
        self.floutwitch.update_adjecent_pos()
        adjesent_tile = [int(self.floutwitch.adjesent_pos_x // self.current_room.tile_size), int(self.floutwitch.adjesent_pos_y // self.current_room.tile_size)]

        hoe_pos_x, hoe_pos_y = (self.floutwitch.adjesent_pos_x, self.floutwitch.adjesent_pos_y)
        self.floutwitch.make_hoe_interaction(self.internal_surface, self.viewport, self, hoe_pos_x, hoe_pos_y)
        self._makes_the_hoe_work(hoe_pos_x, hoe_pos_y, self, self.floutwitch.hoe.anim_frames, self.floutwitch.hoe.animation_speed)
        
        pickaxe_pos_x, pickaxe_pos_y = (self.floutwitch.adjesent_pos_x, self.floutwitch.adjesent_pos_y)
        self.floutwitch.make_pickaxe_interaction(self.internal_surface, self.viewport, self)
        self._makes_the_pickaxe_work(pickaxe_pos_x, pickaxe_pos_y, self, self.floutwitch.pickaxe.anim_frames, self.floutwitch.pickaxe.animation_speed)
        
        watercan_pos_x, watercan_pos_y = (self.floutwitch.adjesent_pos_x, self.floutwitch.adjesent_pos_y)
        self.floutwitch.make_watercan_interaction(self.internal_surface, self.viewport, self, watercan_pos_x, watercan_pos_y)
        self._makes_the_watercan_work(watercan_pos_x, watercan_pos_y, self, self.floutwitch.watercan.anim_frames, self.floutwitch.watercan.animation_speed)
        

        # Updates the mouse distance from the floutwitch.
        self.floutwitch_to_mouse_distance = distance_in_tiles(self.floutwitch.actual_center_pos[0], self.floutwitch.actual_center_pos[1], self.acurate_position[0], self.acurate_position[1], 0, 0, self.current_room.tile_size)
        
        # Checks and collects the wheat if the mouse clicks on top of one.
        self.check_for_wheat_harvest(self.current_room.special_tiles_world, self.acurate_position, self.current_room.tile_world_width, self.current_room.tile_world_length, self.current_room.tile_slot_list, self.current_room.tile_size, self.inventory, self.mouse_just_clicked, self.slot_selected, self.viewport, self.right_just_clicked, adjesent_tile)

        if update_watered_ground_status(self.room_list, self.frames, 20000, self.update_tilemap_terrain):
            self.update_tilemap_terrain = True
        if self.update_tilemap_terrain:
            update_tilemap_terrain(self.current_room.world)

        viewport_window_size = (pygame.display.get_window_size()[0], pygame.display.get_window_size()[1])
        window_size = (pygame.display.get_window_size()[0], pygame.display.get_window_size()[1])
        viewport_adjusted_window_size = (self.floutwitch.rect.x + viewport_window_size[0] / 2, self.floutwitch.rect.y + viewport_window_size[1] / 2)

        if self.floutwitch.rect.x > self.current_room.mincornerx and viewport_adjusted_window_size[0] < self.current_room.maxcornerx and self.floutwitch.rect.x > viewport_window_size[0] / 2:
            self.viewportx = self.floutwitch.rect.x - viewport_window_size[0] / 2
        elif viewport_adjusted_window_size[0] < self.current_room.maxcornerx:
            self.viewportx = 0
        elif viewport_adjusted_window_size[0] >= self.current_room.maxcornerx:
            self.viewportx = self.current_room.maxcornerx - viewport_window_size[0]
        if self.floutwitch.rect.y > self.current_room.mincornery and viewport_adjusted_window_size[1] < self.current_room.maxcornery and self.floutwitch.rect.y > viewport_window_size[1] / 2:
            self.viewporty = self.floutwitch.rect.y - viewport_window_size[1] / 2
        elif viewport_adjusted_window_size[1] < self.current_room.maxcornery:
            self.viewporty = 0
        elif viewport_adjusted_window_size[1] >= self.current_room.maxcornery:
            self.viewporty = self.current_room.maxcornery - viewport_window_size[1]
        
        append_tilemap_to_sprite_data(self.current_room.tile_slot_list, self.sprite_list, self.current_room.world, self.current_room.sub_world, self.current_room.tile_world_width, self.current_room.tile_size, self.sprite_list, pygame.display.get_window_size(), self.viewport.pos_x, self.viewport.pos_y)
        update_special_tiles(self.current_room.special_tiles_world, self.current_room.tile_world_width, 
                            self.current_room.tile_size, self.viewport.pos_x, self.viewport.pos_y, self.internal_surface, self.special_draw_queue,
                            pygame.display.get_window_size()[0], pygame.display.get_window_size()[1])
        update_special_tiles_value(self.room_list, self.current_room.tile_size, self.frames, self.viewport.pos_x, self.viewport.pos_y, pygame.display.get_window_size()[0], pygame.display.get_window_size()[1], 50)
        if self.current_room == self.farm:
            # Updates the shop.
            self.shop.update(self.internal_surface, self.screen, self.mouse_realeased, self.acurate_position, self.right_released, self.mouse_just_clicked)

        self.floutwitch.update(self.internal_surface, self.viewport, self.current_room.tiles_world,
                                self.current_room.tile_world_width, self.current_room.tile_world_length, self.mouse_pos,
                                self.current_room.tile_slot_list, self.colliding_with_solid_object, self.solid_objects_list)
        self.floutwitch.move(self.keys, self)
        self.floutwitch.updates_the_hoe(self.internal_surface, self.viewport)
        self.floutwitch.updates_the_pickaxe(self.internal_surface, self.viewport)
        self.floutwitch.updates_the_watercan(self.internal_surface, self.viewport)

        self.slot_class_selected = self.inventory[self.slot_selected]

        if not self.shop.shop_open:

            self.floutwitch.hoe_action = self.floutwitch.hoe.in_animation
            self.floutwitch.hoe_tick = self.check_if_hoe_needs_to_be_used(self.slot_class_selected, self.slot_list, self.mouse_pos, self.mouse_just_clicked)
            self.floutwitch.pickaxe_action = self.floutwitch.pickaxe.in_animation
            self.floutwitch.pickaxe_tick = self.check_if_pickaxe_needs_to_be_used(self.slot_class_selected, self.slot_list, self.mouse_pos, self.mouse_just_clicked)
            self.floutwitch.watercan_action = self.floutwitch.watercan.in_animation
            self.floutwitch.watercan_tick = self.check_if_watercan_needs_to_be_used(self.slot_class_selected, self.slot_list, self.mouse_pos, self.mouse_just_clicked)
            


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
            self._update_selected_hotbar_slot(using_tool)

        if self.current_room == self.farm:
            
            if self.floutwitch.rect.colliderect(self.farm_to_my_room_passage_rect) and not self.is_fading_out:
                self.paused = True

                self.fadeinout_start_time = time.time()
                self.is_fading_out = True

                self.location_after_change_x = 225
                self.location_after_change_y = self.my_room.tile_world_length * self.current_room.tile_size - 200
                self.room_to_change = self.my_room

        if self.current_room == self.my_room:
            if self.floutwitch.rect.colliderect(self.my_room_to_farm_passage_rect) and not self.is_fading_out:
                self.paused = True
                
                self.fadeinout_start_time = time.time()
                self.is_fading_out = True

                
                self.location_after_change_x = 225
                self.location_after_change_y = 100
                self.room_to_change = self.farm
        
        
        # Split sprites into those with y_sort=True and y_sort=False
        y_sort_sprites = [sprite for sprite in self.sprite_list if sprite.y_sort]
        no_sort_sprites = [sprite for sprite in self.sprite_list if not sprite.y_sort] + self.true_no_y_sort_sprite_list

        # Sort only the y_sort=True sprites by top_left_y
        y_sort_sprites = sorted(y_sort_sprites, key=lambda sprite: sprite.y_sort_y)

        # Combine the sorted and unsorted sprites
        self.sprite_list = no_sort_sprites + y_sort_sprites
        
        self.internal_surface.fill("cadetblue1")
        self.ui_surface.fill((0, 0, 0, 0))
        self.screen_rect = pygame.Rect(self.viewport.pos_x - 10, self.viewport.pos_y - 10, pygame.display.get_window_size()[0] + 20, pygame.display.get_window_size()[1] + 20)

        # Updates viewport position
        self.viewport.update(self.viewportx, self.viewporty)

        # Lights up the selected slot.
        light_slot_by_number(self.slot_selected, self.slot_list)

        # This is where most things are drawn.
        spritemanager.update_sprite_list(self.internal_surface, self.sprite_list, self.viewport.pos_x, self.viewport.pos_y, (pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]))

        # Nicolas is a beautiful smart intelligent human being (Homo sapiens sapiens)    
        #pygame.draw.rect(self.internal_surface, (255, 255, 255), pygame.Rect(self.current_room.mincornerx - self.viewport.pos_x, self.current_room.mincornery - self.viewport.pos_y, self.current_room.maxcornerx, self.current_room.maxcornery), 5)

        self._switch_room(self.fadeinout_start_time, self.room_to_change, self.is_fading_out, self.floutwitch, self.location_after_change_x, self.location_after_change_y)
        
        self.screen.blit(self.internal_surface, (0, 0))
    
        # Calculates the UI and some other things here so they appear in front of the everything else.
        self.shop.update_shop_ui(self.ui_surface, self.acurate_position)
        update_inventory(self.inventory, self.ui_surface, self.slot_list, 10, 10, 10, self.spacement, 20, 10)
        check_for_clicked_slot_interaction(self.mouse_just_clicked, self.right_just_clicked, self.slot_list, self.inventory, self.clicked_slot_data, self.is_picking_up, self.acurate_position)
        update_clicked_slot(self.clicked_slot_data_list, self.ui_surface, self.clicked_slot_list, 10, self.mouse_pos[0] * surface_to_window_ratio[0], self.mouse_pos[1] * surface_to_window_ratio[1], -30, 20)
        self._render_gold(self.floutwitch.gold, self.text_font, self.ui_surface)


        #if self.window_changed_size:
        #    self.scaled_ui_surface = pygame.transform.scale(self.ui_surface, pygame.display.get_window_size())
        #else:
        self.scaled_ui_surface = self.ui_surface


        self.screen.blit(self.scaled_ui_surface, (0, 0))

        self.fadeinout.update(self.screen)

        # Makes the "just clicked" of the variables work.
        self.mouse_just_clicked = False
        self.right_just_clicked = False
        self.page_up_just_clicked = False
        self.page_down_just_clicked = False

        self.update_tilemap_terrain = False

        pygame.display.update() # Udates the screen.
        self.clock.tick(60) # The clock ticks. This is used for the framerate adjustments.

farmbotany = Farmbotany()

while farmbotany.running:
    farmbotany.update() # Runs this every frame
#    import cProfile
#    import pstats
#
#    cProfile.runctx('farmbotany.update()', globals(), locals(), 'profile_stats')
#    p = pstats.Stats('profile_stats')
#    p.sort_stats('cumulative').print_stats(10)  # Print top 10 time-consuming functions

pygame.display.quit() # Exits the display
pygame.quit() # Exits pygame.
# Bye-Bye (:
