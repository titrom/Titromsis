import pygame

from settings import WIDTH, HEIGHT


from brick import Brick
from figure import Figure, StickFigure, SideFigure
from wall import Wall

import random

from grid import Grid

class GameState:
    def handle_events(self, event:pygame.event.Event):
        pass

    def update(self, game):
        pass

    def draw(self, screen:pygame.Surface):
        pass

class PlayingState(GameState):
    def __init__(self):
        super().__init__()

        self.grid = Grid()

        self.figure = StickFigure(self.grid, self.grid.w // 2, 0, 0)
        self.wall = Wall(self.grid.w, self.grid.h)
        self.dx = 0
        self.dy = 1
        self.fast_y = False

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.figure.rotate(self.grid, True)
            elif event.key == pygame.K_q:
                self.figure.rotate(self.grid, False)

    def _add_figure(self):
        self.figure = StickFigure(self.grid, self.grid.w // 2, 0, random.randint(0,0))
    
    def _add_wall(self):
        for brick in self.figure.bricks:
            brick.toWall
        self.wall.add_bricks(self.figure.bricks)
        self._add_figure()

    def update(self, game):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.dx = -1
        elif keys[pygame.K_d]:
            self.dx = 1
        if keys[pygame.K_s]:
            self.fast_y = True

        '''
        Перенести в Grid
        '''
        if game.frame % 6 == 0:
            is_wall_colid = False
            for brick_wall in self.wall.bricks:
                if any((b.x + self.dx, b.y) == (brick_wall.x, brick_wall.y) for b in self.figure.bricks):
                        is_wall_colid = True

            if all([b.x + self.dx < self.grid_w and b.x + self.dx >= 0 for b in self.figure.bricks]) and not is_wall_colid:
                self.figure.move(self.dx, 0)
            self.dx = 0                

        '''
        Перенести в Grid
        '''       
        if game.frame % (30 if not self.fast_y else 2) == 0:
            is_wall_col = any([b.is_up(self.wall.top()) for b in self.figure.bricks]) if len(self.wall.bricks) != 0 else False

            if is_wall_col:
                    self._add_wall()
            if not is_wall_col:
                if any([b.y + self.dy >= self.grid_h for b in self.figure.bricks]):
                    self._add_wall()
                else:
                    self.figure.move(0, self.dy)
            
            self.fast_y = False

        if len(self.wall.bricks):
            if min([b.y for b in self.wall.top()]) + self.offset["top"] < 0:
                game.set_state(PlayingState())

        self.figure.update(self.grid)

        self.wall.update(self.grid, game)
                
    def draw(self, screen):
        screen.fill((0,0,0))

        if self.figure != None:
            self.figure.draw(screen)

        self.wall.draw(screen)

