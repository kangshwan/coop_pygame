# this file is for every game objects.
import os
import pygame as pg
import random
from setting import *
from time import sleep
import math

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.size = (32,48)
        self.load_images()
        #self.image = self.standing_frames[0]
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.acc_max = vec()

    def load_images(self):
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.image.fill(BLACK)
        pass
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_w]:
            self.acc.y = -PLAYER_ACC
        if keys[pg.K_s]:
            self.acc.y = PLAYER_ACC
        
    def update(self):
        self.acc = vec(0,0)
        self.get_keys()
        self.animate()
        # apply friction
        self.acc += self.vel*PLAYER_FRICTION
        #equations of motion
        #print('magnitude:', math.sqrt(self.vel.x**2+self.vel.y**2))
        #print(self.vel)
        #print('accelate:',self.acc)
        self.vel = self.vel + 0.3*self.acc
        if math.sqrt(self.vel.x**2+self.vel.y**2) >3:
            self.vel *= 3/math.sqrt(self.vel.x**2+self.vel.y**2)
        self.pos += self.vel
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.pos -= self.vel
            self.rect.center = self.pos

    def animate(self):
        pass
    def magnitude(self):
        return
    def rotate(self):
        # The vector to the target (the mouse position).
        direction = pg.mouse.get_pos() - self.pos
        # .as_polar gives you the polar coordinates of the vector,
        # i.e. the radius (distance to the target) and the angle.
        radius, angle = direction.as_polar()
        # Rotate the image by the negative angle (y-axis in pygame is flipped).
        self.image = pg.transform.rotate(self.orig_image, -angle)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)

class Leg(Player):
    def __init__(self,game):
        super().__init__(game)
        #under this is for test
        self.angle = 0


    #Overriding
    def load_images(self):
        self.image = pg.Surface((16,48),pg.SRCALPHA)
        self.image.fill(LIGHTBLUE)
        pass
    #Overriding
    def update(self):
        self.rotate()
        super().update()
        #print('arm pos', self.pos)

        pass
class bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.load_images()
        self.image = self

    def load_images(self):
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.image.fill(BLACK)
        pass
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(LIGHTBLUE)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.rect.x = self.pos.x*TILESIZE
        self.rect.y = self.pos.y*TILESIZE


