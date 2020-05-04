import pygame as pg
from setting import *
import pytmx
def collide_hit_rect(first, second):
    return first.hitbox.colliderect(second.rect)
def collide_hit_box(first, second):
    return first.hitbox.colliderect(second.hitbox)
    
class Map:
    def __init__(self, filename):
        self.data = []
        #read data from filename
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        #store data of the map
        
class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # if the player go right, the map should go to right. 
        # and player will in the middle of the game so add WIDTH /2
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)
        x = min(0,x) # left
        y = min(0,y) # top
        x = max(-(self.width - WIDTH), x) #right
        y = max(-(self.height - HEIGHT), y) #bottom
        self.camera = pg.Rect(x,y,self.width, self.height)
    
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

class Button():
    def __init__(self, color, position, width, height, surface, text = ''):
        self.color = color
        self.pos = position
        self.width = width
        self.height = height
        self.text = text
        self.surface = surface

    def draw(self, outline=None):
        if outline:
            pg.draw.rect(self.surface, outline, (self.pos.x-2,self.pos.y-2,self.width+4,self.height+4), 0)
        pg.draw.rect(self.surface, self.color, (self.pos.x, self.pos.y, self.width, self.height), 0)
        if self.text != '':
            font = pg.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            self.surface.blit(text, (self.pos.x + (self.width/2 - text.get_width()/2), self.pos.y + (self.height/2 - text.get_height()/2)))
    
    def isOver(self, pos):
        if self.pos.x < pos[0] and pos[0] <self.pos.x +self.width:
            if self.pos.y < pos[1] <self.pos.y + self.height:
                return True
        return False
