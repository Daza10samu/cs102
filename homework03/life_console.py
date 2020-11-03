import curses
import pathlib
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife, speed: int = 2, save_path: str = "grid") -> None:
        super().__init__(life)
        self.speed = speed
        self.save_path = pathlib.Path(save_path)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for row_id in range(self.life.rows):
            for col_id in range(self.life.cols):
                if self.life.curr_generation[row_id][col_id] == 1:
                    screen.addch(row_id + 1, col_id + 1, "*")
                else:
                    screen.addch(row_id + 1, col_id + 1, " ")

    def run(self) -> None:
        stdscr = curses.initscr()
        curses.noecho()
        stdscr.clear()
        stdscr.refresh()
        screen = curses.newwin(self.life.rows + 2, self.life.cols + 2)
        self.draw_borders(screen)
        screen.timeout(1)
        screen.nodelay(True)

        running = True
        paused = False
        while running:
            char = screen.getch()
            if char == ord(" "):
                paused = bool(paused ^ 1)
            elif char == 19:  # ord for ^S == 19
                self.life.save(self.save_path)
            if not paused:
                self.draw_grid(screen)
                screen.refresh()
                self.life.step()

                time.sleep(self.speed)

        curses.endwin()
