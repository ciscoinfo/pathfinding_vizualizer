import pygame

from algo import *
from button import Button
from constants import *
from grid import Grid
from result import Result
from spot import State


class App:

    def __init__(self):
        self.FPS = 60
        self._running = True
        self.screen = None
        self.grid = Grid(20, 30, 30)
        self.size = self.grid.total_width + 200, self.grid.total_height

        # start point is set
        self.has_start = False

        # end point is set
        self.has_end = False

        # The program has started
        self.started = False

        self.my_buttons = {}
        self.create_buttons()
        self.clock = pygame.time.Clock()
        self._init()

    def _init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pathfinding Algorithms")
        self._running = True

    def main_loop(self):
        while self._running:
            self._handle_input()
            self._process_game_logic()
            self._draw()
            self.clock.tick(self.FPS)
        pygame.quit()

    def create_buttons(self):
        y = 10
        x = self.grid.total_width + 25
        height = 50
        width = 150

        btn_astar = Button(color=COLOR_BT_ALGO_STAR, x=x, y=y, width=width, height=height, text="A *")
        y += height + 10
        btn_dfs = Button(color=COLOR_BT_ALGO_STAR, x=x, y=y, width=width, height=height, text="DFS")
        y += height + 10
        btn_bfs = Button(color=COLOR_BT_ALGO_STAR, x=x, y=y, width=width, height=height, text="BFS")
        y += height + 10
        btn_random = Button(color=COLOR_BT_ALGO_STAR, x=x, y=y, width=width, height=height, text="Random")
        y += height + 50
        btn_clear_all = Button(color=COLOR_BT_CLEAR, x=x, y=y, width=width, height=height, text="Clear all")
        y += height + 10
        btn_clear_path = Button(color=COLOR_BT_CLEAR, x=x, y=y, width=width, height=height, text="Clear path")
        y += height + 50
        self.result = Result(color=WHITE, x=x, y=y, width=width, height=100, text="")

        self.my_buttons["algo_astar"] = btn_astar
        self.my_buttons["algo_dfs"] = btn_dfs
        self.my_buttons["algo_bfs"] = btn_bfs
        self.my_buttons["algo_random"] = btn_random
        self.my_buttons["clear_all"] = btn_clear_all
        self.my_buttons["clear_path"] = btn_clear_path

    def _handle_input(self):

        pos = pygame.mouse.get_pos()
        # position of the mouse

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self._running = False
            if self.started:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, button in self.my_buttons.items():
                    if button.isOver(pos):
                        button.change_color(WHITE)
                        self.btn_action_map(name)

            if event.type == pygame.MOUSEBUTTONUP:
                for button in self.my_buttons.values():
                    if button.isOver(pos): button.change_color(button.initial_color)

            if event.type == pygame.MOUSEMOTION:
                for button in self.my_buttons.values():
                    button.change_color(RED) if button.isOver(pos) else button.change_color(button.initial_color)

            if pygame.mouse.get_pressed(3)[0] and self.grid.is_clicked_inside(pos):
                # prevent click outside the grid
                # LEFT Button
                row, col = self.grid.get_clicked_pos(pos)
                spot = self.grid.grid[row][col]
                if not self.grid.starting_point and spot != self.grid.ending_point:
                    self.grid.starting_point = spot
                    self.grid.starting_point.set_state(State.START)
                elif not self.grid.ending_point and spot != self.grid.starting_point:
                    self.grid.ending_point = spot
                    self.grid.ending_point.set_state(State.END)
                elif spot != self.grid.starting_point and spot != self.grid.ending_point:
                    self.grid.barrier_points.append(spot)
                    spot.set_state(State.BARRIER)
                    self.grid.barrier_points.append(spot)

            elif pygame.mouse.get_pressed(3)[2] and self.grid.is_clicked_inside(pos):
                # print("right button")
                # RIGHT Button
                pos = pygame.mouse.get_pos()
                row, col = self.grid.get_clicked_pos(pos)
                spot = self.grid.grid[row][col]
                if self.grid.starting_point == spot:
                    self.grid.starting_point = None
                elif self.grid.ending_point == spot:
                    self.grid.ending_point = None
                elif spot in self.grid.barrier_points:
                    self.grid.barrier_points.remove(spot)
                spot.set_state(State.NONE)

    def btn_action_map(self, argument):
        switcher = {
            "algo_astar": self.algo_alstar,
            "algo_dfs": self.algo_dfs,
            "algo_bfs": self.algo_bfs,
            "algo_random": self.algo_random,
            "clear_all": self.grid.clear,
            "clear_path": self.grid.soft_clear,
        }
        func = switcher.get(argument, lambda: "Invalid argument")
        # Execute the function
        func()

    def algo_starter(self):
        self.grid.soft_clear()
        self.grid.update_neighbors_grid()
        self.result.set_text_start()

    def algo_alstar(self):
        if self.grid.starting_point and self.grid.ending_point:
            self.algo_starter()
            result = a_star(lambda: self._draw(), self.grid.grid, self.grid.starting_point, self.grid.ending_point)
            if result:
                self.result.set_text_result(result)

    def algo_dfs(self):
        if self.grid.starting_point and self.grid.ending_point:
            self.algo_starter()
            result = dfs(lambda: self._draw(), self.grid.starting_point, self.grid.ending_point)
            if result:
                self.result.set_text_result(result)

    def algo_bfs(self):
        if self.grid.starting_point and self.grid.ending_point:
            self.algo_starter()
            result = bfs(lambda: self._draw(), self.grid.starting_point, self.grid.ending_point)
            if result:
                self.result.set_text_result(result)

    def algo_random(self):
        if self.grid.starting_point and self.grid.ending_point:
            self.algo_starter()
            result = find_random_path(lambda: self._draw(), self.grid.starting_point, self.grid.ending_point)
            if result:
                self.result.set_text_result(result)

    def _process_game_logic(self):
        pass

    def _draw(self):
        self.screen.fill(WHITE)

        self.grid.draw(self.screen)
        self.draw_buttons()
        pygame.display.flip()

    def draw_buttons(self):
        for button in self.my_buttons.values():
            button.draw(self.screen, outline=BLACK)
        self.result.draw(self.screen)

    def run(self):
        # if self._init() == False:
        #     self._running = False
        self.main_loop()


if __name__ == "__main__":
    my_app = App()
    my_app.run()
