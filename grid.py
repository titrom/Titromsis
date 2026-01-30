import pygame

from settings import WIDTH, HEIGHT

from ceil import Ceil

class Grid:
    def __init__(self, top:int = 0, bottom:int = 0, ceil_x:int = 35, ceil_y:int = 35) -> None:

        self.offset = {"top": top, "bottom": bottom}

        w = range(WIDTH // ceil_x)
        h = range(self.offset["top"], (HEIGHT - self.offset["bottom"]) // ceil_y)


        self.w = len(w)
        self.h = len(h)

        self.ceils = [Ceil(x, y, pygame.Rect(x * ceil_x, y * ceil_y, ceil_x, ceil_y)) for x in w  for y in h]

    
    def is_busy_ceil(self, ceils:list[Ceil]) -> int|bool:
        for ceil in ceils:
            g_ceil = self.get_ceil(ceil.x, ceil.y)
            if g_ceil == None:
                return False
            if g_ceil.is_busy:
                return True
        return False

    def occupy_ceils(self, ceils:list[Ceil]):
        for ceil in ceils:
            g_ceil = self.get_ceil(ceil.x, ceil.y)
            if g_ceil == None:
                return False
            g_ceil.is_busy = True
        return True
    
    def get_ceil(self, x, y):
        return next((c for c in self.ceils if c.x == x and c.y == y), None) 
    

        
            
        