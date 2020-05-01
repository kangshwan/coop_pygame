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
from numpy import random
import time
import threading


vec = pg.math.Vector2

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        #pg.mixer.init() # for use of music
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        # make a screen for the game / 게임을 하기위한 screen 생성(창 크기 설정)
        pg.display.set_caption(TITLE)
        # this is the tiltle of the game you'll see in the window / 창의 제목 결정
        self.clock = pg.time.Clock()
        self.running = True
        self.start = True
        self.load_data()

    def run(self):
        #pg.mixer.music.play(loops = -1)   #bg play. loops == false -> play gain , Ture -> once

        self.playing = True
        #if self.playing is True, that means now playing game. / self.playing이 True면 게임을 진행하고있다는뜻 
        # -> 이후 사망시 continue?를 물을때 False로 바꿔주고 Yes일 경우 다시 True로, No일경우 self.running을 False로 바꾸어 주면 좋아보임.
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            #set the frame per second / FPS를 구하기 위함. 이후 dt는 총알구현에 있어서 중요하게 사용됨.
            self.events()
            #events for keyboard and mouse input / 이벤트를 처리하기 위함. 항상 pygame은 event 이벤트발생(사용자의 입력) -> update(입력에 따른 변화를 업데이트해줌) -> draw 이후 그림을 그림
            self.update()
            self.draw()

    def new(self):
        #when start a new game
        self.score = 0
        self.money = 5000
        #이후 player sprite로 들어갈 가능성 있음.
        self.phase = 0
        #이후 1페이즈, 2페이즈 등 결정할때 사용
        self.zombie_remain = 1000 
        #sprite gruop
        self.all_sprites = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.obstacle = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemys = pg.sprite.Group()
        self.feeds = pg.sprite.Group()
        self.feed_pos = []
        #draw map in here / 여기서부터 맵을 그림.
        for row, tiles in enumerate(self.map.data):
            #enumerate는 한 배열에 대하여 index와 그 값을 동시에 가져올수 있음. -> 자세한건 구글링
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, LIGHTBLUE)
                if tile == '2':
                    Wall(self, col, row, BROWN)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'I':
                    self.feed_pos.append((col,row))
        self.camera = Camera(self.map.width, self.map.height)
        # make Camera class / 카메라 객체 생성
        
        test = random.randint(0,len(self.feed_pos)-1)
        Feed(self, self.feed_pos[test][0],self.feed_pos[test][1])


        #아이템or스킬상자가 랜덤한 위치에 드랍되게 / 상자를 먹으면 사라지고 일정 효과가 발동되도록 만들어주기
        #일정 주기마다 생성되도록 만들어주기 - 완료
        #def item_box():
        #    for i in range(1):
        #        self.feeds = pg.sprite.Group()
        #        a = random.randint(10,30)
        #        b = random.randint(15,25)                   
        #        Feed(self, a,b)
        #        
        #    threading.Timer(3, item_box).start()
        #item_box()

     

        for z in range(6,16): #한 블럭이 -1씩 이동  
            enemy(self,z,12)	            
    
        self.start_tick = pg.time.get_ticks()

        self.run()

    def update(self):
        # game loop update
        self.all_sprites.update()
        self.camera.update(self.player)

        self.second = ((pg.time.get_ticks() - self.start_tick)/1000)
        #hits -> used sprite collide method, (x, y, default boolean) collision check
        hit = pg.sprite.pygame.sprite.spritecollide(self.player, self.enemys, False)

        if hit: #적이랑 부딪히면 게임 종료
            pg.quit()


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
        pg.draw.rect(self.screen, WHITE, self.player.hitbox,2)
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
