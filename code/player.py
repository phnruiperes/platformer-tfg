import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple):
        super().__init__()
        self.image = pygame.Surface((36,50))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2(0,0)
        self.speed = 6
        self.gravity = 1
        self.jump_heigh = 20

    def move(self):
        keys = pygame.key.get_pressed()
        #walk
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        self.rect.x += self.direction.x * self.speed
    
    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        pass
        #self.move()
        #self.applyGravity()
        