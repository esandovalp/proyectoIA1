import time

class DominoGame:
    def __init__(self, players):
        # Initialize the game with a list of player names
        self.players = players
        self.board = []  # The current state of the board (list of played dominoes)
        self.hands = {player: [] for player in players}  # Dictionary to store each player's hand
        self.current_player = players[0]  # Start with the first player's turn

    def switch_player(self):
        # Switch to the next player's turn
        current_index = self.players.index(self.current_player)
        next_index = (current_index + 1) % len(self.players)
        self.current_player = self.players[next_index]

    def play_domino(self, domino, end):
        # Play a domino on the board
        if domino in self.hands[self.current_player]:
            self.hands[self.current_player].remove(domino)
            if not self.board:
                # If the board is empty, add the domino
                self.board.append(domino)
            elif domino[0] == end:
                # If the domino matches the end value, add it to the beginning of the board
                self.board.insert(0, domino)
            elif domino[1] == end:
                # If the domino matches the end value, add it to the end of the board
                self.board.append(domino)
            else:
                # Invalid move
                print("Invalid move. Domino does not match the board.")
                return False
            self.switch_player()
            return True
        else:
            print("Invalid move. Domino not in the player's hand.")
            return False

    def get_current_state(self):
        # Get the current state of the game
        return {
            "current_player": self.current_player,
            "board": self.board,
            "hands": self.hands,
        }

    def is_game_over(self):
        # Check if the game is over (a player has an empty hand)
        for player in self.players:
            if not self.hands[player]:
                return True
        return False
    
    def generate_legal_moves(self):
        legal_moves = []
        for domino in self.hands[self.current_player]:
            if (
                not self.board  # If the board is empty, all dominoes are legal moves
                or domino[0] == self.board[0][0]  # Match the left end
                or domino[0] == self.board[-1][1]  # Match the right end
                or domino[1] == self.board[0][0]  # Match the left end (reversed)
                or domino[1] == self.board[-1][1]  # Match the right end (reversed)
            ):
                legal_moves.append(domino)
        return legal_moves
    
    def evaluate_game_state(self):
        # Evaluation function for the current game state
        score = 0

        # Factor 1: Number of tiles in hand
        num_tiles_in_hand = len(self.hands[self.current_player])
        score += num_tiles_in_hand

        # Factor 2: Number of tiles played
        num_tiles_played = len(self.board)
        score -= num_tiles_played

        # Factor 3: Board configuration (e.g., try to play doubles early)
        if num_tiles_played > 0:
            first_tile = self.board[0]
            last_tile = self.board[-1]
            if first_tile[0] == first_tile[1]:
                # If the first tile on the board is a double, give a bonus
                score += 2
            if last_tile[0] == last_tile[1]:
                # If the last tile on the board is a double, give a bonus
                score += 2

        return score
    
    def minimax_with_alpha_beta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_game_over():
            return self.evaluate_game_state()

        if maximizing_player:
            max_eval = float("-inf")
            legal_moves = self.generate_legal_moves()
            for move in legal_moves:
                self.play_domino(move, self.board[-1][1] if self.board else 0)
                eval_score = self.minimax_with_alpha_beta(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if self.board:
                    self.board.pop()
                self.hands[self.current_player].append(move)
                if beta <= alpha:
                    break  # Prune remaining branches
            return max_eval
        else:
            min_eval = float("inf")
            legal_moves = self.generate_legal_moves()
            for move in legal_moves:
                self.play_domino(move, self.board[-1][1] if self.board else 0)
                eval_score = self.minimax_with_alpha_beta(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if self.board:
                    self.board.pop()
                self.hands[self.current_player].append(move)
                if beta <= alpha:
                    break  # Prune remaining branches
            return min_eval

    def get_best_move_with_alpha_beta(self, depth):
        legal_moves = self.generate_legal_moves()
        best_move = None
        alpha = float("-inf")
        beta = float("inf")
        for move in legal_moves:
            self.play_domino(move, self.board[-1][1] if self.board else 0)
            eval_score = self.minimax_with_alpha_beta(depth - 1, alpha, beta, False)
            if eval_score > alpha:
                alpha = eval_score
                best_move = move
            self.board.pop()
            self.hands[self.current_player].append(move)
        return best_move
    
    def get_best_move_with_iterative_deepening(self, max_depth, time_limit=None):
        best_move = None
        start_time = time.time()
        
        for depth in range(1, max_depth + 1):
            legal_moves = self.generate_legal_moves()
            alpha = float("-inf")
            beta = float("inf")
            current_best_move = None

            for move in legal_moves:
                self.play_domino(move, self.board[-1][1] if self.board else 0)
                eval_score = self.minimax_with_alpha_beta(depth - 1, alpha, beta, False)
                if eval_score > alpha:
                    alpha = eval_score
                    current_best_move = move
                if self.board:
                    self.board.pop()  # Check if the board is not empty before popping
                self.hands[self.current_player].append(move)

            # Update the best move if it's found at the current depth
            if current_best_move:
                best_move = current_best_move

            # Check if we've reached the time limit
            if time_limit and time.time() - start_time >= time_limit:
                break

        return best_move
    
    def get_ordered_moves(self):
        legal_moves = self.generate_legal_moves()
        
        # Example: Sort moves by the total number of pips on the dominoes
        return sorted(legal_moves, key=lambda move: sum(move))

    def get_best_move_with_move_ordering(self, max_depth, time_limit=None):
        best_move = None
        start_time = time.time()
        
        for depth in range(1, max_depth + 1):
            ordered_moves = self.get_ordered_moves()  # Sort moves using your ordering heuristic
            alpha = float("-inf")
            beta = float("inf")
            current_best_move = None

            for move in ordered_moves:
                self.play_domino(move, self.board[-1][1] if self.board else 0)
                eval_score = self.minimax_with_alpha_beta(depth - 1, alpha, beta, False)
                if eval_score > alpha:
                    alpha = eval_score
                    current_best_move = move
                if self.board:
                    self.board.pop()  # Check if the board is not empty before popping
                self.hands[self.current_player].append(move)

            # Update the best move if it's found at the current depth
            if current_best_move:
                best_move = current_best_move

            # Check if we've reached the time limit
            if time_limit and time.time() - start_time >= time_limit:
                break

        return best_move
    
    def choose_best_move(self, depth, time_limit=None):
        best_move = None
        best_score = float("-inf")
        start_time = time.time()

        legal_moves = self.generate_legal_moves()
        alpha = float("-inf")
        beta = float("inf")

        for move in legal_moves:
            self.play_domino(move, self.board[-1][1] if self.board else 0)
            eval_score = self.minimax_with_alpha_beta(depth - 1, alpha, beta, False)
            
            if eval_score > best_score:
                best_score = eval_score
                best_move = move

            if self.board:
                self.board.pop()
            self.hands[self.current_player].append(move)

            alpha = max(alpha, best_score)

            if time_limit and time.time() - start_time >= time_limit:
                break

        return best_move
    
    def play_game(self, max_depth, time_limit=None):
        while not self.is_game_over():
            print("\nCurrent state:")
            print(self.get_current_state())
            print(f"{self.current_player}'s turn")

            if self.current_player == "Computer":
                # Computer player's turn
                best_move = self.choose_best_move(max_depth, time_limit)
                if best_move:
                    print(f"Computer plays {best_move}")
                    self.play_domino(best_move, self.board[-1][1] if self.board else 0)
                else:
                    print("Computer has no valid moves.")
            else:
                # Human player's turn (you can implement this part for human input)
                pass

            # Switch to the next player's turn
            self.switch_player()

        print("\nGame Over!")
        print("Final state:")
        print(self.get_current_state())

#game = DominoGame(["Player 1", "Player 2"])
#game.hands["Player 1"] = [(3, 4), (4, 6), (1, 5), (2, 2), (5, 5)]
#game.board = [(6, 3)]
#legal_moves = game.generate_legal_moves()
#print("Legal moves for Player 1:", legal_moves)

#game = DominoGame(["Player 1", "Player 2"])
#game.hands["Player 1"] = [(3, 4), (4, 6), (1, 5), (2, 2), (5, 5)]
#game.board = [(6, 3), (3, 3)]
#score = game.evaluate_game_state()
#print("Evaluation score for Player 1:", score)

#game = DominoGame(["Player 1", "Player 2"])
#game.hands["Player 1"] = [(3, 4), (4, 6), (1, 5), (2, 2), (5, 5)]
#game.board = [(6, 3), (3, 3)]
#best_move = game.get_best_move_with_alpha_beta(depth=3)
#print("Best move for Player 1 with Alpha-Beta Pruning:", best_move)

#game = DominoGame(["Player 1", "Player 2"])
#game.hands["Player 1"] = [(3, 4), (4, 6), (1, 5), (2, 2), (5, 5)]
#game.board = [(6, 3), (3, 3)]

# Set a time limit for the search (in seconds)
#time_limit = 5  # You can adjust this as needed

#best_move = game.get_best_move_with_iterative_deepening(max_depth=10, time_limit=time_limit)
#print("Best move for Player 1 with Iterative Deepening:", best_move)

""" game = DominoGame(["Player 1", "Player 2"])
game.hands["Player 1"] = [(3, 4), (4, 6), (1, 5), (2, 2), (5, 5)]
game.board = [(6, 3), (3, 3)]

# Set a time limit for the search (in seconds)
time_limit = 5  # You can adjust this as needed

best_move = game.get_best_move_with_move_ordering(max_depth=10, time_limit=time_limit)
print("Best move for Player 1 with Move Ordering:", best_move) """

""" game = DominoGame(["Player 1", "Player 2"])
game.hands["Player 1"] = [(3, 4), (4, 6), (1, 5), (2, 2), (5, 5)]
game.board = [(6, 3), (3, 3)]

# Set a time limit for the search (in seconds)
time_limit = 5  # You can adjust this as needed

best_move = game.choose_best_move(depth=3, time_limit=time_limit)
print("Best move for Player 1:", best_move) """

""" game = DominoGame(["Human", "Computer"])
game.hands["Human"] = [(3, 4), (4, 6), (1, 5), (2, 2), (5, 5)]
game.hands["Computer"] = [(6, 3), (3, 3)]
game.board = [(6, 3)]

# Set a time limit for the computer player's move (in seconds)
time_limit = 5  # You can adjust this as needed

game.play_game(max_depth=3, time_limit=time_limit) """

