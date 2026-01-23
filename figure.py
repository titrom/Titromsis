import pygame

from brick import Brick

from typing import Dict, Callable, Any

from enum import Enum

class SideFigure(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Figure:
    def __init__(self, grid, ceil_x, ceil_y, side:int):
        self.bricks:list[Brick] = []
        self.sides:Dict[SideFigure, Callable[..., Any]] = {}
        self.side = SideFigure(side)

    def move(self, dx, dy):
        for brick in self.bricks:
            brick.move(dx, dy)

    def rotate(self, grid, g_w,  right:bool):
        next_side = self.side
        if right:
            next_side = SideFigure(self.side.value + 1) if self.side.value < 3 else SideFigure.UP
            if not self._rotation_rules(next_side, g_w):
                return
        elif not right:
            next_side= SideFigure(self.side.value - 1) if self.side.value > 0 else SideFigure.LEFT
            if not self._rotation_rules(next_side, g_w):
                return
        
        self.side = next_side
        self.bricks = self.sides[self.side](grid, self.bricks[0].x, self.bricks[0].y)

    def _rotation_rules(self, next_side, g_w) -> bool:
        return True
    
    def _rotation_rule_wall(self, next_side, wall_bricks:list[Brick], grid) -> bool:
        new_bricks:list[Brick] = self.sides[next_side](grid, self.bricks[0].x, self.bricks[0].y)
        
        return all([ not pygame.Rect.colliderect(b.rect, wb.rect) for b in new_bricks for wb in wall_bricks ])
    
    def _rotation_rule_screen(self, g_h, g_w) -> bool:
        return False

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
    '''
    Перенести в Grid.
    Записи по типу g[c_y][c_x].должны быть типа отдельным методом. А лучше если сетак будет говорить занета ли ее ячейка, если все нужные ячейки заняты то шлем нахуй
    '''
    def __init__(self, grid, ceil_x, ceil_y, side:int):
        super().__init__(grid, ceil_x, ceil_y, side)

        self.sides[SideFigure.UP] = lambda g, c_x, c_y:[
            Brick(g[c_y][c_x], c_x, c_y),
            Brick(g[c_y + 1][c_x], c_x, c_y + 1),
            Brick(g[c_y + 2][c_x], c_x, c_y + 2),
            Brick(g[c_y + 3][c_x], c_x, c_y + 3)
        ]

        self.sides[SideFigure.DOWN] = lambda g, c_x, c_y:[
            Brick(g[c_y][c_x], c_x, c_y),
            Brick(g[c_y - 1][c_x], c_x, c_y - 1),
            Brick(g[c_y - 2][c_x], c_x, c_y - 2),
            Brick(g[c_y - 3][c_x], c_x, c_y - 3)
        ]

        self.sides[SideFigure.RIGHT] = lambda g, c_x, c_y: [
            Brick(g[c_y][c_x], c_x, c_y),
            Brick(g[c_y][c_x + 1], c_x + 1, c_y),
            Brick(g[c_y][c_x -1], c_x - 1, c_y),
            Brick(g[c_y][c_x -2], c_x - 2, c_y)
        ]

        self.sides[SideFigure.LEFT] = lambda g, c_x, c_y: [
            Brick(g[c_y][c_x], c_x, c_y),
            Brick(g[c_y][c_x - 1], c_x - 1, c_y),
            Brick(g[c_y][c_x + 1], c_x + 1, c_y),
            Brick(g[c_y][c_x + 2], c_x + 2, c_y)
        ]

        self.bricks = self.sides[self.side](grid, ceil_x, ceil_y)
        