from .utils import find_empty, print_board
def is_valid(board, num, pos):
    """
    Checks if the current board is valid.

    Args:
        board (list of list of int): 9x9 Sudoku board
        pos (tuple of int): row and column position of num
        num (int): Number being inputted to the board

    Returns:
        bool: True if number is valid, False otherwise
    """

    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check 3x3 grid
    # [(0,0) , (0,1) , (0,2)],
    # [(1,0) , (1,1) , (1,2)],
    # [(2,0) , (2,1) , (2,2)]
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x *3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False

    return True

def solve(board):
    """
    Solves the Sudoku board by finding an empty cell, inserting a number, checking the validity,
        and repeating. If validity is ever false, will perform backtracking.

    Args:
        board (list of list of int): 9x9 Sudoku board

    Returns:

    """

    # Returns true once there are no empty cells
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    # Adds number (1-9) to empty cells
    for i in range(1, 10):
        if is_valid(board, i, (row,col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False