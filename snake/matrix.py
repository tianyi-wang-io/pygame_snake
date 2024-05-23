import random
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


def generate_random_obstacle(m: int, n: int, size: int) -> Tuple[int, int]:
    pass
