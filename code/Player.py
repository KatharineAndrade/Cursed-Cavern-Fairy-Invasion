import pygame

from code.Entity import Entity
from code.PlayerShot import PlayerShot
from code.const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY, PLAYER_FRAME_WIDTH, PLAYER_FRAME_HEIGHT, PLAYER_NUM_FRAMES


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position, load_image=False)

        self.FRAME_WIDTH = PLAYER_FRAME_WIDTH
        self.FRAME_HEIGHT = PLAYER_FRAME_HEIGHT
        self.NUM_FRAMES = PLAYER_NUM_FRAMES

        self.frames = []
        spritesheet = pygame.image.load(f'./asset/{self.name}.png').convert_alpha()

        for i in range(self.NUM_FRAMES):
            frame_image = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
            frame_image.blit(spritesheet, (0, 0), (i * self.FRAME_WIDTH, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT))
            self.frames.append(frame_image)


        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center = position)

        self.last_update_time = pygame.time.get_ticks()
        self.animation_speed_ms = 150
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self):
        # Lógica de animação
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.animation_speed_ms:
            self.last_update_time = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            old_center = self.rect.center
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(center = old_center)

        # Lógica de movimento
        pressed_key = pygame.key.get_pressed()
        if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < WIN_HEIGHT:
            self.rect.centery += ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            pressed_key = pygame.key.get_pressed()
            if pressed_key[PLAYER_KEY_SHOOT[self.name]]:
                return PlayerShot(name = f'{self.name}Shot', position = (self.rect.centerx, self.rect.centery))

