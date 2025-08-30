import pygame

from code.Entity import Entity
from code.const import WIN_WIDTH, ENTITY_SPEED, WIN_HEIGHT


class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.image = pygame.transform.scale(self.image, (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.image.get_rect(topleft = position)


    def move(self, ):
        self.rect.centerx -= ENTITY_SPEED[self.name]
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH

