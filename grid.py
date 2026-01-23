import pygame

from settings import WIDTH, HEIGHT

class Grid:
    def __init__(self, top:int= -5, bottom:int =0, ceil_x:int = 35, ceil_y:int=35) -> None:

        self.ceils = [[pygame.Rect(x * ceil_x, y * ceil_y, ceil_x, ceil_y) for x in range(WIDTH // ceil_x)] for y in range(top , (HEIGHT - bottom) // ceil_y)] # Переделать на маив ceil

        self.w = len(self.ceils[0])
        self.h = len(self.ceils)

        self.offset = {"top": top, "bottom": bottom}

