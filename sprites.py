# this file is for every game objects.
import os
import pygame as pg
import random
from setting import *
from tilemap import *
from time import sleep
import math
vec = pg.math.Vector2

def collide_with_gameobject(sprite,group,dir):
    if dir == 'x':
        # see collide with x axis
        # x 방향으로 충돌 확인
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hitbox.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hitbox.width/2
                # x 방향 속도가 양수일 경우 -> 오른쪽으로 진행하고있음 따라서 position을 다시 세팅해줌
            if hits[0].rect.centerx < sprite.hitbox.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hitbox.width/2
                # x 방향 속도가 음수일 경우 -> 왼쪽으로 진행하고있음 따라서 position을 다시 세팅해줌
            sprite.vel.x = 0
            # 부딫혔으니 x방향 속도를 0으로 해줌.
            sprite.hitbox.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False,collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hitbox.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hitbox.height/2
                # y 방향 속도가 양수일 경우 -> 아래으로 진행하고있음 따라서 position을 다시 세팅해줌
            if hits[0].rect.centery < sprite.hitbox.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hitbox.height/2
                # y 방향 속도가 양수일 경우 -> 위쪽으로 진행하고있음 따라서 position을 다시 세팅해줌
            sprite.vel.y = 0
            # 부딫혔으니 y방향 속도를 0으로 해줌
            sprite.hitbox.centery = sprite.pos.y

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
        self.hitbox = PLAYER_HIT_BOX
        self.hitbox.center = self.rect.center
        self.pos = vec(x, y)*TILESIZE
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rot = 0
        self.last_shot = 0
        self.gun_status = [[True,1], [False, 0],[False, 0],[False, 0]]
        # 0 is pistol, 1 is shotgun, 2 is sniper 3 is flamethrower
        self.gun_select = 0
        self.last_grenade = 0
        #0 is pistol 1 is shotgun
        self.last_speed = 0
        self.now =pg.time.get_ticks()
        self.max_speed = 3
        self.health = PLAYER_HEALTH
        self.weapon = 'pistol'
        self.weapon_rate = WEAPONS[self.weapon]['rate']
        self.weapon_damage = WEAPONS[self.weapon]['damage']

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
            self.gun_select = 0
            self.weapon = 'pistol'
            self.weapon_rate = WEAPONS[self.weapon]['rate']
            self.weapon_damage = WEAPONS[self.weapon]['damage']

            # 총기를 잘 집었는지 출력
        if keys[pg.K_2]:
            self.gun_select = 1
            self.weapon = 'shotgun'
            self.weapon_rate = WEAPONS[self.weapon]['rate']
            self.weapon_damage = WEAPONS[self.weapon]['damage']
        if keys[pg.K_3]:
            self.gun_select = 2
            self.weapon = 'sniper'
            self.weapon_rate = WEAPONS[self.weapon]['rate']
            self.weapon_damage = WEAPONS[self.weapon]['damage']

        if keys[pg.K_4]:
            self.gun_select = 3
            self.weapon = 'flamethrower'
            self.weapon_rate = WEAPONS[self.weapon]['rate']
            self.weapon_damage = WEAPONS[self.weapon]['damage']
        
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
                if self.gun_status[0][0]:
                    self.shoot(self.gun_select)
            elif self.gun_select == 1:
                if self.gun_status[self.gun_select][0]:
                    self.shoot(self.gun_select)
            elif self.gun_select == 2:
                if self.gun_status[self.gun_select][0]:
                    self.shoot(self.gun_select)
            elif self.gun_select == 3:
                if self.gun_status[self.gun_select][0]:
                    self.shoot(self.gun_select)
        if key[2]:
            #마우스 우클릭시
            now = pg.time.get_ticks()
            print('clicked')
            if now - self.last_grenade > GRENADE_RATE:
                self.last_grenade = now
                dir = vec(1,0).rotate(self.rot)
                relate_pos = vec(pg.mouse.get_pos()[0] - self.game.camera.camera.x, pg.mouse.get_pos()[1] - self.game.camera.camera.y)
                dir_size = relate_pos-self.pos
                Grenade(self.game, self.pos, dir, dir_size.length())
                print('fire in the hole!')

    def shoot(self, gun_select):
        now = pg.time.get_ticks()
        # bring the time when clicked / 딱 클릭된 순간의 시간을 가져옴
        if now - self.last_shot > self.weapon_rate:
            # this is for setting the bullet duration.
            # 초기의 last_shot의 초기값은 0, 이는 총알이 일정 간격을 두고 발사되는것을 염두한것. 
            # ex)클릭 : 5시 1분 04.500초 바로전 총발사 : 5시 1분 04.300일시 뺐을경우 300이기때문에 총알발사 안됌
            self.last_shot = now
            # 이후 now를 last_shot에 저장해줌.
            dir = vec(1,0).rotate(self.rot)
            #self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = random.uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, self.pos, dir.rotate(spread))
            self.gun_status[self.gun_select][1] -= WEAPONS[self.weapon]['bullet_count'] 

            if self.gun_select == 0:
                pass
            elif self.gun_status[self.gun_select][1] <= 0:
                self.gun_status[self.gun_select][0] = False
            print('left bullet', self.gun_status[self.gun_select][1])

    def update(self):
        self.now =pg.time.get_ticks()
        self.acc = vec(0,0)
        self.get_keys()
        self.rotate() 
        self.weapon_rate = WEAPONS[self.weapon]['rate']
        self.acc += self.vel*PLAYER_FRICTION
        #apply friction / 가속력에 마찰력을 더해줌. 현재속력*마찰력(현재는 -0.05로 설정)
        #equations of motion
        self.vel = self.vel + 0.3*self.acc
        if self.vel.length() > self.max_speed: 
            # this is for stop velocity growing infinitly
            # 속도가 무한정으로 빨라지는것을 방지하기위해 속도(vector)의 magnitude(속력)를 계산하여 magnitude가 3을 넘지 않도록 설정
            self.vel *= self.max_speed/self.vel.length()
            # simple vector calculate / 간단한 벡터계산을 이용하였음. 현재속력이 3보다 클경우 3으로 고정하기위한 수식.
        self.pos += self.vel
        self.hitbox.centerx = self.pos.x
        collide_with_gameobject(self, self.game.walls,'x')
        self.hitbox.centery = self.pos.y
        collide_with_gameobject(self, self.game.walls,'y')
        #self.hitbox.centerx = self.pos.x
        #self.collide_with_enemy('x')
        #self.hitbox.centery = self.pos.y
        #self.collide_with_enemy('y')
        self.collide_with_feed()
        self.rect.center = self.hitbox.center

        if self.now - self.last_speed > SPEEDUP_RATE:
            self.max_speed = 3

    
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

    def collide_with_feed(self):
        hits = pg.sprite.spritecollide(self, self.game.feeds, True)
        for hit in hits:
            print(hit.item_no)
            if hit.item_no == 1:
                self.max_speed = 10
                self.last_speed = pg.time.get_ticks()
                self.gun_status[1] = [True, 240]
                self.gun_status[2] = [True, 10]
            self.max_speed = 10
            self.last_speed = pg.time.get_ticks()
            self.gun_status[1] = [True, 240]
            self.gun_status[2] = [True, 10]
            self.gun_status[3] = [True, 500]
            self.weapon_rate *= 0.5
            self.weapon_damage *= 1.5

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

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size = WEAPONS[game.player.weapon]['bullet_size']
        self.load_images()
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        #spread = random.uniform(-BULLET_SPREAD,BULLET_SPREAD)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed']
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

        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()
        
class Grenade(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, magnitude):
        self.groups = game.all_sprites, game.grenades
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size = (10,10)
        self.load_images()
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.dir = dir
        self.speed = GRENADE_SPEED
        self.spawn_time = pg.time.get_ticks()
        
        self.power = magnitude
        if self.power > 300:
            pass
        elif self.power > 200:
            self.speed *= 0.8
        elif self.power > 100:
            self.speed *= 0.6
        else:
            self.speed *= 0.4

    def load_images(self):
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.image.fill(GRENADE)

    def update(self):
        self.vel = self.dir * self.speed
        self.pos += self.vel * self.game.dt
        if self.vel.length() > 0 :
            self.speed -= 10
        elif self.vel.length() < 0 :
            self.vel = 0
        self.rect.centerx = self.pos.x
        self.reflect_with_walls('x')
        self.rect.centery = self.pos.y
        self.reflect_with_walls('y')

        if pg.time.get_ticks() - self.spawn_time > GRENADE_LIFETIME:
            self.kill()
            Explode(self.game, self.pos)

    def reflect_with_walls(self,dir):
        if dir == 'x':
            # see collide with x axis
            # x 방향으로 충돌 확인
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width/2
                    # x 방향 속도가 양수일 경우 -> 오른쪽으로 진행하고있음 따라서 position을 다시 세팅해줌
                    self.reflect((-1,0))
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.rect.width/2
                    # x 방향 속도가 음수일 경우 -> 왼쪽으로 진행하고있음 따라서 position을 다시 세팅해줌
                    self.reflect((1,0))
                self.vel.x = 0
                # 부딫혔으니 x방향 속도를 0으로 해줌.
                self.rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height/2
                    # y 방향 속도가 양수일 경우 -> 아래으로 진행하고있음 따라서 position을 다시 세팅해줌
                    self.reflect((0,-1))
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.rect.height/2
                    # y 방향 속도가 양수일 경우 -> 위쪽으로 진행하고있음 따라서 position을 다시 세팅해줌
                    self.reflect((0,1))
                self.vel.y = 0
                # 부딫혔으니 y방향 속도를 0으로 해줌
                self.rect.centery = self.pos.y
                
    def reflect(self, NV):
        self.dir = self.dir.reflect(pg.math.Vector2(NV))

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.groups = game.all_sprites, game.enemys
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE), pg.SRCALPHA)
        self.image.fill(color)
        self.origin_image = self.image
        self.rect = self.image.get_rect()
        self.hitbox = ENEMY_HIT_BOX.copy()
        self.hitbox.center = self.rect.center
        self.image.fill(RED)
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        #self.rect.x = self.pos.x*TILESIZE
        #self.rect.y = self.pos.y*TILESIZE
        #제 생각에 문제는 단 한번으로 좌표를 할당해도되는데 좌표할당행위를 나눠서 여러번 해서 
        #문제가 생겼던것 같습니다. 이렇게 하니 잘 되는것같네요!

        self.speed = random.choice(ENEMY_SPEED)
        self.rot = 0
        self.health = ENEMY_HEALTH
        
    def avoid_enemys(self):
        for enemy in self.game.enemys:
            if enemy != self:
                dist = self.pos - enemy.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        #self.rect.x -= self.speedy 
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.origin_image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_enemys()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * ENEMY_FRICTION
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt**2
        self.hitbox.centerx = self.pos.x
        collide_with_gameobject(self, self.game.walls, 'x')
        self.hitbox.centery = self.pos.y
        collide_with_gameobject(self, self.game.walls, 'y')
        self.rect.center = self.hitbox.center
        #bullet이랑 enemy가 충돌시 둘 다 kill
        if self.health <= 0:
            self.kill()

    def draw_health(self):
        col = YELLOW
        width = int(self.hitbox.width * self.health / ENEMY_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        self.outer_edge = pg.Rect(0, 0, self.hitbox.width, 7)
        if self.health < ENEMY_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)
            pg.draw.rect(self.image, WHITE, self.outer_edge, 1)

#아이템 상자 생성
class Feed(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.feeds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.rect.x = self.pos.x*TILESIZE
        self.rect.y = self.pos.y*TILESIZE
        # 추후 random을 통해 바꿔야함.
        self.item_no = random.choice(ITEM_KIND)

class Explode(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.explode
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size = (60,60)
        self.load_images()
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def load_images(self):
        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.image.fill(ORANGE)
        pass

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > EXPLOSION_LITETIME:
            self.kill()
        pass
    pass

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

class Ground(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.ground
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.ground_img
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.rect.x = self.pos.x*TILESIZE
        self.rect.y = self.pos.y*TILESIZE
