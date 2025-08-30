import pygame

from code.EnemyShot import EnemyShot
from code.Entity import Entity
# Importe as novas constantes que acabamos de criar
from code.const import ENTITY_SPEED, ENTITY_SHOT_DELAY, \
    ENEMY_FRAME_WIDTH, ENEMY_FRAME_HEIGHT, \
    ENEMY_NUM_FRAMES, ENTITY_SHOT_OFFSET


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position, load_image=False)

        self.FRAME_WIDTH = ENEMY_FRAME_WIDTH
        self.FRAME_HEIGHT = ENEMY_FRAME_HEIGHT
        self.NUM_FRAMES = ENEMY_NUM_FRAMES
        self.frames = []

        spritesheet = pygame.image.load(f'./asset/{self.name}.png').convert_alpha()

        for i in range(self.NUM_FRAMES):
            frame_image = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
            frame_image.blit(spritesheet, (0, 0), (i * self.FRAME_WIDTH, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT))
            self.frames.append(frame_image)

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)

        self.last_update_time = pygame.time.get_ticks()
        self.animation_speed_ms = 150 # Ajuste a velocidade da animação da fada aqui

        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self, ):
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.animation_speed_ms:
            self.last_update_time = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            old_center = self.rect.center
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(center=old_center)

        self.rect.centerx -= ENTITY_SPEED[self.name]

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            offset_x, offset_y = ENTITY_SHOT_OFFSET[self.name]
            shot_pos = (self.rect.centerx + offset_x, self.rect.centery + offset_y)
            return EnemyShot(name=f'{self.name}Shot', position=shot_pos)