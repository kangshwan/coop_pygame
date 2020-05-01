# this file is for every game objects.
import os
import pygame as pg
import random
from setting import *
from time import sleep
import math

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        # not using now / 현재 미사용중, 이후 img를 넣었을때 frame별로 동작하게 하려고 했으나...(할지 모르겠음)
        self.last_update = 0
        # not using now / 현재 미사용중, 뭔지모르겠음.(5월 3일날까지도 미사용시 제거예정.)
        self.size = (TILESIZE,TILESIZE)
        # showing size of the player / player의 size를 지정해줌. 사실 의미없는짓인것 같아서 이후에 간소화 할시 제거 예정
        self.load_images()
        #self.image = self.standing_frames[0]
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.pos = vec(x*32, y*32)
        
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rot = 0
        self.last_shot = 0

        self.gun_status = [True, True]

        self.gun_select = 0
        #1 is pistol 2 is shotgun


    def load_images(self):
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        # self.image에 Surface를 저장함. 나중에 img 삽입시 self.image에 img가 들어갈것.
        self.image.fill(BLACK)
        # 아무것도 없는 Surface기 때문에 채워줌
        pass

    def get_keys(self):
        # event handling / 이벤트 핸들링
        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            self.gun=[True,False]
            # 총알 갯수를 세기위해 만들었으나 추후 삭제예정
            self.gun_select = 0
            print('pistol')
            # 총기를 잘 집었는지 출력
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
        # add acceleration when press w,a,s,d / w,a,s,d를 눌렀을때 가속을 더해줌.
        key = pg.mouse.get_pressed()
        if key[0]:
            if self.gun_select == 0:
                if self.gun_status[0] == True:
                    now = pg.time.get_ticks()
                    # bring the time when clicked / 딱 클릭된 순간의 시간을 가져옴
                    if now - self.last_shot > BULLET_RATE:
                        # this is for setting the bullet duration.
                        # 초기의 last_shot의 초기값은 0, 이는 총알이 일정 간격을 두고 발사되는것을 염두한것. 
                        # ex)클릭 : 5시 1분 04.500초 바로전 총발사 : 5시 1분 04.300일시 뺐을경우 300이기때문에 총알발사 안됌
                        self.last_shot = now
                        # 이후 now를 last_shot에 저장해줌.
                        dir = vec(1,0).rotate(self.rot)
                        Bullet(self.game, self.pos, dir)
            elif self.gun_select == 1:
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
                        # This is for bullet spreads like shotgun
                        # 산탄총 처럼 퍼져나가게 하기 위함


    def update(self):
        self.acc = vec(0,0)
        self.get_keys()
        self.animate()
        self.rotate()
        
        self.acc += self.vel*PLAYER_FRICTION
        #apply friction / 가속력에 마찰력을 더해줌. 현재속력*마찰력(현재는 -0.05로 설정)
        #equations of motion
        self.vel = self.vel + 0.3*self.acc
        if math.sqrt(self.vel.x**2+self.vel.y**2) >3: 
            # this is for stop velocity growing infinitly
            # 속도가 무한정으로 빨라지는것을 방지하기위해 속도(vector)의 magnitude(속력)를 계산하여 magnitude가 3을 넘지 않도록 설정
            self.vel *= 3/math.sqrt(self.vel.x**2+self.vel.y**2)
            # simple vector calculate / 간단한 벡터계산을 이용하였음. 현재속력이 3보다 클경우 3으로 고정하기위한 수식.
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
            # see collide with x axis
            # x 방향으로 충돌 확인
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width/2
                    # x 방향 속도가 양수일 경우 -> 오른쪽으로 진행하고있음 따라서 position을 다시 세팅해줌
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.rect.width/2
                    # x 방향 속도가 음수일 경우 -> 왼쪽으로 진행하고있음 따라서 position을 다시 세팅해줌
                self.vel.x = 0
                # 부딫혔으니 x방향 속도를 0으로 해줌.
                self.rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height/2
                    # y 방향 속도가 양수일 경우 -> 아래으로 진행하고있음 따라서 position을 다시 세팅해줌
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.rect.height/2
                    # y 방향 속도가 양수일 경우 -> 위쪽으로 진행하고있음 따라서 position을 다시 세팅해줌
                self.vel.y = 0
                # 부딫혔으니 y방향 속도를 0으로 해줌
                self.rect.centery = self.pos.y
    #위와 동일할것으로 예상
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
        mouse_pos = pg.mouse.get_pos()
        # window에서 mouse의 절대적인 위치를 가져옴(최대값: [WIDTH,HEIGHT])
        relate_pos = vec(mouse_pos[0] - self.game.camera.camera.x, mouse_pos[1] - self.game.camera.camera.y)
        # mouse의 절대적인 위치 + camera의 x,y 위치. -(minus) 를한 이유는 카메라의 x,y는 음수로 움직이기 때문
        direction = relate_pos - self.pos
        # 이후 player의 위치와 구해둔 상대적인 위치로 방향을 구함.
        # 벡터를 빼서 플레이어에서 마우스 위치를 가리키는 벡터를 구함.
        # .as_polar gives you the polar coordinates of the vector,
        # .as_polar는 벡터를 극좌표계로 나타내줌.
        # i.e. the radius (distance to the target) and the angle.
        radius, angle = direction.as_polar()
        # Rotate the image by the negative angle (y-axis in pygame is flipped).
        # y축이 아래로 증가하므로 극좌표계에서 구한 angle에 -를 해줌
        self.image = pg.transform.rotate(self.orig_image, -angle)
        # 여기에서 orig_image를 사용하는데, 이유는 그냥 image를 사용했다가는 터져버린다. 이미지가 돌아가면서 쭉 늘어나버리기 때문.
        self.rot = angle
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)
    def shotgun(self):
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
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
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
        self.rect = self.image.get_rect()
        self.rect.x = x*TILESIZE
        self.rect.y = y*TILESIZE

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.rect.x = self.pos.x*TILESIZE
        self.rect.y = self.pos.y*TILESIZE

