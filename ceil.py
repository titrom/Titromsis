import pygame
'''
класс из которого состоит Grid
'''
class Ceil:
    def __init__(self, x, y, rect) -> None:
        self.x = x
        self.y = y
        self.rect = rect
        self.is_busy = False