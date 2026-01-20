import pygame

from brick import Brick

class Wall:
    def __init__(self, grid_w, grid_h):
        self.bricks:list[Brick] = []
        self.grid_h = grid_h
        self.grid_w = grid_w
    
    def add_bricks(self, bricks:list[Brick]):
        for brick in bricks:
            self.bricks.append(brick)
    
    def update(self, grid,game):

        self.tetris_search()
        self.lines_down(game.frame)
        for brick in self.bricks:
            brick.update(grid)

    def draw(self, screen):
        for brick in self.bricks:
            brick.draw(screen)
    
    def top(self) -> list[Brick]:
        top:list[Brick] = []
        for i in range(self.grid_w):
            col = [wb for wb in self.bricks if wb.x == i]
            ys = [b.y for b in col]
            if len(ys) != 0:
                up_brick = col[ys.index(min(ys))]
                top.append(up_brick)
        return top
    
    def lines(self):
        lines = []
        for i in range(self.grid_h):
            lines.append( [b for b in self.bricks if b.y == self.grid_h - 1 - i])
        return lines
        
    def lines_down(self, frame):
        lines:list[list[Brick]] = self.lines()
        if frame % 3 == 0:
            down_lines = [
                line for i, line in enumerate(lines) if i != 0 and len(lines[i-1]) == 0 and len(line) != 0
            ]
            for line in down_lines:
                for brick in line:
                    brick.move(0, 1)

    def tetris_search(self):
        lines = 0
        for line in self.lines():
            if len(line) == self.grid_w:
                for b in line:
                    self.bricks.remove(b)
                lines += 1
        if lines != 0:
            if lines > 3:
                print("WOW! THIS IS TETRIS")
            else:
                print(lines, " LINES! GREAT!")
