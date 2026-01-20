import pygame

class Brick:

    def __init__(self, rect:pygame.Rect, ceil_x, ceil_y):
        self.rect = rect
        self.x = ceil_x
        self.y = ceil_y
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

    def update(self, grid):
        self.rect = grid[self.y][self.x]

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 50, 50), self.rect) 