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
        self.size = (32,32)
        self.load_images()
        #self.image = self.standing_frames[0]
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.acc_max = vec()
        self.rot = 0
        self.last_shot = 0


        self.gun_status = [True, True]
        self.gun_select = 0
        #1 is pistol 2 is shotgun


    def load_images(self):
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.image.fill(BLACK)
        pass

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            self.gun=[True,False]
            self.gun_select = 0
            print('pistol')
        if keys[pg.K_2]:
            self.gun=[False,True]
            self.gun_select = 1
            print('shotgun')
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_w]:
            self.acc.y = -PLAYER_ACC
        if keys[pg.K_s]:
            self.acc.y = PLAYER_ACC
        key = pg.mouse.get_pressed()
        if key[0]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1,0).rotate(self.rot)
                Bullet(self.game, self.pos, dir)
            if self.gun_select == 0:
                if self.gun_status[0] == True:
                    now = pg.time.get_ticks()
                    if now - self.last_shot > BULLET_RATE:
                        self.last_shot = now
                        dir = vec(1,0).rotate(self.rot)
                        Bullet(self.game, self.pos, dir)
            if self.gun_select == 1:
                if self.gun_status[1] == True:
                    now = pg.time.get_ticks()
                    if now - self.last_shot > BULLET_RATE:
                        self.last_shot = now
                        dir = vec(1,0).rotate(self.rot - 10 )
                        Bullet(self.game, self.pos, dir)
                        dir = vec(1,0).rotate(self.rot - 5 )
                        Bullet(self.game, self.pos, dir)
                        dir = vec(1,0).rotate(self.rot)
                        Bullet(self.game, self.pos, dir)
                        dir = vec(1,0).rotate(self.rot + 5)
                        Bullet(self.game, self.pos, dir)
                        dir = vec(1,0).rotate(self.rot + 10)
                        Bullet(self.game, self.pos, dir)


    def update(self):
        self.acc = vec(0,0)
        self.get_keys()
        self.animate()
        self.rotate()

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
        self.rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.centerx = self.pos.x
        self.collide_with_enemy('x')
        self.rect.centery = self.pos.y
        self.collide_with_enemy('y')

    def collide_with_walls(self,dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width/2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.rect.width/2
                self.vel.x = 0
                self.rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height/2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.rect.height/2
                self.vel.y = 0
                self.rect.centery = self.pos.y

    def collide_with_enemy(self,dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.enemys, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width/2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.rect.width/2
                self.vel.x = 0
                self.rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.enemys, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height/2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.rect.height/2
                self.vel.y = 0
                self.rect.centery = self.pos.y


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
        self.rot = angle
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)
    def shotgun(self):
        pass
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
class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size = (6,6)
        self.load_images()
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()


    def load_images(self):
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.image.fill(RED)
        pass

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()





class enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemys
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.rect.x = self.pos.x*TILESIZE
        self.rect.y = self.pos.y*TILESIZE

    def update(self):
        self.rect.x -= 1
      

#아이템 상자 생성
class Feed(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.feeds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(WHITE)

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

# def draw_object(surface, color, pos):
#     r = pg.Rect((pos[0], pos[1]), (TILESIZE, TILESIZE))
#     pg.draw.rect(surface, color, r)

