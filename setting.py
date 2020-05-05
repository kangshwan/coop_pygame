import pygame as pg
vec = pg.math.Vector2

# this file is basic settings of game
TITLE = "Zombie Survival"
WIDTH = 960
HEIGHT = 640

FPS = 60
WINDOW_SIZE = [WIDTH,HEIGHT]


TILESIZE = 32
GRIDWIDTH = WIDTH/TILESIZE
# width 40 block
GRIDHEIGHT = HEIGHT/TILESIZE
# height 30 block

#define colors
BLACK     = (  0,  0,  0)
WHITE     = (255,255,255)
RED       = (255,  0,  0)
BROWN     = (150, 75,  0)
LIGHTBLUE = ( 75,137,220)
LIGHTGREY = (100,100,100)
DARKGREY  = ( 40, 40, 40)
GREEN     = (  0,255,  0)
GRENADE   = ( 11, 64,  8)
YELLOW    = (255,255,  0)
ORANGE    = (255,127,  0)
SILVER    = (192,192,192)
GOLD      = (178,151,  0)
CYAN      = (  0,255,255)

#player properties
PLAYER_ACC = 0.45
PLAYER_FRICTION = -0.05
PLAYER_HIT_BOX = pg.Rect(0, 0, 32, 32)
PLAYER_HIT_BOX_OFFSET = vec(20,20)
PLAYER_HEALTH = 100

# Weapon setting
WEAPONS = {}
WEAPONS['pistol']       = {'bullet_speed': 350,
                           'bullet_lifetime': 700,
                           'rate': 500,
                           'damage': 10,
                           'spread': 2,
                           'size': (6,6),
                           'bullet_count': 1,
                           'barrel_offset': vec(38, -5),
                           'barrel_offset_fliped': vec(38, 5)}

WEAPONS['shotgun']      = {'bullet_speed': 300,
                           'bullet_lifetime': 350,
                           'rate': 1000,
                           'damage': 5,
                           'spread': 20,
                           'size': (3,3),
                           'bullet_count': 12,
                           'barrel_offset': vec(34, -3),
                           'barrel_offset_fliped': vec(34, 3)}

WEAPONS['sniper']       = {'bullet_speed': 800,
                           'bullet_lifetime': 700,
                           'rate': 1500,
                           'damage': 13,
                           'spread': 0,
                           'size': (5,3),
                           'bullet_count': 1,
                           'barrel_offset': vec(45, -10),
                           'barrel_offset_fliped': vec(45, 10)}

WEAPONS['flamethrower'] = {'bullet_speed': 100,
                           'bullet_lifetime': 1500,
                           'rate': 0,
                           'damage': 0.1,
                           'spread': 20,
                           'size': (5,5),
                           'bullet_count': 10,
                           'barrel_offset': vec(40, -4),
                           'barrel_offset_fliped': vec(40, 4)}

WEAPON_PRICE = [0, 100, 200, 300]
# grenade properties
GRENADE_SPEED = 800
GRENADE_LIFETIME = 1500
GRENADE_RATE = 2000
GRENADE_DAMAGE = 50

# explosion properties
EXPLOSION_LIFETIME = 500
EXPLOSION_KNOCKBACK = 70

# enemy properties
ENEMY_HEALTH = 100
ENEMY_DAMAGE = 10
ENEMY_KNOCKBACK = 20
ENEMY_SPEED = [30, 30, 30, 30,30, 50, 50, 50, 70,70]
ENEMY_FRICTION = -1
ENEMY_HIT_BOX = pg.Rect(0, 0, 32, 60)
AVOID_RADIUS = 50
ENEMY_SPAWN_TIME = 20000

BOSS_HITBOX = pg.Rect(0, 0, TILESIZE*2,TILESIZE*2)
BOSS_HEALTH = 10000
BOSS_HIT_DAMAGE = 20
BOSS_SPEED = 120
BOSS_ATTACK_RATE = 3000
BOSS_ATTACK_SPEED = 100
BOSS_BULLET_DAMAGE = 30
BOSS_KNOCKBACK = 30

# item properties
SPEEDUP_RATE = 7000
ITEM_KIND = [0,1,2,3,4]#, 1, 1,  2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5]  
AMOR_HEALTH = 25
FEED_RANGE = 10
FEED_SPEED = 0.2
ITEM_SPAWN_TIME = 20000

#image
TEST = "test.png"
GROUND_IMG = ['ground.png', 'stone_floor.png']
WALL_IMG = 'wooden_pillar_front_left.png'
WOOD_PILAR_IMG = ['wooden_pillar_front_left.png', 'wooden_pillar_front_mid.png', 'wooden_pillar_front_right.png', 'wooden_pillar_top.png']

WEAPON_IMGS = []
BULLET_IMGS = []

WEAPON_IMGS.append(['glock.png','glock_hand.png'])#pistol image
WEAPON_IMGS.append(['shotgun.png','shotgun_hand.png'])#shotgun image
WEAPON_IMGS.append(['sniper_rifle.png', 'sniper_test.png'])#sniper image
WEAPON_IMGS.append(['flamethrower.png', 'flamethrower_hand.png'])#flamethrower image

BULLET_IMGS.append('pistol_bullet.png')
BULLET_IMGS.append('shotgun_bullet.png')
BULLET_IMGS.append('sniper_rifle_bullet.png')
BULLET_IMGS.append('tiny_flame.png')

GRENADE_IMG = 'grenade.png'
GRENADE_THROW_IMG = 'grenade_throw.png'

EXPLODE_IMG = ['explosion1_1.png', 'explosion1_2.png', 'explosion1_3.png','explosion1_4.png','explosion1_5.png','explosion1_6.png','explosion1_7.png']

PLAYER_IMG1 = 'move1.png'
PLAYER_IMG2 = 'move2.png'
START_SCREEN = 'main.png'
END_SCREEN = 'ending.png'

ZOMBIE1_IMG = ['zombie1_1.png', 'zombie1_2.png', 'zombie1_3.png', 'zombie1_4.png', 'zombie1_5.png', 'zombie1_6.png', 'zombie1_7.png']
BOSS_IMG = ['boss_1.png','boss_2.png','boss_3.png','boss_4.png','boss_5.png','boss_6.png']
ITEM_IMG = 'item_box.png'
#FEED shake up and down 


#enemy and player distance
DETECT_RADIUS = 400

ITEM_POPUP = 10000
ITEM_EFFECT = {0: 'SPEED UP!', 1:'PLUS GRENADE!', 2:'DMG UP!', 3:'HEAL UP!', 4:'AMOR READY.',5:''}
MAX_ENEMY = 10