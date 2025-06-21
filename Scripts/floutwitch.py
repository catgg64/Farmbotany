import pygame
from axe import *

class Floutwitch():

    def __init__(self, pos_x, pos_y):
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

        self.speed = 5
        self.is_walking = False
        self.needs_reverse = False

    def draw(self, screen, viewport):



        if self.needs_reverse:
            screen.blit(self.image, ((viewport.pos_x - self.rect.x) + 350, (viewport.pos_y - self.rect.y) + 150))
        else:
            screen.blit(self.fliped_image, ((viewport.pos_x - self.rect.x) + 350, (viewport.pos_y - self.rect.y) + 150))
        #pygame.draw.rect(screen, "blue", self.rect)

    def make_axe_interaction(self, screen, viewport):
        self.axe.update()
        self.axe.make_animation(screen, self, self.direction)
        result_x = 0
        result_y = 0
        if self.axe_action:

            if self.direction[3] and not self.axe.in_animation and not self.axe.just_exited_animation:
                self.front_pos_x = (viewport.pos_x - self.rect.x) + 430
                self.front_pos_y = (viewport.pos_y - self.rect.y) + 130
                self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                result_x = -1 * ((self.rect.x - viewport.pos_x) - 500)
                result_y = -1 * ((self.rect.y - viewport.pos_y) - 220)

            elif self.direction[2] and not self.axe.in_animation and not self.axe.just_exited_animation:
                self.front_pos_x = (viewport.pos_x - self.rect.x) + 280
                self.front_pos_y = (viewport.pos_y - self.rect.y) + 130
                self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                result_x = -1 * ((self.rect.x - viewport.pos_x) - 280)
                result_y = -1 * ((self.rect.y - viewport.pos_y) - 220)

            elif self.direction[1] and not self.axe.in_animation and not self.axe.just_exited_animation:
                self.front_pos_x = (viewport.pos_x - self.rect.x) + 350
                self.front_pos_y = (viewport.pos_y - self.rect.y) + 240
                self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                result_x = -1 * ((self.rect.x - viewport.pos_x) - 400)
                result_y = -1 * ((self.rect.y - viewport.pos_y) - 280)

            elif self.direction[0] and not self.axe.in_animation and not self.axe.just_exited_animation:
                self.front_pos_x = (viewport.pos_x - self.rect.x) + 350
                self.front_pos_y = (viewport.pos_y - self.rect.y) + 70
                self.axe.start_animation(self.front_pos_x, self.front_pos_y, self)
                result_x = -1 * ((self.rect.x - viewport.pos_x) - 400)
                result_y = -1 * ((self.rect.y - viewport.pos_y) - 160)







        elif not self.axe.in_animation:
            result_x = 0
            result_y = 0


        self.axe.just_exited_animation = False
        return result_x, result_y

    def move(self, keys):
        if self.can_move:
            if keys[pygame.K_w]:
                self.rect.y += self.speed
                self.is_walking = True
                self.direction[0] = True
            else:
                self.direction[0] = False
            if keys[pygame.K_s]:
                self.rect.y -= self.speed
                self.is_walking = True
                self.direction[1] = True
            else:
                self.direction[1] = False
            if keys[pygame.K_a]:
                self.rect.x += self.speed
                self.is_walking = True
                self.needs_reverse = False
                self.direction[2] = True
            else:
                self.direction[2] = False
            if keys[pygame.K_d]:
                self.rect.x -= self.speed
                self.is_walking = True
                self.needs_reverse = True
                self.direction[3] = True
            else:
                self.direction[3] = False
            if keys[pygame.K_v]:
                self.is_key_v_pressed = True
            else:
                self.is_key_v_pressed = False