from __future__ import annotations

import random
from typing import Optional

import pygame

from figure_fabric import FigureFactory
from grid import Grid
from manager import InputManager
from settings import (
    LEVELS,
    TIMEOUT_MOVE_Y_MAX,
    TIMEOUT_MOVE_Y_MIN,
    WIDTH,
    WIDTH_GRID,
    TIMEOUT_MOVE_X_MIN,
)
from wall import Wall

from figure import Figure


# Базовый класс состояний (экранов) игры
class GameState:
    # оброботка событий создоваемых пользователями
    def handle_events(self, event: pygame.event.Event):
        pass

    # Основной цикл экрана. Здесь проиходят все вычесления
    def update(self, game: Optional["Game"], c_time: int):            
        pass

    # Здесь отресовываються все элементы экрана
    def draw(self, screen: pygame.Surface):
        pass


# Основной экран игры
# grid - экземпляр класа Grid
# figure - экземпляр класса Figure создоваемы при помощи Figure Factory
# input_manager - экземпляр класса InputManager
class PlayingState(GameState):
    def __init__(self):
        super().__init__()

        self.grid: Grid = Grid(ceil_x=30, ceil_y=30)
        self._add_figure()
        self.wall: Wall = Wall(self.grid.w, self.grid.h)

        self.input_manager: InputManager = InputManager()

        self.level_speed: int = 0

        self.score: int = 0

        self.level: int = 0
        self.lines_score: int = 0

        self.timer_move_x = pygame.time.get_ticks()
        self.timer_move_y = pygame.time.get_ticks()

        self.font: pygame.font.Font = pygame.font.SysFont(None, 32)

    # передаем input_manger события в текущем кадре
    # он может вернуть значение отличное от None
    # Мы ожидаем событие rotat, если оно есть то поворачиваем figure
    # на основе передаваемего параметра
    def handle_events(self, event):
        call_back = self.input_manager.handler_event(event)
        if call_back is not None:
            if "rotate" in call_back:
                self.figure.rotate(self.grid, call_back["rotate"])

    def _add_figure(self):
        typeF = random.randint(0, 6)
        self.figure:Figure = FigureFactory.create_figure(
            typeF, self.grid, self.grid.w // 2, 1, 1
        )

    def _add_wall(self):
        for brick in self.figure.bricks:
            brick.toWall()
            self.score += 1
        self.wall.add_bricks(self.figure.bricks)
        self._add_figure()

    def add_score(self, n_line):
        score = (
            round((TIMEOUT_MOVE_Y_MAX / self.level_speed) * 100) * n_line * self.level
        )
        self.lines_score += n_line
        self.score += score if n_line < 3 else 2 * score

    def level_up(self):
        l_keys = list(LEVELS.keys())
        for i, k in enumerate(l_keys[:1]):
            if k < self.lines_score and self.lines_score >= l_keys[i + 1]:
                self.level = LEVELS[l_keys[i + 1]]

        self.level_speed = TIMEOUT_MOVE_Y_MIN - TIMEOUT_MOVE_Y_MAX * self.level

    def update(self, game: Optional["Game"], c_time: int):
        if game is None:
            return
        self.level_up()

        self.input_manager.update(
            t_dx=game.current_time - self.timer_move_x,
            t_dy=game.current_time - self.timer_move_y,
        )

        if game.current_time - self.timer_move_x >= self.input_manager.speed_x:
            is_wall_colid = any(
                (b.x + self.input_manager.dx, b.y) in self.wall.position_map
                for b in self.figure.bricks
            )

            if (
                all(
                    [
                        b.x + self.input_manager.dx < self.grid.w
                        and b.x + self.input_manager.dx >= 0
                        for b in self.figure.bricks
                    ]
                )
                and not is_wall_colid
            ):
                self.figure.move(self.input_manager.dx, 0)
                self.timer_move_x = pygame.time.get_ticks()

        if game.current_time - self.timer_move_y >= self.input_manager.speed_y:
            is_wall_col = any(
                (b.x, b.y + self.input_manager.dy) in self.wall.position_map
                for b in self.figure.bricks
            )

            if is_wall_col or any(
                [b.y + self.input_manager.dy >= self.grid.h for b in self.figure.bricks]
            ):
                self._add_wall()
            elif not is_wall_col:
                self.figure.move(0, self.input_manager.dy)
            
            self.timer_move_y = pygame.time.get_ticks()

        if self.wall.wall_dead():
            game.set_state(PlayingState())

        self.figure.update(self.grid)

        self.wall.update(self.grid, game, self.add_score)

        self.grid.update(self.wall)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(
            text,
            (
                WIDTH // 2 - WIDTH_GRID // 2 - text.get_width() - 50,
                text.get_height() + 20,
            ),
        )
        self.grid.draw(screen)

        text = self.font.render(f"Lines: {self.lines_score}", True, (255, 255, 255))
        screen.blit(
            text,
            (
                WIDTH // 2 - WIDTH_GRID // 2 - text.get_width() - 50,
                text.get_height() + 70,
            ),
        )

        self.figure.draw(screen)

        self.wall.draw(screen)
