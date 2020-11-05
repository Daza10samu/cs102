import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: float = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            return [[0] * self.cols for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        neighbours = []
        for row_id in range(max(cell[0] - 1, 0), min(cell[0] + 2, self.rows)):
            for col_id in range(max(cell[1] - 1, 0), min(cell[1] + 2, self.cols)):
                if row_id != cell[0] or col_id != cell[1]:
                    neighbours.append(self.curr_generation[row_id][col_id])
        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = self.create_grid(randomize=False)
        for row_id in range(self.rows):
            for col_id in range(self.cols):
                alive_count = sum(1 for x in self.get_neighbours((row_id, col_id)) if x == 1)
                if self.curr_generation[row_id][col_id] == 1 and not (
                    alive_count == 3 or alive_count == 2
                ):
                    new_grid[row_id][col_id] = 0
                elif self.curr_generation[row_id][col_id] == 0 and alive_count == 3:
                    new_grid[row_id][col_id] = 1
                else:
                    new_grid[row_id][col_id] = self.curr_generation[row_id][col_id]
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded:
            self.prev_generation, self.curr_generation = (
                self.curr_generation,
                self.get_next_generation(),
            )
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid: Grid
        grid = []
        with filename.open() as f:
            length = 0
            for line in f.readlines():
                line_stripped = line.strip("\n")
                if length == 0:
                    length = len(line_stripped)
                if len(line_stripped) != length or len(set(line_stripped) - {"0", "1"}) != 0:
                    raise ValueError("Формат файла не подходит")
                grid.append([])
                for char in line_stripped:
                    grid[-1].append(int(char))
        result_game = GameOfLife(size=(len(grid), length))
        result_game.curr_generation = grid
        return result_game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with filename.open("w") as f:
            for row in self.curr_generation:
                for elem in row:
                    f.write(str(elem))
                f.write("\n")
