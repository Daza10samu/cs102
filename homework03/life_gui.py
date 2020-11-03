import pathlib

import pygame
from pygame.locals import *
# from pygame.constants import K_LCTRL, K_SPACE, KEYDOWN, KEYUP, MOUSEBUTTONUP, QUIT, K_r, K_s

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(
        self, life: GameOfLife, cell_size: int = 10, speed: int = 10, save_path: str = "grid"
    ) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed
        self.save_path = pathlib.Path(save_path)

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
        is_ctrl_pressed = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN and event.key == K_r:
                    self.life.curr_generation = self.life.create_grid(randomize=True)
                    paused = False
                if event.type == KEYDOWN and event.key == K_SPACE:
                    paused = bool(paused ^ 1)
                if event.type == KEYDOWN and event.key == K_LCTRL:
                    is_ctrl_pressed = True
                if event.type == KEYUP and event.key == K_LCTRL:
                    is_ctrl_pressed = False
                if is_ctrl_pressed and event.type == KEYDOWN and event.key == K_s:
                    self.life.save(self.save_path)
                if paused and event.type == MOUSEBUTTONUP and event.button == 1:
                    left, top = pygame.mouse.get_pos()
                    self.life.curr_generation[top // self.cell_size][left // self.cell_size] = (
                        self.life.curr_generation[top // self.cell_size][left // self.cell_size] ^ 1
                    )
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
