import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for row_id in range(self.life.rows):
            for col_id in range(self.life.cols):
                if self.life.curr_generation[row_id][col_id] == 1:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        pygame.Rect(
                            self.cell_size * col_id + 1,
                            self.cell_size * row_id + 1,
                            self.cell_size - 1,
                            self.cell_size - 1,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        pygame.Rect(
                            self.cell_size * col_id + 1,
                            self.cell_size * row_id + 1,
                            self.cell_size - 1,
                            self.cell_size - 1,
                        ),
                    )

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYUP and event.key == K_SPACE:
                    paused = bool(paused ^ 1)
                if paused and event.type == MOUSEBUTTONUP and event.button == 1:
                    left, top = pygame.mouse.get_pos()
                    self.life.curr_generation[top // self.cell_size][left // self.cell_size] = \
                        self.life.curr_generation[top // self.cell_size][left // self.cell_size] ^ 1
                    self.draw_grid()
                    pygame.display.flip()

            if not paused:
                self.draw_lines()

                # Отрисовка списка клеток
                # Выполнение одного шага игры (обновление состояния ячеек)
                self.life.step()
                self.draw_grid()
                if self.life.is_max_generations_exceeded or not self.life.is_changing:
                    paused = True

                pygame.display.flip()
                clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife(size=(24, 46), randomize=False)
    game = GUI(life, cell_size=40)
    game.run()
