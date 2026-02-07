import pygame

from wall import Wall

import random

from figure_fabric import FigureFactory

from settings import WIDTH, WIDTH_GRID, LEVELS, MAX_SPEED_LEVELS, MIN_SPEED_LEVELS

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

        self.grid = Grid(ceil_x=30, ceil_y=30)
        self.figure = self._add_figure()
        self.wall = Wall(self.grid.w, self.grid.h)
        self.dx = 0
        self.dy = 1
        self.fast_y = False

        self.level_speed = 0

        self.x_frame_count = 0

        self.score = 0

        self.level = 0
        self.lines_score = 0

        self.font = pygame.font.SysFont(None, 32)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.dx = -1
            elif event.key == pygame.K_d:
                self.dx = 1
            elif event.key == pygame.K_e:
                self.figure.rotate(self.grid, True)
            elif event.key == pygame.K_q:
                self.figure.rotate(self.grid, False)

    def _add_figure(self):
        typeF = random.randint(0, 5)
        return FigureFactory.create_figure(typeF, self.grid, self.grid.w // 2, 1, 1)

    def _add_wall(self):
        for brick in self.figure.bricks:
            brick.toWall()
            self.score += 1
        self.wall.add_bricks(self.figure.bricks)
        self.figure = self._add_figure()

    def add_score(self, n_line):
        score = round((MAX_SPEED_LEVELS / self.level_speed) * 100) * n_line * self.level
        self.lines_score += n_line
        self.score += score if n_line < 3 else 2 * score
    
    def level_up(self):
        l_keys = list(LEVELS.keys())
        for i, k in enumerate(l_keys[:1]):
            if k < self.lines_score and self.lines_score >= l_keys[i + 1]:
                self.level = LEVELS[l_keys[i + 1]]

        self.level_speed = MIN_SPEED_LEVELS - MAX_SPEED_LEVELS * self.level

    def update(self, game):
        self.level_up()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_d]:
            self.x_frame_count += 1
        else:
            self.x_frame_count = 0
        if keys[pygame.K_s]:
            self.fast_y = True

        if self.x_frame_count >= 15:
            self.dx = -1 if keys[pygame.K_a] else 1 if keys[pygame.K_d] else 0

        if game.frame % (4 if self.x_frame_count >= 15 else 6) == 0:
            is_wall_colid = any(
                (b.x + self.dx, b.y) in self.wall.position_map 
                for b in self.figure.bricks
            )

            if all([b.x + self.dx  < self.grid.w and b.x + self.dx >= 0 for b in self.figure.bricks]) and not is_wall_colid:
                self.figure.move(self.dx, 0)
            self.dx = 0                
        

        if game.frame % (self.level_speed if not self.fast_y else MAX_SPEED_LEVELS) == 0:
            is_wall_col = any(
                (b.x, b.y + self.dy) in self.wall.position_map
                for b in self.figure.bricks
            )

            if is_wall_col or any([b.y + self.dy >= self.grid.h for b in self.figure.bricks]):
                self._add_wall()
            elif not is_wall_col:
                self.figure.move(0, self.dy)

            self.fast_y = False

        if self.wall.wall_dead(): game.set_state(PlayingState())

        self.figure.update(self.grid)

        self.wall.update(self.grid, game, self.add_score)
        
        self.grid.update(self.wall)
                
    def draw(self, screen):
        screen.fill((0,0,0))

        text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - WIDTH_GRID // 2 - text.get_width() - 50, text.get_height() +20))
        self.grid.draw(screen)

        text = self.font.render(f"Lines: {self.lines_score}", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - WIDTH_GRID // 2 - text.get_width() - 50, text.get_height() + 70))

        if self.figure != None:
            self.figure.draw(screen)

        self.wall.draw(screen)


