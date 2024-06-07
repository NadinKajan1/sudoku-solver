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

        user_input(event, selected_cell, board)

    screen.fill(white)
    draw_grid()
    draw_numbers(board)

    # Highlighting selected cell
    if selected_cell:
        pygame.draw.rect(screen, (0,0,255), (selected_cell[1] * cell_size, selected_cell[0] * cell_size, cell_size, cell_size), width=2)



    pygame.display.update()