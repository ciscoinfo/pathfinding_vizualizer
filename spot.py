import pygame
from constants import *
from enum import Enum


class State(Enum):
    NONE = 0
    START = 1
    END = 2
    OPEN = 3
    CLOSED = 4
    BARRIER = 5
    PATH = 6


class Spot:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.y = row * size
        self.x = col * size
        self.color = WHITE
        self.neighbors = []
        self.state = State.NONE

    def get_pos(self):
        return self.row, self.col

    def set_state(self, state: State):
        if not isinstance(state, State):
            print("ERROR : state doesn't exist")
            return False
        self.state = state
        if state == State.NONE:
            self.color = WHITE
        elif state == State.START:
            self.color = ORANGE
        elif state == State.END:
            self.color = TURQUOISE
        elif state == State.OPEN:
            self.color = GREEN
        elif state == State.CLOSED:
            self.color = RED
        elif state == State.BARRIER:
            self.color = BLACK
        elif state == State.PATH:
            self.color = PURPLE
        else:
            self.color = WHITE

    def is_state(self, state: State):
        return self.state == state

    def get_state(self):
        return self.state

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    # def update_neighbors(self, grid):
    #     if self.row < self.total_rows - 1 and not

    def __lt__(self, other):
        return False

    def add_neighbor(self, spot):
        if not spot.is_state(State.BARRIER):
            self.neighbors.append(spot)
        # else:
        #     print("barrier")

    def color_neighbor(self):
        if not self.is_state(State.BARRIER):
            self.set_state(State.OPEN)

    def decolor(self):
        if not self.is_state(State.BARRIER):
            self.set_state(State.NONE)

    def color_center(self):
        self.set_state(State.PATH)

    def clear(self):
        self.set_state(State.NONE)
        self.neighbors = []

    def soft_clear(self):
        if self.get_state() not in [State.START, State.END, State.BARRIER]:
            self.set_state(State.NONE)
            self.neighbors = []


if __name__ == "__main__":
    new_spot = Spot(1, 1, 1, 1)
    print(new_spot.get_state())
    new_spot.set_state(State.CLOSED)
    print(new_spot.get_state())
    print(new_spot.is_state(State.NONE))
    print(new_spot.is_state(State.CLOSED))
