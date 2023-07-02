import pygame, sys
from level import Level
from settings import *

from numpy.random import randint
import numpy as np

class Main:
    def __init__(self,map):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGH))
        self.clock = pygame.time.Clock()
        self.level = Level(map,self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.level.reset()


            self.screen.fill('black')

            self.level.render()

            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':

    main = Main(map=level_map)
    main.run()

    
