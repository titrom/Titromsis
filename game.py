import pygame

from settings import WIDTH, HEIGHT, FPS

from game_state import PlayingState

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")

        self.clock = pygame.time.Clock()
        self.running = True
        
        self.current_state = PlayingState()

        self.frame = 0

    def set_state(self, new_state):
        self.current_state = new_state

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            else:
                result = self.current_state.handle_events(event)
    
    def update(self):
        self.current_state.update(self)
        self.frame += 1
        if self.frame == 60:
            self.frame = 0

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
