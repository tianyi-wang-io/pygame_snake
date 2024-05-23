import heapq
from collections import deque
from typing import Tuple, List


def mahatma_distance(x: Tuple[int, int], y: Tuple[int, int]) -> int:
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def next_move(x, y):
    for move_x, move_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        next_x, next_y = x + move_x, y + move_y
        yield next_x, next_y


def construct_path(came_from: dict, start: Tuple[int, int], goal: Tuple[int, int], reverse=False) -> List[Tuple[int, int]]:
    path = []
    while goal != start:
        path.append(goal)
        goal = came_from[goal]
    if reverse:
        path.reverse()
    return path


def bfs(m: int, n: int, matrix: List[List[int]],
        start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    queue = deque([start])
    came_from = {start: start}
    while queue:
        i, j = queue.popleft()
        if (i, j) == goal:
            return construct_path(came_from, start, goal)
        for next_i, next_j in next_move(i, j):
            if (not 0 <= next_i < m
                or not 0 <= next_j < n
                or matrix[next_i][next_j] == 1
                or (next_i, next_j) in came_from
            ):
                continue
            queue.append((next_i, next_j))
            came_from[(next_i, next_j)] = (i, j)
    return []


def bfs_with_heuristic(m: int, n: int, matrix: List[List[int]],
                       start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    queue = [(mahatma_distance(start, goal), start)]
    came_from = {start: start}
    while queue:
        distance, (i, j) = heapq.heappop(queue)
        if (i, j) == goal:
            return construct_path(came_from, start, goal)
        for next_i, next_j in next_move(i, j):
            if (not 0 <= next_i < m
                or not 0 <= next_j < n
                or matrix[next_i][next_j] == 1
                or (next_i, next_j) in came_from
            ):
                continue
            heapq.heappush(queue, (mahatma_distance((next_i, next_j), goal), (next_i, next_j)))
            came_from[(next_i, next_j)] = (i, j)
    return []


# TODO: implement dijkstra algorithm
def dijkstra(m: int, n: int, matrix: List[List[int]],
             start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    pass


# TODO: implement A* algorithm
def astart(m: int, n: int, matrix: List[List[int]],
           start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    pass


def path_finder_algorithm(algorithm, m, n, matrix, start, goal):
    functions = {
        "bfs": bfs,
        "bfs_with_heuristic": bfs_with_heuristic,
    }
    if algorithm in functions:
        return functions[algorithm](m, n, matrix, start, goal)
    else:
        raise ValueError(f"Algorithm: {algorithm} not found.")
