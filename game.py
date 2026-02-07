
import pygame

from game_state import GameState, PlayingState
from settings import FPS, HEIGHT, WIDTH


class Game:
    def __init__(self):
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running = True

        self.current_state: GameState = PlayingState()

        self.current_time: int = pygame.time.get_ticks()

    def set_state(self, new_state: GameState):
        self.current_state = new_state

    def handle_events(self):
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                self.running = False
            else:
                result = self.current_state.handle_events(event)

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.current_state.update(self, self.current_time)

    def draw(self):
        self.current_state.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
