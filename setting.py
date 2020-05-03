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
#player properties
PLAYER_ACC = 0.45
PLAYER_FRICTION = -0.05
PLAYER_HIT_BOX = pg.Rect(0, 0, 35, 35)
PLAYER_HIT_BOX_OFFSET = vec(20,20)
PLAYER_HEALTH = 100

# Weapon setting
WEAPONS = {}
WEAPONS['pistol']       = {'bullet_speed': 350,
                           'bullet_lifetime': 700,
                           'rate': 1,
                           'damage': 10,
                           'spread': 4,
                           'bullet_size': (6,6),
                           'bullet_count': 1,
                           'barrel_offset': vec(38, -5),
                           'barrel_offset_fliped': vec(38, 5)}

WEAPONS['shotgun']      = {'bullet_speed': 300,
                           'bullet_lifetime': 350,
                           'rate': 1000,
                           'damage': 5,
                           'spread': 20,
                           'bullet_size': (3,3),
                           'bullet_count': 12,
                           'barrel_offset': vec(34, -4),
                           'barrel_offset_fliped': vec(34, 4)}

WEAPONS['sniper']       = {'bullet_speed': 500,
                           'bullet_lifetime': 1000,
                           'rate': 1500,
                           'damage': 13,
                           'spread': 0,
                           'bullet_size': (3,3),
                           'bullet_count': 1,
                           'barrel_offset': vec(48, 0),
                           'barrel_offset_fliped': vec(48, 0)}

WEAPONS['flamethrower'] = {'bullet_speed': 500,
                           'bullet_lifetime': 400,
                           'rate': 0,
                           'damage': 3,
                           'spread': 20,
                           'bullet_size': (3,3),
                           'bullet_count': 15,
                           'barrel_offset': vec(40, -4),
                           'barrel_offset_fliped': vec(40, 4)}

# grenade properties
GRENADE_SPEED = 600
GRENADE_LIFETIME = 3000
GRENADE_RATE = 1000
GRENADE_DAMAGE = 60

# explosion properties
EXPLOSION_LITETIME = 500
EXPLOSION_KNOCKBACK = 70

# enemy properties
ENEMY_HEALTH = 100
ENEMY_DAMAGE = 10
ENEMY_KNOCKBACK = 20
ENEMY_SPEED = [100, 150, 75, 125]
ENEMY_FRICTION = -1
ENEMY_HIT_BOX = pg.Rect(0, 0, 30, 30)
AVOID_RADIUS = 50

# item properties
SPEEDUP_RATE = 5000
ITEM_KIND = [0, 1, 2, 3, 4]
AMOR_HEALTH = 25

#image
TEST = "test.png"
GROUND_IMG = 'ground.png'
WEAPON_IMGS = []
WEAPON_IMGS.append(['glock.png','glock_hand.png'])#pistol image
WEAPON_IMGS.append(['shotgun.png','shotgun_hand.png'])#shotgun image
WEAPON_IMGS.append('sniper_2.png')#sniper image
WEAPON_IMGS.append('flamethrower.png')#flamethrower image
GRENADE_IMG = 'grenade.png'
GRENADE_THROW_IMG = 'grenade_throw.png'
PLAYER_IMG1 = 'move1.png'
PLAYER_IMG2 = 'move2.png'
START_SCREEN = 'main.jpg'

#FEED shake up and down 
FEED_RANGE = 20
FEED_SPEED = 0.6
#enemy and player distance
DETECT_RADIUS = 400
