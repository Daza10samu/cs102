import random
import typing as tp

import pygame
from pygame.constants import QUIT

# from pygame.locals import *


Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid: Grid
        self.grid = []

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()
            self.draw_grid()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            return [
                [random.randint(0, 1) for _ in range(self.cell_width)]
                for _ in range(self.cell_height)
            ]
        else:
            return [[0] * self.cell_width for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row_id in range(self.cell_height):
            for col_id in range(self.cell_width):
                if self.grid[row_id][col_id] == 1:
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

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        for row_id in range(max(cell[0] - 1, 0), min(cell[0] + 2, self.cell_height)):
            for col_id in range(max(cell[1] - 1, 0), min(cell[1] + 2, self.cell_width)):
                if row_id != cell[0] or col_id != cell[1]:
                    neighbours.append(self.grid[row_id][col_id])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = self.create_grid(randomize=False)
        for row_id in range(self.cell_height):
            for col_id in range(self.cell_width):
                alive_count = sum(1 for x in self.get_neighbours((row_id, col_id)) if x == 1)
                if self.grid[row_id][col_id] == 1 and not (alive_count == 3 or alive_count == 2):
                    new_grid[row_id][col_id] = 0
                elif self.grid[row_id][col_id] == 0 and alive_count == 3:
                    new_grid[row_id][col_id] = 1
                else:
                    new_grid[row_id][col_id] = self.grid[row_id][col_id]
        return new_grid
