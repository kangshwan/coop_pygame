import os
import random
import pygame as pg
import sys
from setting import *
from sprites import *
from tilemap import *
from os import path
import time 
from time import sleep

import time
import threading
#from moviepy.editor import VideoFileClip


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
        self.load_data()

    def run(self):
        #pg.mixer.music.play(loops = -1)   #bg play. loops == false -> play gain , Ture -> once

        self.playing = True
        #if self.playing is True, that means now playing game.
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
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

        self.enemys = pg.sprite.Group()

        #draw map in here
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, LIGHTBLUE)
                if tile == '2':
                    Wall(self, col, row, BROWN)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)
        

        #아이템or스킬상자가 랜덤한 위치에 드랍되게 / 상자를 먹으면 사라지고 일정 효과가 발동되도록 만들어주기
        #일정 주기마다 생성되도록 만들어주기 - 완료
        def item_box():
            for i in range(1):
                self.feeds = pg.sprite.Group()
                a = random.randint(10,30)
                b = random.randint(15,25)                   
                Feed(self, a,b)
            threading.Timer(3, item_box).start()
        item_box()

     

        for z in range(39,40): #한 블럭이 -1씩 이동  
            enemy(self,z,12)
        for z in range(39,40): #한 블럭이 -1씩 이동  
            enemy(self,z,10)
        for z in range(39,40): #한 블럭이 -1씩 이동  
            enemy(self,z,8)
    
        
        

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
        self.camera.update(self.player)

        self.second = ((pg.time.get_ticks() - self.start_tick)/1000)
        #hits -> used sprite collide method, (x, y, default boolean) collision check
        hits = pg.sprite.spritecollide(self.player, self.walls, False)

        hits = pg.sprite.pygame.sprite.spritecollide(self.player, self.walls, False)
        hit = pg.sprite.pygame.sprite.spritecollide(self.player, self.enemys, False)
        if hits:
            #do something
            pass
        if hit: #적이랑 부딪히면 게임 종료
            pg.quit()
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
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.display.update()

    def load_data(self):
        # load map to the game
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder,'map','map2.txt'))
        pass


g = Game()
while g.start:
    # Game start when g.start is True
    while g.running:
        # this g.running will take control of game over or not
        g.new()
pg.quit()
sys.exit()
