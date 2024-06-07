from src import *
from GUI_functions import *
import pygame
import time
import sys

selected_cell = None # Initializing variable to track selected cell
input_given = None


# Game loop to handle user inputs & updates to the UI
while True:
    # Handling events
    for event in pygame.event.get():
        quit_game(event) # User exits game

        cell = select_cell(event) # If a user clicks on a cell
        if cell is not None:
            if cell == selected_cell: # If the user clicks the same cell twice, toggle the highlight
                selected_cell = None
            else:
                selected_cell = cell
                row = selected_cell[0]
                col = selected_cell[1]

        user_input(event, selected_cell, board)

    screen.fill(white)
    draw_grid()
    draw_numbers(board)

    # Highlighting selected cell
    if selected_cell is not None and (board[row][col] == 0 or initial_board[row][col]): # If the user clicks on an empty cell or a cell with a given number
        pygame.draw.rect(screen, blue,
                         (col * cell_size, row * cell_size, cell_size, cell_size),
                         width=2)

    elif selected_cell is not None and board[row][col] != 0 and initial_board[row][col] == False: # If the selected cell has a user input
        if is_valid(board,board[row][col],selected_cell): # Valid highlights green
            pygame.draw.rect(screen, green,
                             (col * cell_size, row * cell_size, cell_size, cell_size),
                             width=2)
        else:
            pygame.draw.rect(screen, red, # Invalid highlights red
                             (col * cell_size, row * cell_size, cell_size, cell_size),
                             width=2)
    pygame.display.update()