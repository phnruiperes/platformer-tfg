import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos: tuple,size: int):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("yellow")
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, shift: int):
        self.rect.x += shift
        # self.move()
        # self.applyGravity()
