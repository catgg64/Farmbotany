import pygame
from globals import *

class Axe:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.anim_frames = 0
        self.animation_speed = 5
        sprite_sheet = pygame.image.load("Sprites/tile_set.png")
        self.in_animation = False
        self.just_exited_animation = False
        self.exited_animation = False
        self.axe_size = 100
        self.frame_one = sprite_sheet.subsurface(pygame.Rect(768, 2976, 32, 32))
        self.frame_two = sprite_sheet.subsurface(pygame.Rect(800, 2976, 32, 32))
        self.frame_three = sprite_sheet.subsurface(pygame.Rect(832, 2976, 32, 32))
        self.frame_four = sprite_sheet.subsurface(pygame.Rect(864, 2976, 32, 32))
        self.frame_five = sprite_sheet.subsurface(pygame.Rect(896, 2976, 32, 32))
        self.frame_six = sprite_sheet.subsurface(pygame.Rect(928, 2976, 32, 32))
        self.frame_one = pygame.transform.scale(self.frame_one, (self.axe_size, self.axe_size))
        self.frame_two = pygame.transform.scale(self.frame_two, (self.axe_size, self.axe_size))
        self.frame_three = pygame.transform.scale(self.frame_three, (self.axe_size, self.axe_size))
        self.frame_four = pygame.transform.scale(self.frame_four, (self.axe_size, self.axe_size))
        self.frame_five = pygame.transform.scale(self.frame_five, (self.axe_size, self.axe_size))
        self.frame_six = pygame.transform.scale(self.frame_six, (self.axe_size, self.axe_size))
        self.flipped_frame_one = pygame.transform.flip(self.frame_one, True, False)
        self.flipped_frame_two = pygame.transform.flip(self.frame_two, True, False)
        self.flipped_frame_three = pygame.transform.flip(self.frame_three, True, False)
        self.flipped_frame_four = pygame.transform.flip(self.frame_four, True, False)
        self.flipped_frame_five = pygame.transform.flip(self.frame_five, True, False)
        self.flipped_frame_six = pygame.transform.flip(self.frame_six, True, False)
        self.up_view_frame_one = sprite_sheet.subsurface(pygame.Rect(768, 2944, 32, 32))
        self.up_view_frame_two = sprite_sheet.subsurface(pygame.Rect(800, 2944, 32, 32))
        self.up_view_frame_three = sprite_sheet.subsurface(pygame.Rect(832, 2944, 32, 32))
        self.up_view_frame_four = sprite_sheet.subsurface(pygame.Rect(864, 2944, 32, 32))
        self.up_view_frame_five = sprite_sheet.subsurface(pygame.Rect(896, 2944, 32, 32))
        self.up_view_frame_six = sprite_sheet.subsurface(pygame.Rect(928, 2944, 32, 32))
        self.up_view_frame_one = pygame.transform.scale(self.up_view_frame_one, (self.axe_size, self.axe_size))
        self.up_view_frame_two = pygame.transform.scale(self.up_view_frame_two, (self.axe_size, self.axe_size))
        self.up_view_frame_three = pygame.transform.scale(self.up_view_frame_three, (self.axe_size, self.axe_size))
        self.up_view_frame_four = pygame.transform.scale(self.up_view_frame_four, (self.axe_size, self.axe_size))
        self.up_view_frame_five = pygame.transform.scale(self.up_view_frame_five, (self.axe_size, self.axe_size))
        self.up_view_frame_six = pygame.transform.scale(self.up_view_frame_six, (self.axe_size, self.axe_size))
        self.flipped_up_view_frame_one = pygame.transform.flip(self.up_view_frame_one, False, True)
        self.flipped_up_view_frame_two = pygame.transform.flip(self.up_view_frame_two, False, True)
        self.flipped_up_view_frame_three = pygame.transform.flip(self.up_view_frame_three, False, True)
        self.flipped_up_view_frame_four = pygame.transform.flip(self.up_view_frame_four, False, True)
        self.flipped_up_view_frame_five = pygame.transform.flip(self.up_view_frame_five, False, True)
        self.flipped_up_view_frame_six = pygame.transform.flip(self.up_view_frame_six, False, True)


    def update(self):
        self.anim_frames += 1

    def reset_animation_frames(self):
        self.anim_frames = 0

    def start_animation(self, x, y, floutwitch):
        self.in_animation = True
        self.x = x
        self.y = y
        self.anim_frames = 0
        floutwitch.can_move = False

    def make_animation(self, screen, floutwitch, direction):

        self.exited_animation = False

        if self.in_animation == True:
            if direction[3]:
                if self.anim_frames < self.animation_speed * 1:
                    screen.blit(self.frame_one, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 1 and self.anim_frames <= self.animation_speed * 2:
                    screen.blit(self.frame_two, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 2 and self.anim_frames <= self.animation_speed * 3:
                    screen.blit(self.frame_three, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 3 and self.anim_frames <= self.animation_speed * 4:
                    screen.blit(self.frame_four, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 4 and self.anim_frames <= self.animation_speed * 5:
                    screen.blit(self.frame_five, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 5 and self.anim_frames <= self.animation_speed * 6:
                    screen.blit(self.frame_six, (self.x, self.y))
                if self.anim_frames == self.animation_speed * 6 - 1:
                    self.exited_animation = True
                if self.anim_frames > self.animation_speed * 6:
                    self.anim_frames = 0
                    self.in_animation = False
                    floutwitch.can_move = True
                    self.just_exited_animation = True
            elif direction[2]:
                if self.anim_frames < self.animation_speed * 1:
                    screen.blit(self.flipped_frame_one, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 1 and self.anim_frames <= self.animation_speed * 2:
                    screen.blit(self.flipped_frame_two, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 2 and self.anim_frames <= self.animation_speed * 3:
                    screen.blit(self.flipped_frame_three, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 3 and self.anim_frames <= self.animation_speed * 4:
                    screen.blit(self.flipped_frame_four, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 4 and self.anim_frames <= self.animation_speed * 5:
                    screen.blit(self.flipped_frame_five, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 5 and self.anim_frames <= self.animation_speed * 6:
                    screen.blit(self.flipped_frame_six, (self.x, self.y))
                if self.anim_frames == self.animation_speed * 6 - 1:
                    self.exited_animation = True
                if self.anim_frames > self.animation_speed * 6:
                    self.anim_frames = 0
                    self.in_animation = False
                    floutwitch.can_move = True
                    self.just_exited_animation = True
            elif direction[1]:
                if self.anim_frames <= self.animation_speed * 1:
                    screen.blit(self.flipped_up_view_frame_one, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 1 and self.anim_frames <= self.animation_speed * 2:
                    screen.blit(self.flipped_up_view_frame_two, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 2 and self.anim_frames <= self.animation_speed * 3:
                    screen.blit(self.flipped_up_view_frame_three, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 3 and self.anim_frames <= self.animation_speed * 4:
                    screen.blit(self.flipped_up_view_frame_four, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 4 and self.anim_frames <= self.animation_speed * 5:
                    screen.blit(self.flipped_up_view_frame_five, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 5 and self.anim_frames <= self.animation_speed * 6:
                    screen.blit(self.flipped_up_view_frame_six, (self.x, self.y))
                if self.anim_frames == self.animation_speed * 6 - 1:
                    self.exited_animation = True
                if self.anim_frames > self.animation_speed * 6:
                    self.anim_frames = 0
                    self.in_animation = False
                    floutwitch.can_move = True
                    self.just_exited_animation = True
            elif direction[0]:
                if self.anim_frames < self.animation_speed * 1:
                    screen.blit(self.up_view_frame_one, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 1 and self.anim_frames <= self.animation_speed * 2:
                    screen.blit(self.up_view_frame_two, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 2 and self.anim_frames <= self.animation_speed * 3:
                    screen.blit(self.up_view_frame_three, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 3 and self.anim_frames <= self.animation_speed * 4:
                    screen.blit(self.up_view_frame_four, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 4 and self.anim_frames <= self.animation_speed * 5:
                    screen.blit(self.up_view_frame_five, (self.x, self.y))
                if self.anim_frames > self.animation_speed * 5 and self.anim_frames <= self.animation_speed * 6:
                    screen.blit(self.up_view_frame_six, (self.x, self.y))
                if self.anim_frames == self.animation_speed * 6 - 1:
                    self.exited_animation = True
                if self.anim_frames > self.animation_speed * 6:
                    self.anim_frames = 0
                    self.in_animation = False
                    floutwitch.can_move = True
                    self.just_exited_animation = True

