class DominoGame:
    def __init__(self):
        # Initialize the game with an empty board and two players with hands
        self.board = []
        self.hands = [[(0, 1), (1, 2), (2, 3)], [(3, 4), (4, 5), (5, 6)]]
        self.current_player = 0  # Player 1 starts

    def switch_player(self):
        # A simple function to switch players
        self.current_player = 1 - self.current_player

    def play_domino(self, domino, end):
        # The play_domino function as defined previously
        if domino in self.hands[self.current_player]:
            self.hands[self.current_player].remove(domino)
            if not self.board:
                self.board.append(domino)
            elif domino[0] == end:
                self.board.insert(0, domino)
            elif domino[1] == end:
                self.board.append(domino)
            else:
                print("Invalid move. Domino does not match the board.")
                return False
            self.switch_player()
            return True
        else:
            print("Invalid move. Domino not in the player's hand.")
            return False

# Initialize a new Domino game
game = DominoGame()

# Let's make a few example moves:
print("Initial Board:", game.board)
print("Player 1's Hand:", game.hands[0])
print("Player 2's Hand:", game.hands[1])

# Player 1 plays (0, 1) to start the game
game.play_domino((0, 1), 1)
print("\nBoard after Player 1's move:", game.board)
print("Player 1's Hand after the move:", game.hands[0])
print("Player 2's Hand after the move:", game.hands[1])

# Player 2 attempts an invalid move (4, 5) since it doesn't match the board
game.play_domino((4, 5), 1)

# Player 2 plays (3, 4) to continue the game
game.play_domino((3, 4), 4)
print("\nBoard after Player 2's move:", game.board)
print("Player 1's Hand after the move:", game.hands[0])
print("Player 2's Hand after the move:", game.hands[1])
