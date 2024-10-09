import random 

# Define ship types and sizes of ships 
SHIP_SIZES = {
    "Carrier": 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2
}

# Helper function to create an empty 10x10 grid
def create_grid():
    return [[" " for _ in range(10)] for _ in range(10)]

# Display a grid with labels for rows and columns 
def display_grid(grid, hide_ships=False):
    print("  " + " ".join(str(i) for i in range(10)))
    for idx, row in enumerate(grid):
        row_display = [" " if hide_ships and cell == "S" else cell for cell in row]
        print(f"{idx} " + " ".join(row_display))

# Class for Battleships game 
class Battleships:
    self.player_board = create_grid()
        self.computer_board = create_grid()
        self.player_guesses_board = create_grid()
        self.computer_guesses_board = create_grid()
        self.player_ships = []
        self.computer_ships = []
        self.player_guesses = []
        self.computer_guesses = []

        