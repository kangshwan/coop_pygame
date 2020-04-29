import os
import random
import pygame as pg
from setting import *
from sprites import *
import time 
from time import sleep
from moviepy.editor import VideoFileClip


vec = pg.math.Vector2

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        #pg.mixer.init() # for use of music
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.screen.fill(BLACK)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.start = True

    def run(self):
        #pg.mixer.music.play(loops = -1)   #bg play. loops == false -> play gain , Ture -> once

        self.playing = True
        #if self.playing is True, that means now playing game.
        while self.playing:
            self.clock.tick(FPS)
            #set the frame per second
            self.events()
            #events for keyboard and mouse input
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def new(self):
        #when start a new game
        self.score = 0
        self.money = 5000
        self.phase = 0
        self.speed_x = 4
        self.speed_y = 4
        self.speed_x_min = -2
        self.speed_y_min = -2
        self.zombie_remain = 1000
        #sprite gruop
        self.all_sprites = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.obstarcle = pg.sprite.Group()
        self.walls = pg.sprite.Group()#just for test
        self.player = Player(self)
        self.leg = Leg(self)
        
     
        #self.player make Player Object
        self.start_tick = pg.time.get_ticks()
        """
            with open(os.path.join(self.dir, SCORE), 'r') as f:
                try:
                    self.highscore = int(f.read())
                except:
                    self.highscore = 0
        """
        self.run()

    def update(self):
        # game loop update
        self.all_sprites.update()
        self.second = ((pg.time.get_ticks() - self.start_tick)/1000)
        #hits -> used sprite collide method, (x, y, default boolean) collision check
        hits = pg.sprite.pygame.sprite.spritecollide(self.player, self.walls, False)
        if hits:
            #do something
            pass
        if self.score == 1000:
            self.level_up.play()
            self.levelup_text()
            sleep(0.4)
            self.enemy_level += 1
            self.levelup(self.phase)
        #게임 클리어 조건
        if self.zombie_remain < 0:
            self.clear_text()
            self.ending = True
            self.playing = False
            sleep(1)

    def events(self):
        # game loop events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False
                    self.start = False
                self.start = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pass
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x,0), (x, HEIGHT))
            for y in range(0, HEIGHT, TILESIZE):
                pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH,y))
                
    def draw(self):
        # game loop - draw
        self.screen.fill(DARKGREY)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.update()


g = Game()
while g.start:
    while g.running:
        g.new()
pg.quit()
