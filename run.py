import random

# Define ship types and their sizes
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
        row_display = [" " if hide_ships and cell == "O" else cell for cell in row]
        print(f"{idx} " + " ".join(row_display))

# Class for the Battleships game
class Battleships:
    def __init__(self):
        self.player_board = create_grid()
        self.computer_board = create_grid()
        self.player_guesses_board = create_grid()
        self.computer_guesses_board = create_grid()
        self.player_guesses = []
        self.computer_guesses = []
        self.player_sunk_ships = 0
        self.computer_sunk_ships = 0
        self.last_computer_hit = None
        self.last_hit_direction = None
        self.possible_next_guesses = []
        self.player_ships = []
        self.computer_ships = []

    # Place a ship on a grid
    def place_ship(self, board, ship_size, ship_name):
        while True:
            if board == self.player_board:
                print(f"Place your {ship_name} (size {ship_size}).")
                orientation = input("Choose orientation (H for horizontal, V for vertical): ").upper()
                print("Enter starting coordinates between (0,0) and (9,9) without parentheses.")
                row, col = map(int, input(f"Enter starting coordinates for your {ship_name} (row,col): ").split(","))
            else:
                orientation = random.choice(["H", "V"])
                row, col = random.randint(0, 9), random.randint(0, 9)

            ship_coordinates = []

            if orientation == "H":
                if col + ship_size <= 10 and all(board[row][c] == " " for c in range(col, col + ship_size)):
                    for c in range(col, col + ship_size):
                        board[row][c] = "O"  # Use "O" to represent ships
                        ship_coordinates.append((row, c))
                    break
            elif orientation == "V":
                if row + ship_size <= 10 and all(board[r][col] == " " for r in range(row, row + ship_size)):
                    for r in range(row, row + ship_size):
                        board[r][col] = "O"  # Use "O" to represent ships
                        ship_coordinates.append((r, col))
                    break

            if board == self.player_board:
                print("Invalid placement. Try again.")

        # Add ship coordinates to the respective player/computer's ship list
        if board == self.player_board:
            self.player_ships.append(ship_coordinates)
        else:
            self.computer_ships.append(ship_coordinates)

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
                print("Coordinates out of bounds. Please enter coordinates between (0,0) and (9,9).")
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
            guess = input("Enter your guess (row,col) between (0,0) and (9,9): ")
            validated_guess = self.validate_guess(guess, self.player_guesses_board)
            if validated_guess:
                row, col = validated_guess
                self.player_guesses.append((row, col))
                if self.computer_board[row][col] == "O":
                    print("Hit!")
                    self.player_guesses_board[row][col] = "*"
                    self.computer_board[row][col] = "*"
                    if self.check_if_ship_sunk(self.computer_ships, row, col):
                        self.player_sunk_ships += 1
                        print("Congratulations! You sank a computer's ship.")
                else:
                    print("Miss!")
                    self.player_guesses_board[row][col] = "X"
                break

    # Check if the entire ship is sunk
    def check_if_ship_sunk(self, ships, row, col):
        for ship in ships:
            if (row, col) in ship:
                ship.remove((row, col))
                if not ship:  # Ship has been completely sunk
                    return True
        return False

    # Handle computer's turn for both easy and hard levels
    def computer_turn(self, difficulty="easy"):
        if difficulty == "easy":
            self.random_computer_turn()
        elif difficulty == "hard":
            self.smart_computer_turn()

    def random_computer_turn(self):
        while True:
            row, col = random.randint(0, 9), random.randint(0, 9)
            if (row, col) not in self.computer_guesses:
                self.computer_guesses.append((row, col))
                print(f"Computer guessed: {row},{col}")
                if self.player_board[row][col] == "O":
                    print("Computer hit one of your ships!")
                    self.computer_guesses_board[row][col] = "*"
                    self.player_board[row][col] = "*"
                    self.last_computer_hit = (row, col)
                    if self.check_if_ship_sunk(self.player_ships, row, col):
                        self.computer_sunk_ships += 1
                        print(f"The computer has sunk one of your ships!")
                        self.last_computer_hit = None
                else:
                    print("Computer missed!")
                    self.computer_guesses_board[row][col] = "X"
                    self.last_computer_hit = None
                break

    # Smart logic for hard difficulty
    def smart_computer_turn(self):
        if self.last_computer_hit and self.last_hit_direction:
            # Continue guessing in the same direction
            row, col = self.last_computer_hit
            if self.last_hit_direction == "H":
                possible_guesses = [(row, col + 1), (row, col - 1)]
            else:
                possible_guesses = [(row + 1, col), (row - 1, col)]
        elif self.last_computer_hit:
            # Try all four directions around the last hit
            row, col = self.last_computer_hit
            possible_guesses = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
            random.shuffle(possible_guesses)
        else:
            self.random_computer_turn()
            return

        for r, c in possible_guesses:
            if (r, c) not in self.computer_guesses and 0 <= r < 10 and 0 <= c < 10:
                self.computer_guesses.append((r, c))
                print(f"Computer guessed: {r},{c}")
                if self.player_board[r][c] == "O":
                    print("Computer hit one of your ships!")
                    self.computer_guesses_board[r][c] = "*"
                    self.player_board[r][c] = "*"
                    self.last_computer_hit = (r, c)
                    if self.check_if_ship_sunk(self.player_ships, r, c):
                        self.computer_sunk_ships += 1
                        print(f"The computer has sunk one of your ships!")
                        self.last_computer_hit = None
                        self.last_hit_direction = None
                    else:
                        # Determine direction of hits
                        if self.last_hit_direction is None:
                            if r == row:
                                self.last_hit_direction = "H"
                            else:
                                self.last_hit_direction = "V"
                else:
                    print("Computer missed!")
                    self.computer_guesses_board[r][c] = "X"
                    if self.last_hit_direction:
                        # If miss, reset hit direction
                        self.last_hit_direction = None
                    break

    # Check if all ships have been sunk
    def all_ships_sunk(self, board):
        for row in board:
            if "O" in row:
                return False
        return True

    # Main game loop with alternating turns
    def play_game(self, difficulty="easy"):
        print("Welcome to Battleships!")
        print("\nInstructions:")
        print("- 'O' represents placement of your ships.")
        print("- 'X' represents a missed hit.")
        print("- '*' represents a successful hit.")
        print("You will place your ships and then take turns guessing where the computer's ships are located.")
        print("The computer will also guess where your ships are hidden.")
        print("The game ends when one player sinks all of the other's ships!\n")

        player_name = input("Enter your name: ")
        print(f"Hello, {player_name}. Let's start!")

        self.place_all_ships()

        while True:
            # Display scoreboard
            print(f"\nScoreboard: {player_name} {self.player_sunk_ships} - {self.computer_sunk_ships} Computer")
            
            # Player's turn
            print("\nYour guesses board:")
            display_grid(self.player_guesses_board)
            print("\nComputer's Guess Board:")
            display_grid(self.computer_guesses_board)
            self.player_turn()

            if self.all_ships_sunk(self.computer_board):
                print(f"Congratulations, {player_name}! You sank all the computer's ships. You win!")
                break

            # Computer's turn
            print("\nComputer's turn:")
            self.computer_turn(difficulty=difficulty)

            if self.all_ships_sunk(self.player_board):
                print("All your ships have been sunk. The computer wins.")
                break

# Start the game
if __name__ == "__main__":
    difficulty = input("Choose difficulty (easy/hard): ").lower()
    game = Battleships()
    game.play_game(difficulty=difficulty)