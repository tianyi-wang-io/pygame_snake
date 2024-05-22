import unittest
from snake.pathfind import create_matrix, remove_obstacles, add_obstacles, bfs


class TestBFS(unittest.TestCase):

    def test_create_matrix(self):
        m, n = 5, 5
        expected_matrix = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.assertEqual(create_matrix(m, n), expected_matrix)

    def test_add_obstacles(self):
        m, n = 5, 5
        obstacles = [(1, 2), (2, 2), (3, 2)]
        matrix = create_matrix(m, n)
        add_obstacles(matrix, obstacles)
        expected_matrix = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.assertEqual(matrix, expected_matrix)

    def test_remove_obstacles(self):
        m, n = 5, 5
        obstacles = [(1, 2), (2, 2), (3, 2)]
        matrix = create_matrix(m, n)
        add_obstacles(matrix, obstacles)
        remove_obstacles(matrix, obstacles)
        expected_matrix = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.assertEqual(matrix, expected_matrix)

    def test_bfs_no_obstacles(self):
        m, n = 5, 5
        matrix = create_matrix(m, n)
        start = (0, 0)
        goal = (4, 4)
        expected_path = [(1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
        self.assertEqual(bfs(m, n, matrix, start, goal), expected_path)

    def test_bfs_with_obstacles(self):
        m, n = 5, 5
        matrix = create_matrix(m, n)
        obstacles = [(0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3)]
        add_obstacles(matrix, obstacles)
        start = (0, 0)
        goal = (4, 4)
        # A valid path that avoids the obstacles
        expected_path = [
            (1, 0), (2, 0), (3, 0), (4, 0),
            (4, 1), (4, 2), (4, 3), (4, 4)
        ]
        result_path = bfs(m, n, matrix, start, goal)
        self.assertEqual(result_path, expected_path)

    def test_bfs_no_path(self):
        m, n = 5, 5
        matrix = create_matrix(m, n)
        obstacles = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]
        add_obstacles(matrix, obstacles)
        start = (0, 0)
        goal = (4, 4)
        expected_path = []
        self.assertEqual(bfs(m, n, matrix, start, goal), expected_path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
