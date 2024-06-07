import unittest
from src import solve

class TestSudokuSolver(unittest.TestCase):
    def test_solve_sudoku(self):
        board = [
            [0, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 0]
        ]
        solution_exists = solve(board)
        self.assertTrue(solution_exists)
        self.assertEqual(board[0][0], 5) # Checks first element
        self.assertEqual(board[8][8], 9) # Checks last element

        # Checking random elements
        self.assertEqual(board[8][0], 3)
        self.assertEqual(board[7][2], 7)
        self.assertEqual(board[4][6], 7)

        # Checking given elements
        self.assertEqual(board[6][1], 6)
        self.assertEqual(board[4][3], 8)

if __name__ == "__main__":
    unittest.main()