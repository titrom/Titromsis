import pygame

from settings import WIDTH_GRID, HEIGHT_GRID

from ceil import Ceil

class Grid:
    def __init__(self, top:int = 50, left:int = 640-160, ceil_x:int = 20, ceil_y:int = 20) -> None:

        w = range(0, (WIDTH_GRID // ceil_x))
        h = range(0, (HEIGHT_GRID  // ceil_y))

        self.w = len(w)
        self.h = len(h)

        self.top = top
        self.left = left

        self.ceils = {
            (x, y): Ceil(x, y, pygame.Rect((x * ceil_x) + self.left, (y * ceil_y) + self.top, ceil_x, ceil_y)) for x in w  for y in h
        }
            
    def is_busy_ceil(self, ceils:list[Ceil]) -> int|bool:
        for ceil in ceils:
            g_ceil = self.get_ceil(ceil.x, ceil.y)
            if g_ceil != None and g_ceil.is_busy:
                return True
        return False
    
    def update(self, wall):
        for cord_ceil in self.ceils:
            self.ceils[cord_ceil].is_busy = cord_ceil in wall.position_map
    def get_ceil(self, x, y):
        return self.ceils.get((x, y)) 
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.left, self.top, WIDTH_GRID, HEIGHT_GRID), width=2)
    

        
            
        