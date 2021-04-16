import pygame
from constants import *
from spot import Spot


class Grid:
    def __init__(self, cell_size, nb_rows, nb_cols):
        self.cell_size = cell_size
        self.nb_rows = nb_rows
        self.nb_cols = nb_cols
        self.total_width = self.nb_cols * self.cell_size
        self.total_height = self.nb_rows * self.cell_size
        self.grid = self._create_grid()
        self.starting_point = None
        self.ending_point = None
        self.barrier_points = []

    def _create_grid(self):
        my_grid = []
        for i in range(self.nb_rows):
            my_grid.append([])
            for j in range(self.nb_cols):
                spot = Spot(i, j, self.cell_size)
                my_grid[i].append(spot)
        return my_grid

    def print_grid(self):
        for i in range(self.nb_rows):
            print(self.grid[i])

    def _draw_grid(self, win):
        for i in range(self.nb_rows + 1):
            line_start = (0, i * self.cell_size)
            line_end = (self.total_width, i * self.cell_size)
            pygame.draw.line(win, GREY, line_start, line_end)
        for j in range(self.nb_cols + 1):
            line_start = (j * self.cell_size, 0)
            line_end = (j * self.cell_size, self.total_height)
            pygame.draw.line(win, GREY, line_start, line_end)

    def _draw_spots(self, win):
        for row in self.grid:
            for spot in row:
                spot.draw(win)

    def draw(self, win):
        self._draw_spots(win)
        self._draw_grid(win)

    def get_clicked_pos(self, pos):
        x, y = pos
        row = y // self.cell_size
        col = x // self.cell_size
        return row, col

    def is_clicked_inside(self, pos):
        x, y = pos
        return x < self.total_width and y < self.total_height

    def update_neighbors_grid(self):
        # print("update_neighbors_grid")
        for row in self.grid:
            for spot in row:
                self.update_neighbors_cell(spot)

    def update_neighbors_cell(self, spot: Spot):
        row = spot.row
        col = spot.col
        if row + 1 < self.nb_rows:
            spot_to_add = self.grid[row + 1][col]
            self.grid[row][col].add_neighbor(spot_to_add)
        if row - 1 >= 0:
            spot_to_add = self.grid[row - 1][col]
            self.grid[row][col].add_neighbor(spot_to_add)
        if col + 1 < self.nb_cols:
            spot_to_add = self.grid[row][col + 1]
            self.grid[row][col].add_neighbor(spot_to_add)
        if col - 1 >= 0:
            spot_to_add = self.grid[row][col - 1]
            self.grid[row][col].add_neighbor(spot_to_add)

    def clear(self):
        self.starting_point = None
        self.ending_point = None
        self.barrier_points = []
        for row in self.grid:
            for spot in row:
                spot.clear()

    def soft_clear(self):
        for row in self.grid:
            for spot in row:
                spot.soft_clear()


if __name__ == "__main__":
    # pass
    grid = Grid(5, 3, 6)
    # print(grid.grid)
    grid.print_grid()
    # grid.read_matrix()
