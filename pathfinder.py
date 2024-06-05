import heapq
from collections import deque
from typing import Tuple, List


def mahatma_distance(x: Tuple[int, int], y: Tuple[int, int]) -> int:
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def next_move(x, y):
    for move_x, move_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        next_x, next_y = x + move_x, y + move_y
        yield next_x, next_y


def construct_path(came_from: dict, start: Tuple[int, int], goal: Tuple[int, int],
                   reverse=False) -> List[Tuple[int, int]]:
    path = []
    while goal != start:
        path.append(goal)
        goal = came_from[goal]
    if reverse:
        path.reverse()
    return path


def bfs(m: int, n: int, matrix: List[List[int]],
        start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], int]:
    queue = deque([start])
    came_from = {start: start}
    step_count = 0
    while queue:
        step_count += 1
        i, j = queue.popleft()
        if (i, j) == goal:
            return construct_path(came_from, start, goal), step_count
        for next_i, next_j in next_move(i, j):
            if (not 0 <= next_i < m
                    or not 0 <= next_j < n
                    or matrix[next_i][next_j] == 1
                    or (next_i, next_j) in came_from):
                continue
            queue.append((next_i, next_j))
            came_from[(next_i, next_j)] = (i, j)
    return [], step_count


def bfs_with_heuristic(m: int, n: int, matrix: List[List[int]],
                       start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], int]:
    queue = [(mahatma_distance(start, goal), start)]
    came_from = {start: start}
    step_count = 0
    while queue:
        step_count += 1
        distance, (i, j) = heapq.heappop(queue)
        if (i, j) == goal:
            return construct_path(came_from, start, goal), step_count
        for next_i, next_j in next_move(i, j):
            if (not 0 <= next_i < m
                    or not 0 <= next_j < n
                    or matrix[next_i][next_j] == 1
                    or (next_i, next_j) in came_from):
                continue
            heapq.heappush(queue, (mahatma_distance((next_i, next_j), goal), (next_i, next_j)))
            came_from[(next_i, next_j)] = (i, j)
    return [], step_count


def dijkstra(m: int, n: int, matrix: List[List[int]],
             start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], int]:
    distances = {(i, j): float('inf') for i in range(m) for j in range(n)}
    distances[start] = 0
    came_from = {start: start}
    queue = [(0, start)]
    step_count = 0
    while queue:
        step_count += 1
        distance, curr = heapq.heappop(queue)
        if curr == goal:
            return construct_path(came_from, start, goal), step_count
        if distance > distances[curr]:
            continue
        for neighbor in next_move(curr[0], curr[1]):
            if not 0 <= neighbor[0] < m or not 0 <= neighbor[1] < n or matrix[neighbor[0]][neighbor[1]] == 1:
                continue
            neighbor_distance = distance + 1
            if neighbor_distance < distances[neighbor]:
                distances[neighbor] = neighbor_distance
                came_from[neighbor] = curr
                heapq.heappush(queue, (neighbor_distance, neighbor))
    return [], step_count


# TODO: This implementation seems incorrect
def astar(m: int, n: int, matrix: List[List[int]],
          start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], int]:
    queue = [(0, start)]
    queue_hash = {start}
    came_from = {start: start}
    g_score = {start: 0}
    step_count = 0
    while queue:
        step_count += 1
        curr_g_score, (i, j) = heapq.heappop(queue)
        queue_hash.remove((i, j))
        if (i, j) == goal:
            return construct_path(came_from, start, goal), step_count
        for next_i, next_j in next_move(i, j):
            neighbor = (next_i, next_j)
            if (not 0 <= next_i < m
                    or not 0 <= next_j < n
                    or matrix[next_i][next_j] == 1):
                continue
            curr_g_score += 1
            if neighbor not in g_score or curr_g_score < g_score[neighbor]:
                g_score[neighbor] = curr_g_score
                f_score = curr_g_score + mahatma_distance(neighbor, goal)
                came_from[neighbor] = (i, j)
                if neighbor not in queue_hash:
                    heapq.heappush(queue, (curr_g_score + f_score, (next_i, next_j)))
                    queue_hash.add(neighbor)
    return [], step_count


def path_finder_algorithm(algorithm, m, n, matrix, start, goal):
    functions = {
        'bfs': bfs,
        'bfs_with_heuristic': bfs_with_heuristic,
        'astar': astar,
        'dijkstra': dijkstra
    }
    if algorithm in functions:
        return functions[algorithm](m, n, matrix, start, goal)
    else:
        raise ValueError(f'{algorithm.capitalize()}, key not found.')
