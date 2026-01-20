import pygame

from brick import Brick

from enum import Enum

class SideFigure(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class RotateD(Enum):
    RIGHT = 1
    LEFT = -1

class Figure:
    def __init__(self, grid, ceil_x, ceil_y, side:int):
        self.bricks:list[Brick] = []
        self.sides = {SideFigure.UP: [], SideFigure.RIGHT: [], SideFigure.DOWN: [], SideFigure.LEFT: []}
        self.side = SideFigure(side)

    def move(self, dx, dy):
        for brick in self.bricks:
            brick.move(dx, dy)

    def rotate(self, grid):
        pass

    def is_wall(self) -> bool:
        return len(self.bricks) == len([i for i in self.bricks if i.is_wall])

    def update(self, grid):
        all_connect_bricks = [i for i in self.bricks if i.is_wall]
        if len(all_connect_bricks) >= 1:
            for brick in self.bricks:
                brick.toWall()
        if not self.is_wall():        
            for brick in self.bricks:
                brick.update(grid)

    def draw(self, screen):
        for brick in self.bricks:
            brick.draw(screen)
            
class StickFigure(Figure):

    def __init__(self, grid, ceil_x, ceil_y, side:int):
        super().__init__(grid, ceil_x, ceil_y, side)

        self.sides[SideFigure.UP] = [
            Brick(grid[ceil_y][ceil_x], ceil_x, ceil_y),
            Brick(grid[ceil_y + 1][ceil_x], ceil_x, ceil_y + 1),
            Brick(grid[ceil_y + 2][ceil_x], ceil_x, ceil_y + 2),
            Brick(grid[ceil_y + 3][ceil_x], ceil_x, ceil_y + 3)
        ]

        self.sides[SideFigure.DOWN] = self.sides[SideFigure.UP]

        self.sides[SideFigure.RIGHT] = [
            Brick(grid[ceil_y][ceil_x], ceil_x, ceil_y),
            Brick(grid[ceil_y][ceil_x + 1], ceil_x + 1, ceil_y),
            Brick(grid[ceil_y][ceil_x -1], ceil_x - 1, ceil_y),
            Brick(grid[ceil_y][ceil_x -2], ceil_x - 2, ceil_y)
        ]

        self.sides[SideFigure.LEFT] = self.sides[SideFigure.RIGHT]
        #[
        #     Brick(grid[ceil_y][ceil_x], ceil_x, ceil_y),
        #     Brick(grid[ceil_y][ceil_x - 1], ceil_x - 1, ceil_y),
        #     Brick(grid[ceil_y][ceil_x + 1], ceil_x + 1, ceil_y),
        #     Brick(grid[ceil_y][ceil_x + 2], ceil_x + 2, ceil_y)
        # ]

        self.bricks = self.sides[self.side]
        print(self.bricks)

    def rotate(self, grid):
        if self.side.value % 2 == 0:
            self.side = SideFigure.RIGHT
            self._up_to_right(grid)
        else:
            self.side = SideFigure.UP
            self._right_to_up(grid)

    def _up_to_right(self, grid):
        self.bricks[1].rect, self.bricks[1].x, self.bricks[1].y = grid[self.bricks[1].y - 1][self.bricks[1].x + 1], self.bricks[1].x + 1, self.bricks[1].y - 1
        self.bricks[2].rect, self.bricks[2].x, self.bricks[2].y = grid[self.bricks[1].y - 2][self.bricks[1].x - 1], self.bricks[2].x - 1, self.bricks[2].y - 2
        self.bricks[3].rect, self.bricks[3].x, self.bricks[3].y = grid[self.bricks[1].y - 3][self.bricks[1].x - 2], self.bricks[3].x - 2, self.bricks[3].y - 3
    
    def _right_to_up(self, grid):
        self.bricks[1].rect, self.bricks[1].x, self.bricks[1].y = grid[self.bricks[1].y + 1][self.bricks[1].x - 1], self.bricks[1].x - 1, self.bricks[1].y + 1
        self.bricks[2].rect, self.bricks[2].x, self.bricks[2].y = grid[self.bricks[1].y + 2][self.bricks[1].x + 1], self.bricks[2].x + 1, self.bricks[2].y + 2
        self.bricks[3].rect, self.bricks[3].x, self.bricks[3].y = grid[self.bricks[1].y + 3][self.bricks[1].x + 2], self.bricks[3].x + 2, self.bricks[3].y + 3