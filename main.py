import sys
import pygame
import random
import time
from collections import deque
from enum import Enum
from typing import List, Tuple, Iterable
from matrix import create_matrix, add_obstacles, remove_obstacles, generate_fixed_obstacle
from pathfinder import path_finder_algorithm


FPS = 10
BLOCK_SIZE = 10
SIDE_PANEL_SIZE = 200
WIDTH = 640
HEIGHT = 480
INITIAL_SNAKE_SIZE = 3
# PATHFIND_ALGORITHM = 'bfs'
# PATHFIND_ALGORITHM = 'bfs_with_heuristic'
# PATHFIND_ALGORITHM = 'astar'
PATHFIND_ALGORITHM = 'dijkstra'


def shrink_coordinates(positions: Iterable[Tuple[int, int]], width_first=True) -> List[Tuple[int, int]]:
    if width_first:
        return [(y // BLOCK_SIZE, x // BLOCK_SIZE) for (x, y) in positions]
    else:
        return [(x // BLOCK_SIZE, y // BLOCK_SIZE) for (x, y) in positions]


def enlarge_coordinates(positions: Iterable[Tuple[int, int]], width_first=True) -> List[Tuple[int, int]]:
    if width_first:
        return [(y * BLOCK_SIZE, x * BLOCK_SIZE) for (x, y) in positions]
    else:
        return [(x * BLOCK_SIZE, y * BLOCK_SIZE) for (x, y) in positions]


class Colors:
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 69, 0)
    ORANGE = pygame.Color(255, 165, 0)
    BLUE = pygame.Color(173, 216, 230, 20)


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    @staticmethod
    def is_opposite_direction(prev, curr) -> bool:
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposites[curr] == prev


class Food:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.position = [(0, 0)]
        self.generate_random_food()

    def generate_random_food(self):
        x = random.randrange(self.width // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randrange(self.height // BLOCK_SIZE) * BLOCK_SIZE
        self.position = [(x, y)]


class PathFinder:
    def __init__(self, width: int, height: int, obstacles: Iterable[Tuple[int, int]]):
        self.x = width // BLOCK_SIZE
        self.y = height // BLOCK_SIZE
        self.matrix = create_matrix(self.y, self.x)
        if obstacles:
            self.add_obstacle(obstacles)
        self.path = []
        self.step_count = 0

    def add_obstacle(self, obstacles: List[Tuple[int, int]]) -> None:
        add_obstacles(self.matrix, obstacles)

    def remove_obstacle(self, obstacles: List[Tuple[int, int]]) -> None:
        remove_obstacles(self.matrix, obstacles)

    def find_path(self, start, goal, obstacles) -> None:
        start = start[1] // BLOCK_SIZE, start[0] // BLOCK_SIZE  # row, col
        goal = goal[1] // BLOCK_SIZE, goal[0] // BLOCK_SIZE
        shrank_obstacles = shrink_coordinates(obstacles, width_first=True)
        self.add_obstacle(shrank_obstacles)
        path, self.step_count = path_finder_algorithm(PATHFIND_ALGORITHM, self.y, self.x, self.matrix, start, goal)
        self.remove_obstacle(shrank_obstacles)
        self.path = enlarge_coordinates(path, width_first=True)


class Snake:
    def __init__(self, width, height, size):
        self.head = (width // 2, height // 2 - BLOCK_SIZE)
        self.body = deque()
        self.tail = self.head
        self.body_set = set()  # exclude snake head
        self.direction = Direction.UP
        self.prev_direction = Direction.UP
        self.init_snake(size)

    def init_snake(self, size):
        for i in range(size):
            position = (self.head[0], self.head[1] + i * BLOCK_SIZE)
            self.body.append(position)
            self.body_set.add(position)
            self.tail = position
        self.body_set.remove(self.head)

    def grow(self, direction: Direction) -> None:
        if Direction.is_opposite_direction(self.prev_direction, direction):
            direction = self.prev_direction

        if direction == Direction.UP:
            new_head = (self.head[0], self.head[1] - BLOCK_SIZE)
        elif direction == Direction.DOWN:
            new_head = (self.head[0], self.head[1] + BLOCK_SIZE)
        elif direction == Direction.LEFT:
            new_head = (self.head[0] - BLOCK_SIZE, self.head[1])
        else:
            new_head = (self.head[0] + BLOCK_SIZE, self.head[1])

        self.body_set.add(self.head)
        self.head = new_head
        self.body.appendleft(self.head)
        self.tail = self.body.pop()
        self.body_set.remove(self.tail)
        self.prev_direction = direction

    def eat(self, food_position: Tuple[int, int]) -> bool:
        if self.head == food_position:
            self.body.append(self.tail)
            self.body_set.add(self.tail)
            return True
        else:
            return False


class App:
    def __init__(self, width, height):
        self._running = True
        self._start = False
        self._game_window = None
        self.display_size = (WIDTH + SIDE_PANEL_SIZE, HEIGHT)
        self.game_display_size = (width, height)
        self.obstacles = set()
        self.add_obstacle(start=(2, 2), size=3)
        self.snake = Snake(width, height, INITIAL_SNAKE_SIZE)
        self.food = Food(width, height)
        self.pathfinder = PathFinder(width, height, self.obstacles)
        self.direction = Direction.UP
        self.score = 0

    def update_food_position(self):
        self.food.generate_random_food()
        while self.food.position[0] in self.obstacles:
            self.food.generate_random_food()

    def side_panel(self):
        side_panel_size = (SIDE_PANEL_SIZE, HEIGHT)
        side_panel = pygame.Surface(side_panel_size)
        side_panel.fill(Colors.WHITE)

        # render text
        font = pygame.font.SysFont(None, 22)
        text_to_render = [
            f'Game Status: {"Pause" if not self._start else "Start"}',
            f'Score: {self.score}',
            f'Path Algorithm: {PATHFIND_ALGORITHM.capitalize()}',
            f'Algorithm grid explored: ',
            f'{self.pathfinder.step_count} / {WIDTH // BLOCK_SIZE * HEIGHT // BLOCK_SIZE}',
        ]

        y_offset = 20
        for text in text_to_render:
            text_surface = font.render(text, True, Colors.BLACK)
            side_panel.blit(text_surface, (10, y_offset))
            y_offset += 60

        self._game_window.blit(side_panel, (WIDTH, 0))

    def game_over(self):
        self._running = False
        time.sleep(3)
        pygame.quit()
        sys.exit(0)

    def is_game_over(self):
        x, y = self.snake.head[0], self.snake.head[1]
        if (x < 0
                or y < 0
                or x >= self.game_display_size[0]
                or y >= self.game_display_size[1]
                or (x, y) in self.get_obstacles_draw_position()):
            print('game over')
            self.game_over()

    def add_obstacle(self, start, size) -> None:
        obstacle = generate_fixed_obstacle(HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE, size, start)
        for position in obstacle:
            self.obstacles.add(position)

    def get_obstacles_draw_position(self):
        return enlarge_coordinates(self.obstacles)

    def draw(self, coordinates: Iterable[Tuple[int, int]], color, **kwargs):
        for x, y in coordinates:
            pixels = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self._game_window, color, pixels, **kwargs)

    def game_event_handler(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                self.direction = Direction.DOWN
            elif event.key == pygame.K_LEFT:
                self.direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                self.direction = Direction.RIGHT
            # Space
            elif event.key == pygame.K_SPACE:
                self._start = self._start is False
            # Esc
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def game_initializer(self):
        passes, fails = pygame.init()
        if fails > 0:
            print(f'{fails} fails.')
        else:
            print('Game initiated.')
        pygame.display.set_caption('Snake')
        self._game_window = pygame.display.set_mode(self.display_size, pygame.SCALED)
        self._game_window.fill(Colors.BLACK)
        self._running = True

    def game_state_update(self):
        if self._start:
            self.snake.grow(self.direction)
            if self.snake.eat(self.food.position[0]):
                self.score += 1
                self.update_food_position()
                self.pathfinder.find_path(self.snake.head, self.food.position[0], self.snake.body_set | self.obstacles)
        self.draw(self.pathfinder.path, Colors.BLUE, border_radius=1)
        self.draw(self.snake.body, Colors.WHITE, border_radius=3)
        self.draw(self.food.position, Colors.RED)
        self.draw(self.get_obstacles_draw_position(), Colors.ORANGE)
        self.side_panel()
        pygame.display.update()
        self.is_game_over()

    def game_execute(self):
        try:
            self.game_initializer()
        except Exception as e:
            print(e)

        clock = pygame.time.Clock()
        self.pathfinder.find_path(self.snake.head, self.food.position[0], self.snake.body_set | self.obstacles)
        while self._running:
            self._game_window.fill(Colors.BLACK)
            for event in pygame.event.get():
                self.game_event_handler(event)
            self.game_state_update()
            clock.tick(FPS)


def main():
    app = App(WIDTH, HEIGHT)
    app.game_execute()


if __name__ == '__main__':
    main()
