import pygame

from ceil import Ceil

from grid import Grid

class Brick:

    def __init__(self, ceil:Ceil):
        self.is_create = ceil != None

        if not self.is_create:
            return None
        self.x = ceil.x
        self.y = ceil.y
        self.rect = ceil.rect
        self.is_wall = False

    def toWall(self):
        self.is_wall = True
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def moveTo(self, x, y):
        self.x, self.y = x, y

    def is_up(self, bricks):
        result = False
        for brick in bricks:
            result = brick.x == self.x and brick.y - 1 == self.y
            if result:
                break
    
        return result

    def update(self, grid:Grid):
        new_rect = grid.get_ceil(self.x, self.y)
        if new_rect != None:
            self.rect = new_rect.rect

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 50, 50), self.rect) 