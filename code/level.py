import pygame
from player import Player
from coin import Coin
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, size: int):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('#888888')
        self.rect = self.image.get_rect(topleft=pos)
    
    def update(self,shift: int):
        self.rect.x += shift

class Level:
    def __init__(self,level_map,surface):
        self.surface = surface
        self.encoded_map = level_map
        self.setup_level(self.encoded_map)
        self.shift = 0
        
    def setup_level(self,level_map):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.coins = pygame.sprite.Group()
        for row_index,row_data in enumerate(level_map):
            for col_index,tile_info in enumerate(row_data):
                x = col_index*TILE_SIZE
                y = row_index*TILE_SIZE
                if tile_info == 1: 
                    self.tiles.add(Tile((x,y),TILE_SIZE))
                elif tile_info == 2:
                    self.coins.add(Coin((x+(TILE_SIZE-COIN_SIZE)/2,y+(TILE_SIZE-COIN_SIZE)/2),COIN_SIZE))
                elif tile_info == 3:                   
                    self.player.add(Player((x,y)))
    
    def reset(self):
        self.player.empty()
        self.tiles.empty()
        self.coins.empty()
        self.setup_level(self.encoded_map)
                    
    def scroll(self):
        if self.player:
            player = self.player.sprite
            player_x = player.rect.centerx
            direction_x = player.direction.x
            
            if player_x < WINDOW_WIDTH*0.4 and direction_x < 0:
                self.shift = 6
                player.speed = 0
            elif player_x > WINDOW_WIDTH*0.6 and direction_x > 0:
                self.shift = -6
                player.speed = 0
            else:
                self.shift = 0
                player.speed = 6
            

    def hCollision(self):
        if self.player:
            player = self.player.sprite
            player.move()
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                        
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left
                    
    def vCollision(self):
        if self.player:
            player = self.player.sprite
            player.applyGravity()
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        #jump
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_SPACE]:
                            player.direction.y = -player.jump_heigh
                            player.rect.y += player.direction.y
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0

    def render(self):
        self.tiles.update(self.shift)
        self.tiles.draw(self.surface)
        
        self.player.update()
        self.player.draw(self.surface)

        self.coins.update(self.shift)
        self.coins.draw(self.surface)

        self.hCollision()
        self.vCollision()
        self.scroll()

        
