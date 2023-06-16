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
                    print('(',len(level_map),',',len(level_map[0]),') =',len(level_map)*len(level_map[0]))
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')

            self.level.render()

            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    heigh = 11
    width = 28
    generator = np.random.default_rng(3134892)
    level = np.zeros(shape=(heigh,width),dtype=int)
    discount = 0
    for i in range(heigh):
        for j in range(width):
            pick = generator.choice([0,1,2],p=[0.8*(1-discount),0.8*discount,0.2])
            level[i][j] = pick
        discount += 1/heigh
    level[len(level)-3][0] = 3
    print(level)
    main = Main(map=level_map)
    main.run()
    

    
