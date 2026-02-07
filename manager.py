import pygame

from settings import (
    TIMEOUT_MOVE_Y_MIN,
    TIMEOUT_MOVE_X_MIN,
    TIMEOUT_DEDOUNCE_DIRECTION_X,
    TIMEOUT_MOVE_Y_MAX,
    TIMEOUT_MOVE_X_MAX,
)


# Базовый класа Manager
# Manager - это сущность которое отслеживает один тип поведения в игре
# И/или он может управлять только одной областью
class Manager:
    def handler_event(self, event):
        pass

    def update(self):
        pass


# InputManager Отслеживает нажатия кнопок
# Управлет напровление и скоростью передвежения
# dx, dy - на сколько долны измениться координаты
# speed_x,speed_y - как часто direction будет не равен базовым занчениям
# fast_y - флаг для включения ускореного спуска
# x_frame_count - дебаунс нажатия кнопок управления по горизонтали
class InputManager(Manager):
    def __init__(self):
        super().__init__()
        self._dx: int = 0
        self._dy: int = 1

        self._speed_x: int = TIMEOUT_MOVE_X_MIN
        self._speed_y: int = TIMEOUT_MOVE_Y_MIN

        self._fast_y: bool = False

    @property
    def dx(self) -> int:
        return self._dx

    @property
    def dy(self) -> int:
        return self._dy

    @property
    def speed_x(self) -> int:
        return self._speed_x

    @property
    def speed_y(self) -> int:
        return self._speed_y

    @speed_y.setter
    def speed_y(self, value: int):
        self._speed_y = value

    # Обрабатываем эвенты на перемещения и поворот
    # В случае поворота возвращаем событие rotate c параметром который указывает направление
    # в противном случак возвращаем None
    def handler_event(self, event: pygame.event.Event) -> dict[str, bool] | None:
        super().handler_event(event)
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_a:
                        self._dx = -1
                    case pygame.K_d:
                        self._dx = 1
                    case pygame.K_e:
                        return {"rotate": True}
                    case pygame.K_q:
                        return {"rotate": False}
                    case pygame.K_s:
                        self._fast_y = True
            case pygame.KEYUP:
                match event.key:
                    case pygame.K_a:
                        self._dx = 0
                    case pygame.K_d:
                        self._dx = 0
                    case pygame.K_s:
                        self._fast_y = False


    # обнновляем скорости
    def update(self, t_dx: int, t_dy: int) -> None:
        self._speed_x = TIMEOUT_MOVE_X_MIN
        # (
        #     TIMEOUT_MOVE_X_MAX
        #     if self._x_frame_count >= TIMEOUT_DEDOUNCE_DIRECTION_X
        #     else TIMEOUT_MOVE_X_MIN
        # )
        self._speed_y = TIMEOUT_MOVE_Y_MIN if not self._fast_y else TIMEOUT_MOVE_Y_MAX

