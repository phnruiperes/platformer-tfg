import pygame, sys
from level import Level
from settings import *
from rlenv import TestEnv
from numpy.random import randint

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
    testEnv = TestEnv()
    testEnv.reset()
    done = False
    while not done:
        done = testEnv.step(action=randint(0,3))[2]
    aux = list(testEnv.map[0])           
    aux[0] = 'P'
    testEnv.map[0] = ''.join(aux)
    main = Main(map=testEnv.map)
    main.run()

    
