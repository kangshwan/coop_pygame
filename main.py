import random
import sys

from setting import *
from sprites import *
from tilemap import *
from hud import *
from os import path
from time import sleep
import random
import time
import threading

vec = pg.math.Vector2



class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        #pg.mixer.init() # for use of music
        #pg.mixer.init('')
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        # make a screen for the game / 게임을 하기위한 screen 생성(창 크기 설정)
        pg.display.set_caption(TITLE)
        # this is the tiltle of the game you'll see in the window / 창의 제목 결정
        self.clock = pg.time.Clock()
        self.running = True
        self.start = True

        self.load_data()
                #메뉴판 만들고
                #button -> game start 누르면 self.game_running()


    def run(self):
        #pg.mixer.music.play(loops = -1)   #bg play. loops == false -> play gain , Ture -> once

        self.playing = True
        #if self.playing is True, that means now playing game. / self.playing이 True면 게임을 진행하고있다는뜻 
        # -> 이후 사망시 continue?를 물을때 False로 바꿔주고 Yes일 경우 다시 True로, No일경우 self.running을 False로 바꾸어 주면 좋아보임.
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            #set the frame per second / FPS를 구하기 위함. 이후 dt는 총알구현에 있어서 중요하게 사용됨.
            self.events()
            if not self.paused:
            #if self.paused == 0:
                self.update()
            #events for keyboard and mouse input / 이벤트를 처리하기 위함. 항상 pygame은 event 이벤트발생(사용자의 입력) -> update(입력에 따른 변화를 업데이트해줌) -> draw 이후 그림을 그림
            
            self.draw()

    def new(self):
        #when start a new game
        self.score = 0
        self.phase = 0
        #이후 1페이즈, 2페이즈 등 결정할때 사용
        self.zombie_remain = 1000 
        self.enemy_spawned = 0
        self.item_spawned = 0
        #sprite gruop
        self.all_sprites = pg.sprite.Group()
        self.zombies     = pg.sprite.Group()
        self.bullets     = pg.sprite.Group()
        self.grenades    = pg.sprite.Group()
        self.obstacle    = pg.sprite.Group()
        self.walls       = pg.sprite.Group()
        self.enemys      = pg.sprite.Group()
        self.feeds       = pg.sprite.Group()
        self.explode     = pg.sprite.Group()
        self.ground      = pg.sprite.Group()
        self.trace       = pg.sprite.Group()
        self.feed_pos = []
        self.enemy_pos = []
        self.paused = False 
        
        #for row, tiles in enumerate(self.map.data):
        #    #enumerate는 한 배열에 대하여 index와 그 값을 동시에 가져올수 있음. -> 자세한건 구글링
        #    block = ''
        #    check = False
        #    passed = 0
        #    for col, tile in enumerate(tiles):
        #        if tile == '[':
        #            check = True
        #            passed +=1
        #            continue
        #        if tile == ']':
        #            check = False
        #        if check:
        #            block += tile
        #            passed+=1
        #            continue
        #        col -= passed
        #        if tile == 's':
        #            print('passed')
        #            Ground(self, col, row, self.stone_floor_img)
        #        else:
        #            Ground(self, col, row, self.ground_img)
        #        
        #        if tile == '1':
        #            Wall(self, col, row, LIGHTBLUE, None)
        #        if tile == '2':
        #            Wall(self, col, row, BROWN, None)
        #            print(col,row)
        #        
        #
        #        if block != '':
        #            if block[1] == 's':
        #                Ground(self, col, row, self.stone_floor_img)
        #            if block == 'wpl':
        #                Wall(self, col, row, None, self.wood_pillar_img[0])
        #            if block == 'wpm':
        #                Wall(self, col, row, None, self.wood_pillar_img[1])
        #            if block == 'wpr':
        #                Wall(self, col, row, None, self.wood_pillar_img[2])
        #            if block == 'wpt':
        #                Wall(self, col, row, None, self.wood_pillar_img[3])
        #            
        #            block = ''
        #draw map in here / 여기서부터 맵을 그림.
        #for row, tiles in enumerate(self.map.data):
        #    #enumerate는 한 배열에 대하여 index와 그 값을 동시에 가져올수 있음. -> 자세한건 구글링
        #    for col, tile in enumerate(tiles):
        #        if tile == 'P':
        #            self.player = Player(self, col, row)
        #        if tile == 'I':
        #            self.feed_pos.append([(col,row),False])
        #
        #for row, tiles in enumerate(self.map.data):
        #    #enumerate는 한 배열에 대하여 index와 그 값을 동시에 가져올수 있음. -> 자세한건 구글링
        #    for col, tile in enumerate(tiles):
        #        if tile == 'E':
        #            self.enemy_pos.append((col,row))
        #            Enemy(self, col, row)        
        #enemy_pos에 col,row 저장. 추후 feed처럼 append하여 생성하면 좋아보임.
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'enemy_spawn':
                self.enemy_pos.append((tile_object.x, tile_object.y))
                Enemy(self, tile_object.x, tile_object.y)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        # make Camera class / 카메라 객체 생성
        
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

        self.start_tick = pg.time.get_ticks()

        self.run()

    def update(self):
        self.now = pg.time.get_ticks()
        # game loop update
        self.all_sprites.update()
        self.camera.update(self.player)
        if self.now - self.item_spawned > 3000:    
            #test = random.randint(0,len(self.feed_pos)-1)
            #if self.feed_pos[test][1] == True:
            #    Feed(self, self.feed_pos[test][0][0],self.feed_pos[test][0][1])
            try:
                chosen_item = random.choice(self.feed_pos)
            except IndexError:
                chosen_item = [[0,0],True]
            if chosen_item[1] == False:
                Feed(self, chosen_item[0][0], chosen_item[0][1])
                chosen_item[1] = True

            self.item_spawned = self.now
        #update에서 Enemy 생성
        if self.now - self.enemy_spawned > 10000:
            for e_position in self.enemy_pos:
                #3초마다 해당 장소에서 생성. 추후 enemy_pos를 list로 쓸경우 for문 안에넣고 index들로 접근해서 생성하면 될듯.
                Enemy(self, e_position[0], e_position[1])
                self.enemy_spawned = self.now
        self.second = ((pg.time.get_ticks() - self.start_tick)/1000)

        #hits -> used sprite collide method, (x, y, default boolean) collision check
        hits = pg.sprite.pygame.sprite.spritecollide(self.player, self.enemys, False, collide_hit_box)
        for hit in hits:
            if self.player.amor != 0:
                self.player.amor -= ENEMY_DAMAGE
                if self.player.amor < 0:
                    self.player.health += self.player.amor
            else:
                self.player.health -= ENEMY_DAMAGE
            hit.vel = vec(0, 0)
            hit.acc = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(ENEMY_KNOCKBACK, 0).rotate(-hits[0].rot)

        # player collide with the feed
        hits = pg.sprite.pygame.sprite.spritecollide(self.player, self.feeds, True, collide_hit_rect)
        for hit in hits:
            if hit.item_no == 0:
                self.player.max_speed = 10
                self.player.last_speed = pg.time.get_ticks()
                self.player.gun_status[1] = [True, 240]
                self.player.gun_status[2] = [True, 10]
                self.player.gun_status[3] = [True, 500]

            if hit.item_no == 1:
                self.player.weapon_rate *= 0.001
                self.player.last_weapon_speed = pg.time.get_ticks()

            if hit.item_no == 2:
                self.player.weapon_damage *= 2.0
                self.player.last_weapon_damage = pg.time.get_ticks()

            if hit.item_no == 3:
                self.player.health += 50
                if self.player.health > PLAYER_HEALTH :
                    self.player.health = PLAYER_HEALTH
            
            if hit.item_no == 4:
                self.player.gun_status[1] = [True, 12]
                self.player.gun_status[2] = [True, 1]
                self.player.gun_status[3] = [True, 1000]
                self.player.amor = AMOR_HEALTH # 체력이 아니라 armor (일정 시간이 지나면 사라짐) / 초록색이 아니라 체력과 따로 흰색으로 표시되도록
                self.player.max_health = PLAYER_HEALTH + AMOR_HEALTH
                self.player.max_health = self.player.health + self.player.amor
                if self.player.max_health < PLAYER_HEALTH:
                    self.player.max_health = PLAYER_HEALTH

        # bullet hit the mob
        if self.player.gun_select in [2,3]:
            hits = pg.sprite.groupcollide(self.enemys, self.bullets, False, False, collide_hit_box)
            for hit in hits:
                hit.health -= self.player.weapon_damage
                hit.vel = vec(0, 0)
        else:
            hits = pg.sprite.groupcollide(self.enemys, self.bullets, False, True)
            for hit in hits:
                hit.health -= self.player.weapon_damage * len(hits[hit])
                hit.vel = vec(0, 0)

        # explosion hit the player
        hits = pg.sprite.pygame.sprite.spritecollide(self.player, self.explode, False, collide_hit_box)
        for hit in hits:
            if self.player.amor > 0:
                self.player.amor -= GRENADE_DAMAGE
                if self.player.amor < 0:
                    self.player.health += self.player.amor
            else:
                self.player.health -= GRENADE_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
            rot = (self.player.pos - hit.pos).angle_to(vec(1,0))
            self.player.pos += vec(EXPLOSION_KNOCKBACK, 0).rotate(-rot)
        
        # explosion hit the mob
        hits = pg.sprite.groupcollide(self.enemys, self.explode, False, False)
        for hit in hits:
            hit.health -= GRENADE_DAMAGE
            hit.vel = vec(0, 0)
            hit.pos += vec(EXPLOSION_KNOCKBACK, 0).rotate(-hit.rot)
        if self.playing == False:
            self.runnig = False

    def events(self):
        # game loop events
        key_1 = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False
                    self.start = False
                self.start = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pass
            if key_1[pg.K_p]:
                self.paused = not self.paused
                self.player.standing = True
            if key_1[pg.K_PERIOD]:
                self.draw_debug = not self.draw_debug
            
    #def draw_grid(self):
    #    for x in range(0, WIDTH, TILESIZE):
    #        pg.draw.line(self.screen, LIGHTGREY, (x,0), (x, HEIGHT))
    #        for y in range(0, HEIGHT, TILESIZE):
    #            pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH,y))

    def draw(self):
        # game loop - draw
        #self.screen.fill(DARKGREY)
        #self.draw_grid()
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.draw_health()
                sprite.draw_body()
            if self.draw_debug:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.rect),1)

                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hitbox),1)

            if isinstance(sprite, Player):
                sprite.draw_body()
                #self.screen.blit(sprite.image, self.camera.apply(sprite))
                if self.draw_debug:
                    pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hitbox),1)
                    pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.rect),1)
            else:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                for wall in self.walls:
                    pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect),1)


        #pg.draw.rect(self.screen, WHITE, self.player.hitbox,2)
        
        # HUD functions
        draw_player_health(self.screen, 10, HEIGHT - 40, self.player.health, self.player.amor ,self.player.max_health)
        draw_gun_list(self.screen, self.player.gun_status, self.player.gun_select)
        draw_grenade_list(self.screen, self.player.grenade[1])
        draw_money(self.screen, 10, 10, self.player.money,self.poke_font)
        pg.display.update()
        
    def load_data(self):
        # load map to the game
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'Image')
        map_folder = path.join(game_folder,'map')
        player_folder = path.join(img_folder,'player')
        weapon_folder = path.join(img_folder, 'weapon')
        enemy_folder = path.join(img_folder,'enemy')
        vfx_folder = path.join(img_folder, 'special_effect')
        font_folder = path.join(game_folder, 'Font')
        self.bullet_img = []
        self.explode_img = []
        self.zombie1_img = []
        self.wood_pillar_img = []
        self.map = TiledMap(path.join(map_folder,'map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        #self.ground_img = pg.image.load(path.join(map_folder, GROUND_IMG[0])).convert_alpha()
        #self.stone_floor_img = pg.image.load(path.join(map_folder, GROUND_IMG[1])).convert_alpha()
        self.grenade_img = pg.image.load(path.join(weapon_folder, GRENADE_THROW_IMG)).convert_alpha()
        self.pistol_img = pg.image.load(path.join(weapon_folder, WEAPON_IMGS[0][1])).convert_alpha()
        self.shotgun_img = pg.transform.scale(pg.image.load(path.join(weapon_folder, WEAPON_IMGS[1][1])).convert_alpha(), (62,16))
        self.sniper_img = pg.transform.scale(pg.image.load(path.join(weapon_folder, WEAPON_IMGS[2][1])).convert_alpha(),(85,30))
        self.flamethrower_img = pg.transform.scale(pg.image.load(path.join(weapon_folder, WEAPON_IMGS[3][1])).convert_alpha(),(70,18))
        self.move1_img = pg.image.load(path.join(player_folder, PLAYER_IMG1)).convert_alpha()
        self.move2_img = pg.image.load(path.join(player_folder, PLAYER_IMG2)).convert_alpha()
        #for i in range(4):
        #    self.wood_pillar_img.append(pg.image.load(path.join(map_folder, WOOD_PILAR_IMG[i])).convert_alpha())
        for i in range(4):
            self.bullet_img.append(pg.image.load(path.join(weapon_folder, BULLET_IMGS[i])).convert_alpha())
        for i in range(7):
            self.explode_img.append(pg.image.load(path.join(vfx_folder, EXPLODE_IMG[i])).convert_alpha())
        for i in range(7):
            self.zombie1_img.append(pg.transform.scale(pg.image.load(path.join(enemy_folder, ZOMBIE1_IMG[i])).convert_alpha(), (35,56)))
        pass
        self.poke_font = path.join(font_folder, 'PokemonGb-RAeo.ttf')

g = Game()
while g.start:
    # Game start when g.start is True
    g.running = True
    while g.running:
        # this g.running will take control of game over or not
        g.new()
    if g.running == False:
        pg.quit()
    pg.quit()