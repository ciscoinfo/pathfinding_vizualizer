import queue
from collections import deque
import random
import pygame
from spot import Spot, State


def h(p1, p2):
    # heuristic
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


def reconstruct_path(came_from, current, start, fn_draw):
    count = 0
    while current in came_from:
        count += 1
        current = came_from[current]
        if current != start:
            current.set_state(State.PATH)
        fn_draw()
    print(f"path length = {count}")
    return count


def dfs(fn_draw, starting_node: Spot, ending_node: Spot):
    stack = deque()
    visited = []

    stack.append(starting_node)
    while stack:

        current_node = stack.pop()
        # visited
        visited.append(current_node)

        if current_node == ending_node:
            return len(visited)

        if current_node != starting_node:
            current_node.set_state(State.PATH)
            fn_draw()

        # looking_for_neighbors and adding to the stack
        for neighbor in current_node.neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
    return False


def bfs(fn_draw, starting_node: Spot, ending_node: Spot):
    stack = deque()
    visited = []

    stack.append(starting_node)
    while stack:

        current_node = stack.popleft()
        visited.append(current_node)

        if current_node == ending_node:
            return len(visited)

        if current_node != starting_node:
            current_node.set_state(State.PATH)
            fn_draw()

        # looking_for_neighbors and adding to the stack
        for neighbor in current_node.neighbors:
            if neighbor not in visited and neighbor not in stack:
                stack.append(neighbor)
    return False


def try_random_path(starting_node: Spot, ending_node: Spot):
    visited = []
    running = True
    current_node = starting_node
    while running:
        if current_node == ending_node:
            # print("gagné")
            return visited
        else:
            valid_neighbors = [x for x in current_node.neighbors if x not in visited]
            if not valid_neighbors:
                # print("plus de chemin")
                return False
            else:
                current_node = random.choice(valid_neighbors)
                # current_node.set_state(State.PATH)
                visited.append(current_node)
    # print("terminé")


def find_random_path(fn_draw, starting_node: Spot, ending_node: Spot):

    path_found = False
    counter = 0
    while not path_found:
        path_found = try_random_path(starting_node, ending_node)
        counter += 1
    # found
    # print(f"nombre d'essais = {counter}")
    for node in path_found:
        if node not in [starting_node, ending_node]:
            node.set_state(State.PATH)
            fn_draw()
    return len(path_found)


def a_star(fn_draw, grid, start, end):
    count = 0
    open_set = queue.PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    # dictionnary init with all spot to infinite
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        # the node
        open_set_hash.remove(current)

        if current == end:
            # we find the shortest path
            count = reconstruct_path(came_from, end, start, fn_draw)
            end.set_state(State.END)
            return count

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_state(State.OPEN)
        fn_draw()
        # pygame.time.delay(50)
        if current != start:
            current.set_state(State.CLOSED)

    return False
