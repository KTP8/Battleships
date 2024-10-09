#Game Class 
import random 

class Battleships:
    def __init__(self, board_size, num_ships):
        self.board_size = board_size
        self.num_ships = num_ships
        self.player_board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.computer_board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.player_ships = []
        self.computer_ships = []
        self.player_guesses = []
        self.computer_guesses = []

     def display_board(self, board):
        for row in board:
            print(' | '.join(row))
            print('-' * (self.board_size * 4 - 1))

    def place_ships(self):
        for _ in range(self.num_ships):
            ship = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
            while ship in self.computer_ships:
                ship = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
            self.computer_ships.append(ship)
            # Placeholder for player ship placement, later implement player input validation
        
    def play_game(self):
        print("Welcome to Battleships!")
        self.display_board(self.player_board)
        self.place_ships()
        # Placeholder for the game loop