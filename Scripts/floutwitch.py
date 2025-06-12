import pygame

class Floutwitch():

    def __init__(self, pos_x, pos_y):
        self.image = pygame.image.load("Sprites/tile_set.png").convert_alpha()
        self.substract_rect = pygame.Rect(2016, 2912, 32, 32)
        self.image = self.image.subsurface(self.substract_rect)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.fliped_image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

        self.speed = 5
        self.is_walking = False
        self.needs_reverse = False

    def draw(self, screen):
        screen.blit(self.image, self.rect,)
        #pygame.draw.rect(screen, "blue", self.rect)

    def move(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.is_walking = True
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            self.is_walking = True
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.is_walking = True
            self.needs_reverse = False
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.is_walking = True
            self.needs_reverse = True