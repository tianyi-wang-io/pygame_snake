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


def generate_fixed_obstacle(m: int, n: int, size: int, start: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = start
    rows = m // size
    cols = n // size
    one = [(rows, i) for i in range(cols, cols * 2)]
    two = [(i, cols * 2) for i in range(rows, rows * 2)]
    three = [(rows * 2, i) for i in range(cols * 2, cols-1, -1)]
    obstacles = one + two + three
    obstacles = [(i + x, j + y) for i, j in obstacles]
    return obstacles
