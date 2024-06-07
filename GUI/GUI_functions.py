from src import *
import pygame
import time
import sys

board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

# list of list of bool to differentiate given values from inputted values
initial_board = [
    [True, True, False, True, False, False, True, True, False],
    [True, False, False, False, True, True, False, False, True],
    [False, False, False, True, False, True, False, True, True],
    [False, False, True, False, True, False, True, True, False],
    [False, False, True, False, True, False, True, True, False],
    [True, False, True, False, True, False, False, False, True],
    [False, True, False, True, False, False, False, True, True],
    [True, True, False, False, False, True, True, False, False],
    [False, True, True, True, False, True, False, False, True]
]

# Initializing game window
pygame.init()
screen_width = 540
screen_height = 540
screen = pygame.display.set_mode((screen_width, 640)) # Set height to 640 to accomodate for stat bar
pygame.display.set_caption("Sudoku Solver")

# Defining colors for ease of use
white = (255,255,255)
black = (0,0,0)
gray = (200,200,200)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
font = pygame.font.SysFont(None, 36)

# Defining grid parameters
grid_size = 9
cell_size = screen_width // grid_size

# Stat bar items
strikes = 0 # Number of times user inputs an invalid number

# Drawing game board
def draw_grid():
    for i in range(grid_size + 1):
        line_width = 1 if i % 3 != 0 else 3
        pygame.draw.line(screen, black, (i * cell_size, 0), (i * cell_size, screen_height), line_width)
        pygame.draw.line(screen, black, (0, i * cell_size), (screen_width, i * cell_size), line_width)
    pygame.draw.line(screen, black, (0,540), (540,540), 3) # Additional bottom line to separate stat bar



# Initializing board with given numbers
def draw_numbers(board):
    for row in range(grid_size):
        for col in range(grid_size):
            if board[row][col] != 0:
                number = font.render(str(board[row][col]), True, black)
                screen.blit(number, (col * cell_size + 20, row * cell_size + 20))

# User exits game
def quit_game(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

# User selects a cell
def select_cell(event):
    """
    Highlights the cell the user clicks on.

    Args:
        event (pygame.event): user click event

    Returns:
        (row, col): position of the selected cell
        None: returns None if the user doesn't click or clicks anywhere other than the grid
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if mouse_y < 540:  # Checking if user clicked within grid & not stat bar
            row = mouse_y // cell_size
            col = mouse_x // cell_size
            pygame.draw.rect(screen, blue,
                             (col * cell_size, row * cell_size, cell_size, cell_size),
                             width=2)
            return row, col
    return None

# User inputs a number
def user_input(event, cell, board):
    """
    Checks if user selected a cell not containing a given number, then inputs a number 1-9 or deletes a previous input,
        then adds that number to the board.

    Args:
        event (pygame.event): user pressing a number 1-9
        cell (row,col): position of the selected cell (None if no cell is selected)
        board (list of list of int): 9x9 Sudoku board

    Returns:
        None
    """
    if event.type == pygame.KEYDOWN and cell is not None: # Checks if cell is selected & user selected a number 1-9
        row, col = cell

        # User adding an input 1-9
        if pygame.K_1 <= event.key <= pygame.K_9:
            if not initial_board[row][col]: # Checks if selected cell has a given number
                num = event.key - 48 # Converts key to corresponding number
                board[row][col] = num

                if is_valid(board, num, cell):
                    print("YAY")
                else:
                    print("BOO")

        # User deleting an input
        elif event.key == pygame.K_DELETE:
            if not initial_board[row][col]:
                board[row][col] = 0
                pygame.draw.rect(screen, (255, 255, 255), (col * cell_size, row * cell_size, cell_size, cell_size))

