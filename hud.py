import pygame as pg
import os
from os import path
from setting import *
BAR_LENGTH = 100
BAR_HEIGHT = 30
class button():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
 
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

def draw_player_health(surf, x, y, health, amor, max_health):
    # 현재 체력과 방어력, 그리고 최대체력의 한계치를 받아옴.
    pct = (health+amor)/max_health
    # 최대치에대한 체력과 방어력의 비율
    if pct < 0:
        pct = 0
    try:
        amor_pct = amor/(health+amor)
        # 내 체력에서 방어력 비율
        health_pct = health/PLAYER_HEALTH
        # 실제 체력에서 체력 비율
    except ZeroDivisionError:
        amor_pct = 0
        health_pct = 0
        # health+amor가 0이되는 순간도 존재하기때문에 예외처리
    if pct < amor_pct or amor <= 0:
        health_fill = (health_pct+amor_pct)* BAR_LENGTH
    else:
        health_fill = (pct-amor_pct) * BAR_LENGTH
    amor_fill = pct * BAR_LENGTH
    # amor가 있다면 체력보다 BAR_LENGTH가 앞에있어서, 가장긺.
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    #외곽 테두리
    health_fill_rect = pg.Rect(x, y, health_fill, BAR_HEIGHT)
    amor_fill_rect = pg.Rect(x, y, amor_fill, BAR_HEIGHT)

    amor_col = SILVER

    if health_pct > 0.6:
        col = GREEN
    elif health_pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, amor_col, amor_fill_rect)
    pg.draw.rect(surf, col, health_fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 3)
    # 그리는 순서를 아머->체력->외곽 순으로 그려서 체력이 아머위에 덧쓰워져서 아머가 채워진것처럼 보인다.

def draw_gun_list(surf, gunstatus, gun_now):
    for idx, val in enumerate(gunstatus):
        draw_gun(surf, BAR_LENGTH + 40 + idx * 80, HEIGHT-60, val, idx, gun_now)

def draw_gun(surf, x, y, possible, gun_kind, gun_now):
    BAR_WIDTH = 50
    BAR_HEIGHT = 50
    image = 0
    rotated = 0
    game_folder = path.dirname(__file__)
    img_folder = path.join(game_folder, 'Image','weapon')
    
    if gun_kind == 0:
        image = pg.image.load(path.join(img_folder, WEAPON_IMGS[gun_kind][0])).convert_alpha()
        rotated = pg.transform.scale(pg.transform.rotate(image, 40),(48, 48))
    if gun_kind == 1:
        image = pg.image.load(path.join(img_folder, WEAPON_IMGS[gun_kind][0])).convert_alpha()
        rotated = pg.transform.scale(pg.transform.rotate(image, 40),(48, 48))
    if gun_kind == 2:
        image = pg.image.load(path.join(img_folder, WEAPON_IMGS[gun_kind][0])).convert_alpha()
        rotated = pg.transform.scale(pg.transform.rotate(image, 40),(48, 48))
    if gun_kind == 3:
        image = pg.image.load(path.join(img_folder, WEAPON_IMGS[gun_kind][0])).convert_alpha()
        rotated = pg.transform.scale(pg.transform.rotate(image, 40),(48, 48))

    if possible[0]:
        gun_rect = pg.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        pg.draw.rect(surf, LIGHTGREY, gun_rect)
        if gun_kind == gun_now:
            pg.draw.rect(surf, RED, gun_rect,2)
        else:
            pg.draw.rect(surf, WHITE, gun_rect,2)
        surf.blit(rotated, (x+2, y+2))
    else:
        gun_rect = pg.Rect(x, y, BAR_WIDTH - 10, BAR_HEIGHT - 10)
        rotated = pg.transform.scale(rotated, (36,36))
        pg.draw.rect(surf, LIGHTGREY, gun_rect)
        if gun_kind == gun_now:
            pg.draw.rect(surf, RED, gun_rect,2)
        else:
            pg.draw.rect(surf, WHITE, gun_rect,2)
        surf.blit(rotated, (x+2, y+2))

def draw_grenade_list(surf, grenade_left):
    for idx in range(grenade_left):
        draw_grenade(surf, WIDTH-40-(idx*25), HEIGHT-40)
    pass

def draw_grenade(surf, x, y):
    game_folder = path.dirname(__file__)
    img_folder = path.join(game_folder, 'Image','weapon')
    image = pg.transform.scale(pg.image.load(path.join(img_folder, GRENADE_IMG)).convert_alpha(),(20, 24))

    surf.blit(image, (x, y))
    pass

def draw_money(surf, x, y, money_amount, in_font):
    font = pg.font.Font(in_font, 30)
    text = font.render(f"Money: {money_amount}",True, GOLD)
    surf.blit(text, (x,y))  
    pass