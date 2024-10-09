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
    
     # Place a ship on a grid
    def place_ship(self, board, ship_size, ship_name):
        while True:
            if board == self.player_board:
                orientation = input(f"Place your {ship_name} (size {ship_size}). Choose orientation (H for horizontal, V for vertical): ").upper()
                row, col = map(int, input(f"Enter starting coordinates for your {ship_name} (row,col): ").split(","))
            else:
                orientation = random.choice(["H", "V"])
                row, col = random.randint(0, 9), random.randint(0, 9)
            
            if orientation == "H":
                if col + ship_size <= 10 and all(board[row][c] == " " for c in range(col, col + ship_size)):
                    for c in range(col, col + ship_size):
                        board[row][c] = "S"
                    break
            elif orientation == "V":
                if row + ship_size <= 10 and all(board[r][col] == " " for r in range(row, row + ship_size)):
                    for r in range(row, row + ship_size):
                        board[r][col] = "S"
                    break
            if board == self.player_board:
                print("Invalid placement. Try again.")