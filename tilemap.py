import pygame as pg
from setting import *

def collide_hit_rect(first, second):
    return first.hitbox.colliderect(second.rect)
class Map:
    def __init__(self, filename):
        self.data = []
        #read data from filename
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        #store data of the map

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # if the player go right, the map should go to right. 
        # and player will in the middle of the game so add WIDTH /2
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        x = min(0,x) # left
        y = min(0,y) # top
        x = max(-(self.width - WIDTH), x) #right
        y = max(-(self.height - HEIGHT), y) #bottom
        self.camera = pg.Rect(x,y,self.width, self.height)
        