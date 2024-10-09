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

    # Place all ships for a player
    def place_all_ships(self):
        print("Place your ships on the board.")
        for ship, size in SHIP_SIZES.items():
            self.place_ship(self.player_board, size, ship)
        print("Computer is placing its ships.")
        for ship, size in SHIP_SIZES.items():
            self.place_ship(self.computer_board, size, ship)

    # Validate a guess to ensure it is within bounds and has not been guessed already
    def validate_guess(self, guess, guesses_board):
        try:
            row, col = map(int, guess.split(","))
            if (row < 0 or row >= 10) or (col < 0 or col >= 10):
                print("Coordinates out of bounds. Try again.")
                return False
            if guesses_board[row][col] != " ":
                print("You have already guessed those coordinates. Try again.")
                return False
            return (row, col)
        except ValueError:
            print("Invalid input. Please enter row,col (e.g., 2,3).")
            return False

    # Handle player's turn
    def player_turn(self):
        while True:
            guess = input("Enter your guess (row,col): ")
            validated_guess = self.validate_guess(guess, self.player_guesses_board)
            if validated_guess:
                row, col = validated_guess
                self.player_guesses.append((row, col))
                if self.computer_board[row][col] == "S":
                    print("Hit!")
                    self.player_guesses_board[row][col] = "*"
                    self.computer_board[row][col] = "*"
                else:
                    print("Miss!")
                    self.player_guesses_board[row][col] = "X"
                break

    # Handle computer's turn
    def computer_turn(self):
        while True:
            row, col = random.randint(0, 9), random.randint(0, 9)
            if (row, col) not in self.computer_guesses:
                self.computer_guesses.append((row, col))
                print(f"Computer guessed: {row},{col}")
                if self.player_board[row][col] == "S":
                    print("Computer hit one of your ships!")
                    self.computer_guesses_board[row][col] = "*"
                    self.player_board[row][col] = "*"
                else:
                    print("Computer missed!")
                    self.computer_guesses_board[row][col] = "X"
                
     # Check if all ships have been sunk
    def all_ships_sunk(self, board):
        for row in board:
            if "S" in row:
                return False
        return True

    # Main game loop
    def play_game(self):
        print("Welcome to Battleships!")
        player_name = input("Enter your name: ")
        print(f"Hello, {player_name}. Let's start!")
        
        self.place_all_ships()

        while True:
            # Player's turn
            print("\nYour guesses board:")
            display_grid(self.player_guesses_board)
            print("\nComputer's board (hidden):")
            display_grid(self.computer_guesses_board, hide_ships=True)
            self.player_turn()

            if self.all_ships_sunk(self.computer_board):
                print("Congratulations! You sank all the computer's ships. You win!")
                break

            # Computer's turn
            print("\nComputer's turn:")
            self.computer_turn()

            if self.all_ships_sunk(self.player_board):
                print("All your ships have been sunk. The computer wins.")
                break

# Start the game
if __name__ == "__main__":
    game = Battleships()
    game.play_game()