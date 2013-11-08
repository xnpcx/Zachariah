import pygame, sys, player
from pygame.locals import *
from pixelperfect import *
import tmx
import os


def load():
    dt = 60.0
    
    pygame.init()
    screen = pygame.display.get_surface()
    
    clock = pygame.time.Clock()
    lvl = Level(screen, 'test')

    
    """Main loop"""
    while True:
        key = pygame.key.get_pressed()
        lvl.tilemap.update(dt, lvl, key)
        screen.fill((0,100,0))
        lvl.tilemap.draw(screen)

        pygame.display.update()
        clock.tick(dt)
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lvl.hero.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    lvl.hero.jump_cut()
                
class Level(object):
    
    def __init__(self, screen, name):
        
        """Loading the level files, changing the CWD to match the files for loading,
        This was easier than having to edit the .tmx file every time it needed to
        be edited."""
        os.chdir('levels/%s/' % name)
        self.level = "%s.tmx" % name
        self.tilesheet = pygame.image.load('%s.png' % name)
        self.tilemap = tmx.load(self.level, screen.get_size())
        os.chdir('../..')
        
        """Loading the 'hero' into the level, and adding him/her to the self.sprites group"""
        self.sprites = tmx.SpriteLayer()
        self.start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.hero = player.Player(self, (self.start_cell.px, self.start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)
        
        """Cell, rect, and mask dicts"""
        self.cell_size = (self.tilemap.layers['Tile Layer 1'].tile_width, self.tilemap.layers['Tile Layer 1'].tile_height)
        self.cells_dict = self.tilemap.layers['Tile Layer 1'].cells
        self.height_dict = self.gen_height_map()
        self.rect_dict = self.get_rect_dict()
        self.mask_dict = self.make_mask_dict()
        
        
    def set_player_loc(self, player, loc):
        player.rect.center = loc
        
    def get_rect_dict(self):
        rect_dict = {}
        for coord, cell in self.cells_dict.items():
            rect_dict[coord] = cell.tile.surface.get_rect(x = coord[0] * self.cell_size[0], y = coord[1] * self.cell_size[1])
        return rect_dict

        
    def gen_height_map(self):
        height_dict = {}
        test_mask = pygame.Mask((1,self.tilemap.layers['Tile Layer 1'].tile_width))
        test_mask.fill()
        for coord, cell in self.cells_dict.items():
            heights = []
            mask = pygame.mask.from_surface(cell.tile.surface)
            for i in range(cell.tile.surface.get_width()):
                height = mask.overlap_area(test_mask,(i, 0))
                heights.append(height)
            height_dict[(coord)] = heights
        return height_dict
    
    def make_mask_dict(self):
        mask_dict = {}
        for i, cell in self.cells_dict.items():
            mask_dict[i] = pygame.mask.from_surface(cell.tile.surface)
        return mask_dict
        
        
        
        
        