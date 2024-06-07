def find_empty(board):
    """
    Find the first empty cell in the Soduko board.

    Args:
        board (list of list of int): 9x9 Sudoku board where empty cells are represented as 0.

    Returns:
        tuple: A tuple (i, j) representing row & column indices of the first empty cell.
               Returns None if no empty cell is found.
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0: # Check if cell is empty
                return (i,j) # row, col

    return None

def print_board(board):
    """
    Prints the Sudoku board into he output terminal in a displayable format.

    Args:
        board (list of list of int): 9x9 Sudoku board where empty cells are represented as 0.

    Returns:
        None.
    """
    # Prints horizontal lines
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - -")

        # Prints vertical lines
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")
    print("") # Space to separate multiple boards