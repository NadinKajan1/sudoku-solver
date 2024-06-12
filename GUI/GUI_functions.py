from src import *
import pygame
import sys
from game_state import game_state

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

# Strike Symbol for when user enters invalid input
strike_symbol = pygame.image.load("strike_symbol.jpg")
strike_symbol = pygame.transform.scale(strike_symbol, (30,30))

# Game over text for when user enters 3 invalid inputs
game_over_font = pygame.font.SysFont(None, 72) # Game over message
game_over_text = game_over_font.render("Game Over", True, red)
text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))

# Restart button text
restart_text_surface = font.render("Restart", True, black)
restart_rect = restart_text_surface.get_rect(center=(270, 325))

# Solve button text
solve_text_surface = font.render("Solve", True, black)
solve_text_rect = solve_text_surface.get_rect(center=(270,590))

# Timer text
timer_text_surface = font.render("Timer:", True, black)
timer_text_rect = timer_text_surface.get_rect(center=(370,590))

# Timer variables
timer = 0
clock = pygame.time.Clock()
clock_paused = False # Flag to stop timer when game is over

# Drawing game board
def draw_grid():
    for i in range(grid_size + 1):
        line_width = 1 if i % 3 != 0 else 3
        pygame.draw.line(screen, black, (i * cell_size, 0), (i * cell_size, screen_height), line_width)
        pygame.draw.line(screen, black, (0, i * cell_size), (screen_width, i * cell_size), line_width)
    pygame.draw.line(screen, black, (0,540), (540,540), 3) # Additional bottom line to separate stat bar
    screen.blit(timer_text_surface, timer_text_rect) # Adding the word "Timer:" in the stat bar

    # Solve button
    pygame.draw.rect(screen, white, (220,565,100,50))
    pygame.draw.rect(screen, black, (220, 565, 100, 50),2)
    screen.blit(solve_text_surface, solve_text_rect)

#pygame.draw.rect(screen, white, (170,300,200,50))

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

                if not is_valid(board, num, cell): # Increments strikes for every invalid input
                    game_state.strikes += 1

        # User deleting an input
        elif event.key == pygame.K_DELETE:
            if not initial_board[row][col]:
                board[row][col] = 0
                pygame.draw.rect(screen, (255, 255, 255), (col * cell_size, row * cell_size, cell_size, cell_size))

# Checks for 3 strikes, presents restart button
def game_over_check():
    global clock_paused
    if game_state.strikes == 3:
        clock_paused = True
        screen.blit(game_over_text, text_rect) # Display game over text

        # Drawing restart button
        pygame.draw.rect(screen, white, (170,300,200,50))
        pygame.draw.rect(screen, black, (170, 300, 200, 50),2)
        screen.blit(restart_text_surface, restart_rect)


# Checks if user clicks the restart button
def restart_clicked(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if (mouse_x <= 370 and mouse_x >= 170) and (mouse_y <= 350 and mouse_y >= 300): # If the user clicks the restart button
            reset_game()

# Resets strikes to 0, removes all user inputs, resets the time
def reset_game():
    global board, selected_cell, clock_paused, timer, clock

    # Reset the board to the initial state
    board[:] = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    # Resetting game variables to original values
    game_state.strikes = 0
    selected_cell = None
    clock_paused = False
    timer = 0
    clock = pygame.time.Clock()

    # Clear the screen
    screen.fill(white)
    draw_grid()
    draw_numbers(board)
    pygame.display.update()

# Display time found in main loop
def display_time(time):
    # Formatting time into a displayable format
    minutes = time // 60
    seconds = time % 60
    time_str = '{:02d}:{:02d}'.format(int(minutes), int(seconds))

    timer_surface = font.render(time_str, True, black)
    timer_rect = timer_surface.get_rect(center=(470, 590))
    screen.blit(timer_surface, timer_rect)

# Calculate elapsed time
def timer_function():
    global timer, clock, clock_paused
    if not clock_paused:
        milliseconds = clock.tick(60)
        timer += milliseconds / 1000
        display_time(int(timer))

def solve_clicked(event):
    global clock_paused, timer
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x <= 320 and mouse_x >= 220 and mouse_y <= 615 and mouse_y >= 565:
            board[:] = [
                [7, 8, 0, 4, 0, 0, 1, 2, 0],
                [6, 0, 0, 0, 7, 5, 0, 0, 9],
                [0, 0, 0, 6, 0, 1, 0, 7, 8],
                [0, 0, 7, 0, 4, 0, 2, 6, 0],
                [0, 0, 1, 0, 5, 0, 9, 3, 0],
                [9, 0, 4, 0, 6, 0, 0, 0, 5],
                [0, 7, 0, 3, 0, 0, 0, 1, 2],
                [1, 2, 0, 0, 0, 7, 4, 0, 0],
                [0, 4, 9, 2, 0, 6, 0, 0, 7]
            ]
            print("SOLVING")
            solve(board)
            print_board(board)