import sys
import pygame
import random
import time
from collections import deque
from enum import Enum
from typing import List, Tuple, Deque
from pathfind import create_matrix, add_obstacles, remove_obstacles, bfs


FPS = 10
BLOCK_SIZE = 10


class Colors:
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
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
        x = random.randrange(0, self.width // BLOCK_SIZE) * 10
        y = random.randrange(0, self.height // BLOCK_SIZE) * 10
        self.position = [(x, y)]


class PathFinder:
    def __init__(self, width, height):
        self.x = width // BLOCK_SIZE
        self.y = height // BLOCK_SIZE
        self.matrix = create_matrix(self.y, self.x)
        self.path = []

    def add_obstacle(self, obstacle) -> None:
        add_obstacles(self.matrix, obstacle)

    def remove_obstacle(self, obstacle) -> None:
        remove_obstacles(self.matrix, obstacle)

    def find_path(self, start, goal) -> None:
        start = start[1] // 10, start[0] // 10  # row, col
        goal = goal[1] // 10, goal[0] // 10
        path = bfs(self.y, self.x, self.matrix, start, goal)
        self.path = [(y * BLOCK_SIZE, x * BLOCK_SIZE) for (x, y) in path]  # (col, row)


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
            pixel = (self.head[0], self.head[1] + i * BLOCK_SIZE)
            self.body.append(pixel)
            self.body_set.add(pixel)
            self.tail = pixel
        self.body_set.remove(self.head)

    def grow(self, direction: Direction) -> None:
        if Direction.is_opposite_direction(self.prev_direction, direction):
            direction = self.prev_direction

        if direction == Direction.UP:
            self.head = (self.head[0], self.head[1] - BLOCK_SIZE)
        elif direction == Direction.DOWN:
            self.head = (self.head[0], self.head[1] + BLOCK_SIZE)
        elif direction == Direction.LEFT:
            self.head = (self.head[0] - BLOCK_SIZE, self.head[1])
        else:
            self.head = (self.head[0] + BLOCK_SIZE, self.head[1])
        self.body.appendleft(self.head)
        self.body_set.add(self.body[1])
        self.prev_direction = direction
        self.body_set.remove(self.body.pop())

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
        self.display_size = (width, height)
        self.snake = Snake(width, height, 3)
        self.food = Food(width, height)
        self.pathfinder = PathFinder(width, height)
        self.direction = Direction.UP
        self.fps = pygame.time.Clock()

    def on_init(self):
        passes, fails = pygame.init()
        if fails > 0:
            print(f'{fails} fails.')
        else:
            print('Game initiated.')
        pygame.display.set_caption('Snake')
        self._game_window = pygame.display.set_mode(self.display_size, pygame.SCALED)
        self._game_window.fill(Colors.BLACK)
        self._running = True

    def game_over(self):
        self._running = False
        time.sleep(3)
        pygame.quit()
        sys.exit()

    def is_game_over(self):
        x, y = self.snake.head[0], self.snake.head[1]
        if x < 0 or y < 0 or x >= self.display_size[0] or y >= self.display_size[1] or (x, y) in self.snake.body_set:
            print('game over')
            self.game_over()

    def on_event(self, event):
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

    def draw(self, coordinates: Deque | List[Tuple[int, int]], color, **kwargs):
        for x, y in coordinates:
            pixels = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self._game_window, color, pixels, **kwargs)

    def on_execute(self):
        try:
            self.on_init()
        except Exception as e:
            print(e)

        while self._running:
            self._game_window.fill(Colors.BLACK)
            for event in pygame.event.get():
                self.on_event(event)
            if not self._start:
                self.pathfinder.find_path(self.snake.head, self.food.position[0])
                self.draw(self.pathfinder.path, Colors.BLUE, border_radius=1)
                self.draw(self.snake.body, Colors.WHITE, border_radius=3)
                self.draw(self.food.position, Colors.RED)
                pygame.display.update()
                continue
            self.snake.grow(self.direction)
            if self.snake.eat(self.food.position[0]):
                self.food.generate_random_food()
                self.pathfinder.find_path(self.snake.head, self.food.position[0])
            self.draw(self.pathfinder.path, Colors.BLUE, border_radius=1)
            self.draw(self.snake.body, Colors.WHITE, border_radius=3)
            self.draw(self.food.position, Colors.RED)
            pygame.display.update()
            self.is_game_over()
            self.fps.tick(FPS)


def main():
    app = App(640, 480)
    app.on_execute()


if __name__ == '__main__':
    main()
