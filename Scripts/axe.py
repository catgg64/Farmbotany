import pygame
from globals import *

class Axe:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.anim_frames = 0
        self.animation_speed = 10
        sprite_sheet = pygame.image.load("Sprites/tile_set.png")
        self.frame_one = sprite_sheet.subsurface(pygame.Rect(768, 2976, 32, 32))
        self.frame_two = sprite_sheet.subsurface(pygame.Rect(800, 2976, 32, 32))
        self.frame_three = sprite_sheet.subsurface(pygame.Rect(832, 2976, 32, 32))
        self.frame_four = sprite_sheet.subsurface(pygame.Rect(864, 2976, 32, 32))
        self.frame_five = sprite_sheet.subsurface(pygame.Rect(896, 2976, 32, 32))
        self.frame_six = sprite_sheet.subsurface(pygame.Rect(928, 2976, 32, 32))
        self.frame_one = pygame.transform.scale(self.frame_one, (100, 100))
        self.frame_two = pygame.transform.scale(self.frame_two, (100, 100))
        self.frame_three = pygame.transform.scale(self.frame_three, (100, 100))
        self.frame_four = pygame.transform.scale(self.frame_four, (100, 100))
        self.frame_five = pygame.transform.scale(self.frame_five, (100, 100))
        self.frame_six = pygame.transform.scale(self.frame_six, (100, 100))


    def update(self, x, y, screen):
        self.x = x
        self.y = y
        self.anim_frames += 1
        if self.anim_frames < self.animation_speed * 1:
            screen.blit(self.frame_one, (self.x, self.y))
        if self.anim_frames > self.animation_speed * 1 and self.anim_frames < self.animation_speed * 3:
            screen.blit(self.frame_two, (self.x, self.y))
        if self.anim_frames > self.animation_speed * 3 and self.anim_frames < self.animation_speed * 4:
            screen.blit(self.frame_three, (self.x, self.y))
        if self.anim_frames > self.animation_speed * 4 and self.anim_frames < self.animation_speed * 5:
            screen.blit(self.frame_four, (self.x, self.y))
        if self.anim_frames > self.animation_speed * 5 and self.anim_frames < self.animation_speed * 6:
            screen.blit(self.frame_five, (self.x, self.y))
        if self.anim_frames > self.animation_speed * 6 and self.anim_frames < self.animation_speed * 7:
            screen.blit(self.frame_six, (self.x, self.y))
        if self.anim_frames > self.animation_speed * 7:
            self.anim_frames = 0


    def reset_animation_frames(self):
        self.anim_frames = 0