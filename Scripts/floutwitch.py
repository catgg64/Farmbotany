import pygame

from tilemanager import *
from axe import *

class Floutwitch():

    def __init__(self, pos_x, pos_y, internal_surface):
        self.image = pygame.image.load("Sprites/tile_set.png").convert_alpha()
        self.substract_rect = pygame.Rect(2016, 2912, 32, 32)
        self.image = self.image.subsurface(self.substract_rect)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.fliped_image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
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

        self.speed = 5
        self.is_walking = False
        self.needs_reverse = False

    def update(self, internal_surface, viewport, current_tile_map, current_tile_map_width, current_tile_map_lengh, mouse_pos, slot_tile_map):
        self.tile_map = current_tile_map
        self.tile_map_width = current_tile_map_width
        self.tile_map_lengh = current_tile_map_lengh
        self.mouse_pos = mouse_pos
        self.viewport = viewport
        self.slot_tile_map = slot_tile_map
        self.actual_floutwitch_position = (self.rect.x - viewport.pos_x + 350, self.rect.y - viewport.pos_y + 150)

        #print(-1 * (self.rect.x - viewport.pos_x - 350), -1 * (self.rect.y - viewport.pos_y - 150))
        #print(self.mouse_pos[0] - (-1 * (self.rect.x - viewport.pos_x - 350)),
        #      self.mouse_pos[1] - (-1 * (self.rect.y - viewport.pos_y - 150)))

        if self.needs_reverse:
            self.internal_surface.blit(self.image, ((self.rect.x) + 0, (self.rect.y) + 0))
        else:
            self.internal_surface.blit(self.fliped_image, ((self.rect.x) + 0, (self.rect.y) + 0))
        #pygame.draw.rect(internal_surface, "blue", self.rect)

    def make_axe_interaction(self, internal_surface, viewport):
        self.axe.update()

        result_x = 0
        result_y = 0

        if self.axe_action:

            is_done = False

            distance_from_cursor_x, distance_from_cursor_y = self.mouse_pos[0] - (
                        -1 * (self.rect.x - viewport.pos_x - 350)), self.mouse_pos[1] - (
                                                                         -1 * (self.rect.y - viewport.pos_y - 150))

            if distance_from_cursor_x < 108 and distance_from_cursor_x > -32 and distance_from_cursor_y < 153 and distance_from_cursor_y > -32:
                pos = position_to_tile_value(self.mouse_pos[0], self.mouse_pos[1], self.tile_map_width,
                                             self.tile_map_lengh, 64, viewport.pos_x, viewport.pos_y)
                grid_pos = tile_value_to_position(pos, self.tile_map_width, 64)
                actual_pos = (grid_pos[0] - self.actual_floutwitch_position[0], grid_pos[1] - self.actual_floutwitch_position[1])
                pos = round(pos)
                self.tile_map[pos].id = "2"
                is_done = True

                self.facing_direction = [False, False, False, False]

                if actual_pos[0] < 0:
                    self.facing_direction[2] = True
                elif actual_pos[0] > 60:
                    self.facing_direction[3] = True
                elif actual_pos[1] < 0:
                    self.facing_direction[0] = True
                elif actual_pos[1] > 0:
                    self.facing_direction[1] = True

                if actual_pos[0] > 60 and not self.axe.in_animation and not self.axe.just_exited_animation:
                    self.front_pos_x = (viewport.pos_x - self.rect.x) + 80
                    self.front_pos_y = (viewport.pos_y - self.rect.y) + 0
                    self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    self.in_close_animation = True


                elif actual_pos[0] < 0 and not self.axe.in_animation and not self.axe.just_exited_animation:
                    self.front_pos_x = (viewport.pos_x - self.rect.x) + (280 - 350)
                    self.front_pos_y = (viewport.pos_y - self.rect.y) + 0
                    self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    self.in_close_animation = True


                elif actual_pos[1] > 0 and not self.axe.in_animation and not self.axe.just_exited_animation:
                    self.front_pos_x = (viewport.pos_x - self.rect.x) + 20
                    self.front_pos_y = (viewport.pos_y - self.rect.y) + (240 - 350)
                    self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    self.in_close_animation = True


                elif actual_pos[1] < 0 and not self.axe.in_animation and not self.axe.just_exited_animation:
                    self.front_pos_x = (viewport.pos_x - self.rect.x) + 10
                    self.front_pos_y = (viewport.pos_y - self.rect.y) + (90 - 350)
                    self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    self.in_close_animation = True

                self.axe.make_animation(internal_surface, self, self.facing_direction)



        if self.axe_action:
            if not is_done:
                if self.direction[3] and not self.axe.in_animation and not self.axe.just_exited_animation:
                    self.front_pos_x = self.rect.x + 80
                    self.front_pos_y = self.rect.y + 0
                    self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.rect.x + 150)
                    result_y = (self.rect.y + 70)
                    print(result_x, result_y)

                elif self.direction[2] and not self.axe.in_animation and not self.axe.just_exited_animation:
                    self.front_pos_x = self.rect.x + (280 - 350)
                    self.front_pos_y = self.rect.y + 0
                    self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.rect.x + -70)
                    result_y = (self.rect.y + 70)
                    print(result_x, result_y)

                elif self.direction[1] and not self.axe.in_animation and not self.axe.just_exited_animation:
                    self.front_pos_x = self.rect.x + 20
                    self.front_pos_y = self.rect.y + (240 - 150)
                    self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.rect.x + 50)
                    result_y = (self.rect.y + 130)
                    print(result_x, result_y)

                elif self.direction[0] and not self.axe.in_animation and not self.axe.just_exited_animation:
                    self.front_pos_x = self.rect.x + 10
                    self.front_pos_y = self.rect.y + (90 - 150)
                    self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                    result_x = (self.rect.x + 50)
                    result_y = (self.rect.y + -10)
                    print(result_x, result_y)

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

    def move(self, keys):
        if self.can_move:
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
                self.is_walking = True
                self.direction[0] = True
            else:
                self.direction[0] = False
            if keys[pygame.K_s]:
                self.rect.y += self.speed
                self.is_walking = True
                self.direction[1] = True
            else:
                self.direction[1] = False
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
                self.is_walking = True
                self.needs_reverse = False
                self.direction[2] = True
            else:
                self.direction[2] = False
            if keys[pygame.K_d]:
                self.rect.x += self.speed
                self.is_walking = True
                self.needs_reverse = True
                self.direction[3] = True
            else:
                self.direction[3] = False
            if keys[pygame.K_v]:
                self.is_key_v_pressed = True
            else:
                self.is_key_v_pressed = False