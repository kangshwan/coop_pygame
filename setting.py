import pygame as pg
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


#player properties
PLAYER_ACC = 0.45
PLAYER_FRICTION = -0.05
PLAYER_HIT_BOX = pg.Rect(0, 0, 35, 35)
PLAYER_HEALTH = 100

# gun properties
BULLET_SPEED = 500
BULLET_LIFETIME = 700
BULLET_RATE = 300
BULLET_DAMAGE = 5

PISTOL_SPEED = 500
PISTOL_LIFETIME = 700
PISTOL_RATE = 250

# item properties
SPEEDUP_RATE = 5000

#image
TEST = "test.png"
#image
MUSIC = 'MUSIC.MP3'
