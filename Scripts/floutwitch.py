import pygame

from tilemanager import *
from hoe import *
import spritemanager
import pickaxe

class Floutwitch():
    def __init__(self, pos_x, pos_y, internal_surface, farmbotany):
        self.image_right = pygame.image.load("Sprites/tile_set.png").convert_alpha()
        self.substract_rect = pygame.Rect(2080, 2912, 32, 32)
        self.image_right = self.image_right.subsurface(self.substract_rect)
        self.image_right = pygame.transform.scale(self.image_right, (100, 100))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.rect = pygame.Rect(pos_x, pos_y, 50, 25)
        self.image_rect = self.image_right.get_rect(topleft=(pos_x, pos_y))
        self.image_down = pygame.image.load("Sprites/tile_set.png").convert_alpha()
        self.substract_rect_down = pygame.Rect(2016, 2912, 32, 32)
        self.image_down = self.image_down.subsurface(self.substract_rect_down)
        self.image_down = pygame.transform.scale(self.image_down, (100, 100))
        self.image_up = pygame.image.load("Sprites/tile_set.png").convert_alpha()
        self.substract_rect_up = pygame.Rect(2048, 2912, 32, 32)
        self.image_up = self.image_up.subsurface(self.substract_rect_up)
        self.image_up = pygame.transform.scale(self.image_up, (100, 100))
        self.hoe = Hoe(self.rect.x, self.rect.y)
        self.pickaxe = pickaxe.PickAxe(self.rect.x, self.rect.y)
        self.can_move = True
        self.front_pos_x = 0
        self.front_pos_y = 0
        self.is_key_v_pressed = False
        self.hoe_action = False
        self.direction = [False, False, False, False]
        self.direction_faced = [False, False, False, False]
        self.in_close_animation = False
        self.facing_direction = False
        self.hoe_tick = False
        self.internal_surface = internal_surface
        self.gold = 0
        self.farmbotany = farmbotany
        self.pickaxe_tick = False
        self.pickaxe_action = False
        
        self.speed = 5
        self.is_walking = False
        self.needs_reverse = False

    def update(self, internal_surface, viewport, current_tile_map, current_tile_map_width, current_tile_map_lengh, mouse_pos, slot_tile_map, colliding_with_solid_object, solid_objects_list):
        self.tile_map = current_tile_map
        self.tile_map_width = current_tile_map_width
        self.tile_map_lengh = current_tile_map_lengh
        self.mouse_pos = mouse_pos
        self.viewport = viewport
        self.slot_tile_map = slot_tile_map
        self.colliding_with_solid_object = colliding_with_solid_object
        self.solid_objects_list = solid_objects_list
        self.image_rect = self.image_right.get_rect(topleft=(self.rect.x - 25, self.rect.y - 50))
        
        self.actual_floutwitch_position = (self.rect.x - viewport.pos_x, self.rect.y - viewport.pos_y)
        self.actual_center_pos = [self.actual_rect.x + (50 / 2), self.actual_rect.y + (20 / 2)]
        
        if self.direction[1] and self.direction[2] and self.direction[3]:
            self.direction_faced[1] = True
            self.direction_faced[2] = False
            self.direction_faced[3] = False
            
        
        if self.direction[0] and self.direction[2] and self.direction[3]:
            self.direction_faced[0] = True
            self.direction_faced[2] = False
            self.direction_faced[3] = False
            
        if self.direction_faced[2]:
            self.image = self.image_right
            #self.internal_surface.blit(self.image_right, ((self.rect.x) + -25, (self.rect.y) + -50))
        elif self.direction_faced[3]:
            self.image = self.image_left
            #self.internal_surface.blit(self.image_left, ((self.rect.x) + -25, (self.rect.y) + -50))
        elif self.direction_faced[0]:
            self.image = self.image_up
            #self.internal_surface.blit(self.image_up, ((self.rect.x) + -25, (self.rect.y) + -50))
        elif self.direction_faced[1]:
            self.image = self.image_down
            #self.internal_surface.blit(self.image_down, ((self.rect.x) + -25, (self.rect.y) + -50))
        else:
            self.image = self.image_down
            #self.internal_surface.blit(self.image_down, ((self.rect.x) + -25, (self.rect.y) + -50))
        
        self.farmbotany.sprite_list.append(spritemanager.SpriteData(self.image, self.rect.x + -25, self.rect.y + -50, self.rect.x + 25, self.rect.y + 50, True))
        
        self.actual_rect = pygame.Rect(self.rect.x - self.farmbotany.viewport.pos_x, self.rect.y - self.farmbotany.viewport.pos_y, 50, 25)
        
    def make_hoe_interaction(self, internal_surface, viewport, farmbotany):

        result_x = 0
        result_y = 0
        
        if not farmbotany.paused:

            # if self.hoe_action:

            #     is_done = False

            #     distance_from_cursor_x, distance_from_cursor_y = (self.mouse_pos[0] - self.rect.x - self.viewport.pos_x,
            #                                                                          self.mouse_pos[1] - self.rect.y - self.viewport.pos_y)

            #     if distance_from_cursor_x < 108 and distance_from_cursor_x > -32 and distance_from_cursor_y < 153 and distance_from_cursor_y > -32:
            #         pos = position_to_tile_value(self.mouse_pos[0], self.mouse_pos[1], self.tile_map_width,
            #                                      self.tile_map_lengh, 64, viewport.pos_x, viewport.pos_y)
            #         grid_pos = tile_value_to_position(pos, self.tile_map_width, 64)
            #         actual_pos = (grid_pos[0] - self.actual_floutwitch_position[0], grid_pos[1] - self.actual_floutwitch_position[1])
            #         print(actual_pos)
            #         pos = round(pos)
            #         self.tile_map[pos].id = "2"
            #         is_done = True
            #         print(actual_pos)

            #         self.facing_direction = [False, False, False, False]

            #         if actual_pos[0] < 0:
            #             self.facing_direction[2] = True
            #         elif actual_pos[0] > 60:
            #             self.facing_direction[3] = True
            #         elif actual_pos[1] < 0:
            #             self.facing_direction[0] = True
            #         elif actual_pos[1] > 0:
            #             self.facing_direction[1] = True
                        
            #         if actual_pos[0] > 60 and not self.hoe.in_animation and not self.hoe.just_exited_animation:
            #             self.front_pos_x = (self.rect.x) + 80
            #             self.front_pos_y = (self.rect.y) + 0
            #             self.hoe.start_animation(self.front_pos_x, self.front_pos_y, self)
            #             self.in_close_animation = True


            #         elif actual_pos[0] < 0 and not self.hoe.in_animation and not self.hoe.just_exited_animation:
            #             self.front_pos_x = (self.rect.x) + (280 - 350)
            #             self.front_pos_y = (self.rect.y) + 0
            #             self.hoe.start_animation(self.front_pos_x, self.front_pos_y, self)
            #             self.in_close_animation = True


            #         elif actual_pos[1] > 0 and not self.hoe.in_animation and not self.hoe.just_exited_animation:
            #             self.front_pos_x = (self.rect.x) + 10
            #             self.front_pos_y = (self.rect.y) + (90 - 350)
            #             self.hoe.start_animation(self.front_pos_x, self.front_pos_y, self)
            #             self.in_close_animation = True


            #         elif actual_pos[1] < 0 and not self.hoe.in_animation and not self.hoe.just_exited_animation:
            #             self.front_pos_x = (self.rect.x) + 10
            #             self.front_pos_y = (self.rect.y) + (240 - 350)
            #             self.hoe.start_animation(self.front_pos_x, self.front_pos_y, self)
            #             self.in_close_animation = True

            #         self.hoe.make_animation(internal_surface, self, self.facing_direction)

            if self.hoe_tick and not self.hoe.in_animation:
                if self.direction_faced[3]:
                    self.front_pos_x = self.image_rect.x + 80
                    self.front_pos_y = self.image_rect.y + 0
                    self.hoe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.image_rect.x + 150)
                    result_y = (self.image_rect.y + 70)
                    

                elif self.direction_faced[2]:
                    self.front_pos_x = self.image_rect.x + (280 - 350)
                    self.front_pos_y = self.image_rect.y + 0
                    self.hoe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.image_rect.x + -70)
                    result_y = (self.image_rect.y + 70)
                    

                elif self.direction_faced[1]:
                    self.front_pos_x = self.image_rect.x + 20
                    self.front_pos_y = self.image_rect.y + (240 - 150)
                    self.hoe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.image_rect.x + 50)
                    result_y = (self.image_rect.y + 130)
                    

                elif self.direction_faced[0]:
                    self.front_pos_x = self.image_rect.x + 10
                    self.front_pos_y = self.image_rect.y + (90 - 150)
                    self.hoe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.image_rect.x + 50)
                    result_y = (self.image_rect.y + -10)
                    

                self.hoe.make_animation(internal_surface, self, self.direction_faced)

            if self.hoe_action:
                if self.direction_faced[3]:
                    result_x = (self.image_rect.x + 150)
                    result_y = (self.image_rect.y + 70)
                

                elif self.direction_faced[2]:
                    result_x = (self.image_rect.x + -70)
                    result_y = (self.image_rect.y + 70)
                    

                elif self.direction_faced[1]:
                    result_x = (self.image_rect.x + 50)
                    result_y = (self.image_rect.y + 130)
                    

                elif self.direction_faced[0]:
                    result_x = (self.image_rect.x + 50)
                    result_y = (self.image_rect.y + -10)
                






        elif not self.hoe.in_animation:
            result_x = 0
            result_y = 0


        self.hoe.just_exited_animation = False
        return result_x, result_y

    def updates_the_hoe(self, internal_surface, viewport):
        self.hoe.update()
        if self.hoe.in_animation:
            self.hoe.make_animation(internal_surface, self, self.direction_faced)

        if self.in_close_animation:
            self.hoe.make_animation(internal_surface, self, self.facing_direction_faced)

        if not self.hoe.in_animation:
            self.in_close_animation = False
    
    def make_pickaxe_interaction(self, internal_surface, viewport, farmbotany):

        result_x = 0
        result_y = 0
        
        if not farmbotany.paused:

            # if self.pickaxe_action:

            #     is_done = False

            #     distance_from_cursor_x, distance_from_cursor_y = (self.mouse_pos[0] - self.rect.x - self.viewport.pos_x,
            #                                                                          self.mouse_pos[1] - self.rect.y - self.viewport.pos_y)

            #     if distance_from_cursor_x < 108 and distance_from_cursor_x > -32 and distance_from_cursor_y < 153 and distance_from_cursor_y > -32:
            #         pos = position_to_tile_value(self.mouse_pos[0], self.mouse_pos[1], self.tile_map_width,
            #                                      self.tile_map_lengh, 64, viewport.pos_x, viewport.pos_y)
            #         grid_pos = tile_value_to_position(pos, self.tile_map_width, 64)
            #         actual_pos = (grid_pos[0] - self.actual_floutwitch_position[0], grid_pos[1] - self.actual_floutwitch_position[1])
            #         print(actual_pos)
            #         pos = round(pos)
            #         self.tile_map[pos].id = "2"
            #         is_done = True
            #         print(actual_pos)

            #         self.facing_direction = [False, False, False, False]

            #         if actual_pos[0] < 0:
            #             self.facing_direction[2] = True
            #         elif actual_pos[0] > 60:
            #             self.facing_direction[3] = True
            #         elif actual_pos[1] < 0:
            #             self.facing_direction[0] = True
            #         elif actual_pos[1] > 0:
            #             self.facing_direction[1] = True
                        
            #         if actual_pos[0] > 60 and not self.pickaxe.in_animation and not self.pickaxe.just_exited_animation:
            #             self.front_pos_x = (self.rect.x) + 80
            #             self.front_pos_y = (self.rect.y) + 0
            #             self.pickaxe.start_animation(self.front_pos_x, self.front_pos_y, self)
            #             self.in_close_animation = True


            #         elif actual_pos[0] < 0 and not self.pickaxe.in_animation and not self.pickaxe.just_exited_animation:
            #             self.front_pos_x = (self.rect.x) + (280 - 350)
            #             self.front_pos_y = (self.rect.y) + 0
            #             self.pickaxe.start_animation(self.front_pos_x, self.front_pos_y, self)
            #             self.in_close_animation = True


            #         elif actual_pos[1] > 0 and not self.pickaxe.in_animation and not self.pickaxe.just_exited_animation:
            #             self.front_pos_x = (self.rect.x) + 10
            #             self.front_pos_y = (self.rect.y) + (90 - 350)
            #             self.pickaxe.start_animation(self.front_pos_x, self.front_pos_y, self)
            #             self.in_close_animation = True


            #         elif actual_pos[1] < 0 and not self.pickaxe.in_animation and not self.pickaxe.just_exited_animation:
            #             self.front_pos_x = (self.rect.x) + 10
            #             self.front_pos_y = (self.rect.y) + (240 - 350)
            #             self.pickaxe.start_animation(self.front_pos_x, self.front_pos_y, self)
            #             self.in_close_animation = True

            #         self.pickaxe.make_animation(internal_surface, self, self.facing_direction)

            if self.pickaxe_tick:
                if self.direction_faced[3]:
                    self.front_pos_x = self.image_rect.x + 80
                    self.front_pos_y = self.image_rect.y + 0
                    self.pickaxe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.image_rect.x + 150)
                    result_y = (self.image_rect.y + 70)
                    

                elif self.direction_faced[2]:
                    self.front_pos_x = self.image_rect.x + (280 - 350)
                    self.front_pos_y = self.image_rect.y + 0
                    self.pickaxe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.image_rect.x + -70)
                    result_y = (self.image_rect.y + 70)
                    

                elif self.direction_faced[1]:
                    self.front_pos_x = self.image_rect.x + 20
                    self.front_pos_y = self.image_rect.y + (240 - 150)
                    self.pickaxe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.image_rect.x + 50)
                    result_y = (self.image_rect.y + 130)
                    

                elif self.direction_faced[0]:
                    self.front_pos_x = self.image_rect.x + 10
                    self.front_pos_y = self.image_rect.y + (90 - 150)
                    self.pickaxe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.image_rect.x + 50)
                    result_y = (self.image_rect.y + -10)
                    

                self.pickaxe.make_animation(internal_surface, self, self.direction_faced)

            if self.pickaxe_action:
                if self.direction_faced[3]:
                    result_x = (self.image_rect.x + 150)
                    result_y = (self.image_rect.y + 70)
                

                elif self.direction_faced[2]:
                    result_x = (self.image_rect.x + -70)
                    result_y = (self.image_rect.y + 70)
                    

                elif self.direction_faced[1]:
                    result_x = (self.image_rect.x + 50)
                    result_y = (self.image_rect.y + 130)
                    

                elif self.direction_faced[0]:
                    result_x = (self.image_rect.x + 50)
                    result_y = (self.image_rect.y + -10)
                






        elif not self.pickaxe.in_animation:
            result_x = 0
            result_y = 0


        self.pickaxe.just_exited_animation = False
        return result_x, result_y

    def updates_the_pickaxe(self, internal_surface, viewport):
        self.pickaxe.update()
        if self.pickaxe.in_animation:
            self.pickaxe.make_animation(internal_surface, self, self.direction_faced)

        if self.in_close_animation:
            self.pickaxe.make_animation(internal_surface, self, self.facing_direction_faced)

        if not self.pickaxe.in_animation:
            self.in_close_animation = False

    def move(self, keys, farmbotany):
        if not farmbotany.paused:
            if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
                self.is_walking = True
            else:
                self.is_walking = False

            if self.can_move:
                if keys[pygame.K_w]:
                    self.rect.y -= self.speed
                    for solid_object in self.solid_objects_list:
                        if solid_object.rect.colliderect(self.rect):
                            self.rect.y += self.speed

                    self.direction[0] = True
                    self.direction_faced[0] = True
                    self.direction_faced[1] = False
                    self.direction_faced[2] = False
                    self.direction_faced[3] = False
                else:
                    self.direction[0] = False
                if keys[pygame.K_s]:
                    self.rect.y += self.speed
                    for solid_object in self.solid_objects_list:
                        if solid_object.rect.colliderect(self.rect):
                            self.rect.y -= self.speed

                    self.direction[1] = True
                    self.direction_faced[0] = False
                    self.direction_faced[1] = True
                    self.direction_faced[2] = False
                    self.direction_faced[3] = False
                else:
                    self.direction[1] = False
                if keys[pygame.K_a]:
                    self.rect.x -= self.speed
                    for solid_object in self.solid_objects_list:
                        if solid_object.rect.colliderect(self.rect):
                            self.rect.x += self.speed
                    
                    self.needs_reverse = False
                    self.direction[2] = True
                    self.direction_faced[0] = False
                    self.direction_faced[1] = False
                    self.direction_faced[2] = True
                    self.direction_faced[3] = False
                else:
                    self.direction[2] = False
                if keys[pygame.K_d]:
                    self.rect.x += self.speed
                    self.needs_reverse = True
                    for solid_object in self.solid_objects_list:
                        if self.rect.collidepoint((solid_object.rect.x - self.farmbotany.viewport.pos_x, solid_object.rect.y - self.farmbotany.viewport.pos_y)):
                            self.rect.x -= self.speed
                
                    self.direction[3] = True
                    self.direction_faced[0] = False
                    self.direction_faced[1] = False
                    self.direction_faced[2] = False
                    self.direction_faced[3] = True
                else:
                    self.direction[3] = False
                if keys[pygame.K_v]:
                    self.is_key_v_pressed = True
                else:
                    self.is_key_v_pressed = False
    
    def actual_rect_update(self, viewport):
        self.actual_rect = pygame.Rect(
            self.rect.x - viewport.pos_x - 25,  # Apply the same x-offset as image_rect
            self.rect.y - viewport.pos_y - 50,  # Apply the same y-offset as image_rect
            50, 25
        )

        self.nearby_rect = pygame.Rect(self.rect.x - 64, self.rect.y - 64, 128, 128)