import pygame

from brick import Brick


class Wall:
    def __init__(self, grid_w, grid_h):
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.position_map: dict[tuple[int, int], Brick] = {}
        self.full_lines = set()

    def update_full_lines(self):
        line_counts = {}
        for brick in self.position_map.values():
            if brick.y not in line_counts:
                line_counts[brick.y] = 0
            line_counts[brick.y] += 1

        self.full_lines = {
            y for y, count in line_counts.items()
            if count == self.grid_w
        }
    
    def add_bricks(self, bricks:list[Brick]):
        for brick in bricks:
            self.position_map[(brick.x, brick.y)] = brick

    def remove_brick_at_position(self, x, y):
        if (x, y) in self.position_map:
            self.position_map.pop((x,y))
    
    def update(self, grid, game, add_score_event):
        self.tetris_search(add_score_event)
        # self.lines_down(game.frame)
        new_bricks = [b for b in self.position_map.values()]
        for brick in new_bricks:
            brick.update(grid)
        
        self.position_map.clear()
        self.add_bricks(new_bricks)

    def draw(self, screen):
        for brick in self.position_map.values():
            brick.draw(screen)
    
    def lines(self) -> list[list[Brick]]:
        lines = []
        for i in range(self.grid_h):
            lines.append( [b for b in self.position_map.values() if b.y == self.grid_h - 1 - i])
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
    

    def tetris_search(self, add):
        lines_to_remove = 0
        for y in self.full_lines:
            bricks_in_line = [b for b in self.position_map.values() if b.y == y]
            [self.remove_brick_at_position(b.x, b.y) for b in bricks_in_line]
            lines_to_remove += 1

        if lines_to_remove:
            add(lines_to_remove)

        self.update_full_lines()

    
    def wall_dead(self) -> bool:
        return min([b.y for b in self.position_map.values()]) <= 0 if len(self.position_map) != 0 else False