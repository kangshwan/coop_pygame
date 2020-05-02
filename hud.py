import pygame as pg
from setting import *
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 30
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 3)

def draw_gun_list(surf, gunstatus):
    for idx, val in enumerate(gunstatus):
        draw_gun(surf, 140 + idx * 80, HEIGHT-60, val)

def draw_gun(surf, x, y, possible):
    BAR_LENGTH = 50
    BAR_HEIGHT = 50

    if possible[0]:
        gun_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        pg.draw.rect(surf, LIGHTGREY, gun_rect)
        pg.draw.rect(surf, WHITE, gun_rect,2)
    else:
        gun_rect = pg.Rect(x, y, BAR_LENGTH - 10, BAR_HEIGHT - 10)
        pg.draw.rect(surf, LIGHTGREY, gun_rect)
        pg.draw.rect(surf, WHITE, gun_rect,2)