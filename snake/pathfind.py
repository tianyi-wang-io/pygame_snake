from collections import deque
from typing import Tuple, List


def create_matrix(m: int, n: int) -> List[List[int]]:
    matrix = [[0 for _ in range(n)] for _ in range(m)]
    return matrix


def remove_obstacles(matrix: List[List[int]], obstacles: List[Tuple[int, int]]) -> None:
    for i, j in obstacles:
        matrix[i][j] = 0


def add_obstacles(matrix: List[List[int]], obstacles: List[Tuple[int, int]]) -> None:
    for i, j in obstacles:
        matrix[i][j] = 1


def bfs(m: int, n: int, matrix: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    def next_move(x, y):
        for move_x, move_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_x, next_y = x + move_x, y + move_y
            if (next_x, next_y) in visited:
                continue
            if not 0 <= next_x < m or not 0 <= next_y < n:
                continue
            if matrix[next_x][next_y] == 1:
                continue
            yield next_x, next_y

    queue = deque([start])
    visited = {start}
    came_from = {}
    while queue:
        i, j = queue.popleft()
        if (i, j) == goal:
            path = []
            while (i, j) != start:
                path.append((i, j))
                i, j = came_from[(i, j)]
            return path[::-1]
        for next_i, next_j in next_move(i, j):
            queue.append((next_i, next_j))
            visited.add((next_i, next_j))
            came_from[(next_i, next_j)] = (i, j)
    return []
