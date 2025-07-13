import pygame

from tilemanager import *
from axe import *

class Floutwitch():
    def __init__(self, pos_x, pos_y, internal_surface):
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
        self.axe = Axe(self.rect.x, self.rect.y)
        self.can_move = True
        self.front_pos_x = 0
        self.front_pos_y = 0
        self.is_key_v_pressed = False
        self.axe_action = False
        self.direction = [False, False, False, False]
        self.direction_faced = [False, False, False, False]
        self.in_close_animation = False
        self.facing_direction = False
        self.internal_surface = internal_surface
        self.gold = 0

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
        

        if self.direction_faced[2]:
            self.internal_surface.blit(self.image_right, ((self.rect.x) + -25, (self.rect.y) + -50))
        elif self.direction_faced[3]:
            self.internal_surface.blit(self.image_left, ((self.rect.x) + -25, (self.rect.y) + -50))
        elif self.direction_faced[0]:
            self.internal_surface.blit(self.image_up, ((self.rect.x) + -25, (self.rect.y) + -50))
        elif self.direction_faced[1]:
            self.internal_surface.blit(self.image_down, ((self.rect.x) + -25, (self.rect.y) + -50))
        else:
            self.internal_surface.blit(self.image_down, ((self.rect.x) + -25, (self.rect.y) + -50))
        
        #pygame.draw.rect(internal_surface, "blue", self.rect)

    def make_axe_interaction(self, internal_surface, viewport, farmbotany):
        self.axe.update()

        result_x = 0
        result_y = 0
        
        if not farmbotany.paused:

            # if self.axe_action:

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
                        
            #         if actual_pos[0] > 60 and not self.axe.in_animation and not self.axe.just_exited_animation:
            #             self.front_pos_x = (self.rect.x) + 80
            #             self.front_pos_y = (self.rect.y) + 0
            #             self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
            #             self.in_close_animation = True


            #         elif actual_pos[0] < 0 and not self.axe.in_animation and not self.axe.just_exited_animation:
            #             self.front_pos_x = (self.rect.x) + (280 - 350)
            #             self.front_pos_y = (self.rect.y) + 0
            #             self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
            #             self.in_close_animation = True


            #         elif actual_pos[1] > 0 and not self.axe.in_animation and not self.axe.just_exited_animation:
            #             self.front_pos_x = (self.rect.x) + 10
            #             self.front_pos_y = (self.rect.y) + (90 - 350)
            #             self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
            #             self.in_close_animation = True


            #         elif actual_pos[1] < 0 and not self.axe.in_animation and not self.axe.just_exited_animation:
            #             self.front_pos_x = (self.rect.x) + 10
            #             self.front_pos_y = (self.rect.y) + (240 - 350)
            #             self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
            #             self.in_close_animation = True

            #         self.axe.make_animation(internal_surface, self, self.facing_direction)



            if self.axe_action:
                if self.direction[3] and not self.axe.in_animation and not self.axe.just_exited_animation:
                    self.front_pos_x = self.image_rect.x + 80
                    self.front_pos_y = self.image_rect.y + 0
                    self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.image_rect.x + 150)
                    result_y = (self.image_rect.y + 70)
                    

                elif self.direction[2] and not self.axe.in_animation and not self.axe.just_exited_animation:
                    self.front_pos_x = self.image_rect.x + (280 - 350)
                    self.front_pos_y = self.image_rect.y + 0
                    self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.image_rect.x + -70)
                    result_y = (self.image_rect.y + 70)
                    

                elif self.direction[1] and not self.axe.in_animation and not self.axe.just_exited_animation:
                    self.front_pos_x = self.image_rect.x + 20
                    self.front_pos_y = self.image_rect.y + (240 - 150)
                    self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.image_rect.x + 50)
                    result_y = (self.image_rect.y + 130)
                    

                elif self.direction[0] and not self.axe.in_animation and not self.axe.just_exited_animation:
                    self.front_pos_x = self.image_rect.x + 10
                    self.front_pos_y = self.image_rect.y + (90 - 150)
                    self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.image_rect.x + 50)
                    result_y = (self.image_rect.y + -10)
                    

                self.axe.make_animation(internal_surface, self, self.direction)

        if self.axe.in_animation:
            self.axe.make_animation(internal_surface, self, self.direction)

        if self.in_close_animation:
            self.axe.make_animation(internal_surface, self, self.facing_direction)

        if not self.axe.in_animation:
            self.in_close_animation = False





        elif not self.axe.in_animation:
            result_x = 0
            result_y = 0


        self.axe.just_exited_animation = False
        return result_x, result_y

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
                        if solid_object.rect.colliderect(self.rect):
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