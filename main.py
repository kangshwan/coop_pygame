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
        pg.mixer.init() # for use of music
        pg.mixer.music.load('Sound/sound1.mp3')
        pg.mixer.music.play(-1)
    
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        # make a screen for the game / 게임을 하기위한 screen 생성(창 크기 설정)
        pg.display.set_caption(TITLE)
        # this is the tiltle of the game you'll see in the window / 창의 제목 결정
        self.clock = pg.time.Clock()
        self.running = False
        self.screen_running = False
        self.start = True
        self.ending = False
        #self.selecting = True
        self.load_data()

                #메뉴판 만들고
                #button -> game start 누르면 self.game_running()

    def run(self):
        #pg.mixer.music.play(loops = -1)   #bg play. loops == false -> play gain , Ture -> once
        
        #if self.playing is True, that means now playing game. / self.playing이 True면 게임을 진행하고있다는뜻 
        # -> 이후 사망시 continue?를 물을때 False로 바꿔주고 Yes일 경우 다시 True로, No일경우 self.running을 False로 바꾸어 주면 좋아보임.
        self.playing = True
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
        self.ending = False

        #sprite gruop
        self.all_sprites  = pg.sprite.Group()
        self.zombies      = pg.sprite.Group()
        self.bullets      = pg.sprite.Group()
        self.grenades     = pg.sprite.Group()
        self.obstacle     = pg.sprite.Group()
        self.walls        = pg.sprite.Group()
        self.enemys       = pg.sprite.Group()
        self.feeds        = pg.sprite.Group()
        self.explode      = pg.sprite.Group()
        self.ground       = pg.sprite.Group()
        self.boss_bullet = pg.sprite.Group()
        
        self.spawned_enemy = 0
        
        self.feed_pos = []
        self.enemy_pos = []
        self.paused = False
        self.boss_pos = ()
        self.boss_spawn = True
        self.paused_text = False

        self.item_time = 0
        self.item_no = 5
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
        #            
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
            if tile_object.name == 'enemy_spawn':
                self.enemy_pos.append((tile_object.x, tile_object.y))
                if EXPLAIN_GUN:
                    Enemy(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'boss':
                self.boss_pos = (tile_object.x, tile_object.y)
            if tile_object.name == 'item':
                self.feed_pos.append([(tile_object.x,tile_object.y),False])
                if EXPLAIN_ITEM:
                    Feed(self, tile_object.x, tile_object.y)

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
        if not EXPLAIN_ITEM:
            if self.now - self.item_spawned > ITEM_SPAWN_TIME:    
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
        if not EXPLAIN_GUN:
            if self.now - self.enemy_spawned > ENEMY_SPAWN_TIME:
                if self.boss_spawn:
                    for e_position in self.enemy_pos:
                        #3초마다 해당 장소에서 생성. 추후 enemy_pos를 list로 쓸경우 for문 안에넣고 index들로 접근해서 생성하면 될듯.
                        if self.spawned_enemy < MAX_ENEMY:
                            Enemy(self, e_position[0], e_position[1])
                            self.enemy_spawned = self.now
                            self.spawned_enemy += 1
        self.second = ((pg.time.get_ticks() - self.start_tick)/1000)

        #update에서 Boss 생성
        if self.player.kill_enemy > MAX_ENEMY:
            if self.boss_spawn:
                #3초마다 해당 장소에서 생성. 추후 enemy_pos를 list로 쓸경우 for문 안에넣고 index들로 접근해서 생성하면 될듯.
                self.boss = Boss(self, self.boss_pos[0], self.boss_pos[1])
                self.boss_spawn = not self.boss_spawn
       
        hits = pg.sprite.pygame.sprite.spritecollide(self.player, self.boss_bullet, True, collide_hit_box)
        for hit in hits:
            if self.player.amor != 0:
                self.player.amor -= BOSS_BULLET_DAMAGE
                if self.player.amor < 0:
                    self.player.health += self.player.amor
            else:
                self.player.health -= BOSS_BULLET_DAMAGE
            hit.vel = vec(0, 0)
            hit.acc = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            if self.boss.target_dist.y > 0:
                self.player.pos += vec(0, BOSS_KNOCKBACK)
            else:
                self.player.pos += vec(0, -BOSS_KNOCKBACK)       

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
            self.player.vel = vec(0,0)

        # player collide with the feed
        hits = pg.sprite.pygame.sprite.spritecollide(self.player, self.feeds, True, collide_hit_rect)
        
        for hit in hits:
            self.item_no = hit.item_no
            for position in self.feed_pos:
                if (hit.pos.x,hit.pos.y) == position[0]:
                    position[1] = False
            if hit.item_no == 0:
                #move speed up
                self.player.max_speed = 10
                self.player.last_speed = pg.time.get_ticks()
                #self.player.gun_status[2] = [True, 10]
            if hit.item_no == 1:
                #bullet speed up
                if self.player.grenade[0] == True:
                    self.player.grenade[1] += 3
                else:
                    self.player.grenade[0] = True
                    self.player.grenade[1] = 3

            if hit.item_no == 2:
                #damage up
                self.player.weapon_damage *= 2.0
                self.player.grenade_damage *= 2.0
                self.player.last_weapon_damage = pg.time.get_ticks()

            if hit.item_no == 3:
                #heal
                
                if self.player.health + 50 > PLAYER_HEALTH :
                    
                    self.player.health = PLAYER_HEALTH
                    self.player.max_health = self.player.health + self.player.amor
                else:
                    self.player.health += 50
            
            if hit.item_no == 4:
                #get amor
                self.player.amor = AMOR_HEALTH # 체력이 아니라 armor (일정 시간이 지나면 사라짐) / 초록색이 아니라 체력과 따로 흰색으로 표시되도록
                self.player.max_health = PLAYER_HEALTH + AMOR_HEALTH
                self.player.max_health = self.player.health + self.player.amor
                if self.player.max_health < PLAYER_HEALTH:
                    self.player.max_health = PLAYER_HEALTH
            self.item_time = self.now
                
        # bullet hit the mob
        if self.player.gun_select in [2,3]:
            hits = pg.sprite.groupcollide(self.enemys, self.bullets, False, False, collide_hit_box)
            for hit in hits:
                hit.health -= self.player.weapon_damage
                hit.vel = vec(0, 0)
        else:
            hits = pg.sprite.groupcollide(self.enemys, self.bullets, False, True, collide_hit_box)
            for hit in hits:
                hit.health -= self.player.weapon_damage * len(hits[hit])
                hit.vel = vec(0, 0)

        if not self.boss_spawn:
            hits = pg.sprite.pygame.sprite.collide_rect(self.player, self.boss)
            if hits:
                if self.player.amor > 0:
                    self.player.amor -= BOSS_HIT_DAMAGE
                    if self.player.amor < 0:
                        self.player.health += self.player.amor
                else:
                    self.player.health -= BOSS_HIT_DAMAGE
                #self.boss.vel = vec(0, 0)

                if self.player.health <= 0:
                    self.playing = False
                    self.running = False
                    self.player.key = 0
                rot = (self.player.pos - self.boss.pos).angle_to(vec(1,0))
                self.player.pos += vec(EXPLOSION_KNOCKBACK, 0).rotate(-rot)

            if self.player.gun_select in [2,3]:
                hits = pg.sprite.pygame.sprite.spritecollide(self.boss, self.bullets, False, collide_hit_box)
                for hit in hits:
                    self.boss.health -= self.player.weapon_damage
                    #self.boss.vel = vec(0, 0)
            else:
                hits = pg.sprite.pygame.sprite.spritecollide(self.boss, self.bullets, True, collide_hit_box)
                for hit in hits:
                    self.boss.health -= self.player.weapon_damage * len(hits)
                    #self.boss.vel = vec(0, 0)
            #boss collide with explode
            hits = pg.sprite.pygame.sprite.spritecollide(self.boss, self.explode, False, collide_hit_box)
            for hit in hits:
                self.boss.health -= GRENADE_DAMAGE
                hit.vel = vec(0, 0)
                rot = (self.player.pos - hit.pos).angle_to(vec(1,0))
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
                self.running = False
                self.player.key = 0
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
        
            
        if self.ending == True:
            self.clear_text()
            self.ending = True
            self.playing = False
                
    def clear_text(self):
        for i in range(8):
            self.draw_text('CLEAR !! ', 30, GREEN, WIDTH/2, HEIGHT/2-100)
            pg.display.update()
            sleep(0.1)
            self.draw_text('CLEAR !! ', 30, RED, WIDTH/2, HEIGHT/2-100)
            pg.display.update()
            sleep(0.1)

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
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.paused = not self.paused
                    self.player.standing = True
                    self.paused_text = not self.paused_text
                if event.key == pg.K_PERIOD:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_2 and pg.key.get_mods() & pg.KMOD_CTRL:
                    if self.player.money >= WEAPON_PRICE[1]:
                        self.player.money -= WEAPON_PRICE[1]
                        if self.player.gun_status[1][0] != True:
                            self.player.gun_status[1][0] = not self.player.gun_status[1][0]
                            self.player.gun_status[1][1] = 120
                        else:
                            self.player.gun_status[1][1] += 120
                if event.key == pg.K_3 and pg.key.get_mods() & pg.KMOD_CTRL:
                    if self.player.money >= WEAPON_PRICE[2]:
                        self.player.money -= WEAPON_PRICE[2]
                        if self.player.gun_status[2][0] != True:
                            self.player.gun_status[2][0] = not self.player.gun_status[2][0]
                            self.player.gun_status[2][1] = 10
                        else:
                            self.player.gun_status[2][1] = 10
                if event.key == pg.K_4 and pg.key.get_mods() & pg.KMOD_CTRL:
                    if self.player.money >= WEAPON_PRICE[3]:  
                        self.player.money -= WEAPON_PRICE[3]
                        if self.player.gun_status[3][0] != True:
                            self.player.gun_status[3][0] = not self.player.gun_status[3][0]
                            self.player.gun_status[3][1] = 1000
                        else:
                            self.player.gun_status[3][1] = 1000   
            if event.type == pg.MOUSEBUTTONDOWN:
                #screen button 기믹
                pass
                

            
    def draw(self):
        # game loop - draw
        #self.screen.fill(DARKGREY)
        #self.draw_grid()
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Boss):
                sprite.draw_body()
            if isinstance(sprite, Enemy):
                sprite.draw_health()
                sprite.draw_body()
                if self.draw_debug:
                    pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hitbox),1)
                    pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.rect),1)            


            if isinstance(sprite, Player):
                sprite.draw_body()
                #self.screen.blit(sprite.image, self.camera.apply(sprite))
                if self.draw_debug:
                    pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hitbox),1)
                    pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.rect),1)            
            else:
               #else 지울까 말까 지울까 말까
                self.screen.blit(sprite.image, self.camera.apply(sprite))
         
            if self.draw_debug:
                for wall in self.walls:
                    pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect),1)
            if self.paused_text:
                self.draw_text("PAUSE", 70, BLACK, WIDTH - 466, HEIGHT - 356)
                self.draw_text("PAUSE", 70, RED, WIDTH - 470, HEIGHT - 360)
                       
                       

        #pg.draw.rect(self.screen, WHITE, self.player.hitbox,2)
        if self.now - self.item_time < ITEM_POPUP:
            self.draw_text(ITEM_EFFECT[self.item_no],30, WHITE, WIDTH/2, HEIGHT/2-HEIGHT/4)
        # HUD functions
        draw_player_health(self.screen, 10, HEIGHT - 40, self.player.health, self.player.amor ,self.player.max_health)
        draw_gun_list(self.screen, self.player.gun_status, self.player.gun_select)
        draw_grenade_list(self.screen, self.player.grenade[1])
        draw_bullet_ratio(self.screen, WIDTH-40, (HEIGHT/4)+(HEIGHT/7),self.player.gun_select,self.player.gun_status[self.player.gun_select][1])
        draw_money(self.screen, 10, 10, self.player.money,self.poke_font)
        if not self.boss_spawn:
            draw_boss_health(self.screen, WIDTH/2-(TILESIZE*2), 2, self.boss.health)
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
        self.boss_img = []
        self.boss_bullet_img = []
        #self.wood_pillar_img = []
        self.map = TiledMap(path.join(map_folder,'map.tmx'))
        if EXPLAIN_GUN:
            self.map = TiledMap(path.join(map_folder,'explain_gun.tmx'))
        if EXPLAIN_ITEM:
            self.map = TiledMap(path.join(map_folder,'explain_item.tmx'))

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
        self.item_box = pg.transform.scale(pg.image.load(path.join(img_folder, ITEM_IMG)).convert_alpha(),(30,30))
        #for i in range(4):
        #    self.wood_pillar_img.append(pg.image.load(path.join(map_folder, WOOD_PILAR_IMG[i])).convert_alpha())
        for i in range(4):
            self.bullet_img.append(pg.image.load(path.join(weapon_folder, BULLET_IMGS[i])).convert_alpha())
        for i in range(7):
            self.explode_img.append(pg.image.load(path.join(vfx_folder, EXPLODE_IMG[i])).convert_alpha())
        for i in range(7):
            self.zombie1_img.append(pg.transform.scale(pg.image.load(path.join(enemy_folder, ZOMBIE1_IMG[i])).convert_alpha(), (35,56)))
        for i in range(6):
            self.boss_img.append(pg.transform.scale(pg.image.load(path.join(enemy_folder, BOSS_IMG[i])).convert_alpha(),(128, 128)))
        self.boss_bullet_img.append((pg.image.load(path.join(enemy_folder, BOSS_BULLET[0])).convert_alpha()))
        self.boss_bullet_img.append((pg.image.load(path.join(enemy_folder, BOSS_BULLET[1])).convert_alpha()))
        self.brankovic_font = os.path.join(font_folder, 'brankovic.ttf')
        self.poke_font = path.join(font_folder, 'PokemonGb-RAeo.ttf')
        self.start_screen = pg.transform.scale(pg.image.load(path.join(img_folder, START_SCREEN)).convert_alpha(),(WIDTH,HEIGHT))
        self.ending_screen = pg.transform.scale(pg.image.load(path.join(img_folder, END_SCREEN)).convert_alpha(),(WIDTH,HEIGHT))
        
        pass
    
    def show_start_screen(self):
        #GAME START시에 나타낼 스크린
        #pg.mixer.music.load(os.path.join(self.snd_dir, 'Mysterious.ogg'))
        #pg.mixer.music.play(loops=-1)
        self.screen_running = True
        self.start_new()
        
        #pg.mixer.music.fadeoRut(500)

    def start_new(self):
        self.start_group = pg.sprite.Group()
        
        self.start_run()

    def start_run(self):
        #start loop
        
            
        self.start_playing = True
        while self.start_playing:
            self.clock.tick(FPS)
            self.start_events()
            self.start_update()
            #self.check_range()
            self.start_draw()
            
    def start_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.start_playing:
                    self.start_playing = False
                self.start = False
           
            if event.type == pg.MOUSEBUTTONDOWN:
                
                pos = pg.mouse.get_pos()
                if startbutton.isOver(pos):
                    while g.screen_running:
                 # this g.running will take control of game over or not
                        g.running=True
                        self.start_playing = False
                        self.screen_running = False
                        #pg.quit()

                elif exitbutton.isOver(pos):
                    pg.quit()
                    quit()
                       
    def start_update(self):
        self.start_group.update()

    def start_draw(self):
        self.screen.blit(self.start_screen, (0,0))
        self.start_group.draw(self.screen)
        # pg.draw.rect(self.screen, WHITE,[155, 440, 100, 40])
        # pg.draw.rect(self.screen, WHITE,[155, 485, 100, 40])
        self.draw_text("START", 30, BLACK, WIDTH - 752, HEIGHT - 200)
        self.draw_text("START", 30, DARKGREY, WIDTH - 754, HEIGHT - 203)
        self.draw_text("EXIT", 30, BLACK, WIDTH - 748, HEIGHT - 150)
        self.draw_text("EXIT", 30, DARKGREY, WIDTH - 750, HEIGHT - 153)
       
        pg.display.update()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.brankovic_font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    
    def show_over_screen(self):
        # Game Over시에 나타낼 스크린
        self.screen.blit(self.ending_screen, (0,0))
        self.draw_text("GAVE OVER", 50, WHITE, WIDTH/2, HEIGHT/4)
        #self.draw_text("GAVE OVER", 48, BLACK, WIDTH/2, HEIGHT/4)
        self.draw_text("Survival Time : "+ str(self.second), 23, WHITE, WIDTH/2, HEIGHT/2)
        #self.draw_text("Survival Time : "+ str(self.second), 22, BLACK, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a 'Z' key to play again, 'ESC' to 'QUIT'", 23, WHITE, WIDTH/2, HEIGHT*3/4)
        #self.draw_text("Press a 'Z' key to play again, 'ESC' to 'QUIT'", 22, BLACK, WIDTH/2, HEIGHT*3/4)
        
        pg.display.update()
        sleep(1.5)
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                    self.start = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                        waiting = False
                    if event.key == pg.K_z:
                        self.start = True
                        waiting = False

startbutton = Button(155, 440, 100, 40)
exitbutton = Button(155, 485, 100, 40)
g = Game()
while g.start:
    g.show_start_screen() 
    # Game start when g.start is True
    while g.running:
        # this g.running will take control of game over or not
        g.new()
        g.show_over_screen()
pg.quit()