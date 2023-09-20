import time

class DominoGame:
    def __init__(self, players):
        # Initialize the game with a list of player names
        self.players = players
        self.board = []  # The current state of the board (list of played dominoes)
        self.hands = {player: [] for player in players}  # Dictionary to store each player's hand
        self.current_player = players[0]  # Start with the first player's turn

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
    
    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.is_game_over():
            return self.evaluate_game_state()

        if maximizing_player:
            max_eval = float("-inf")
            legal_moves = self.generate_legal_moves()
            for move in legal_moves:
                self.play_domino(move, self.board[-1][1] if self.board else 0)
                eval_score = self.minimax(depth - 1, False)
                max_eval = max(max_eval, eval_score)
                if self.board:
                    self.board.pop()
                self.hands[self.current_player].append(move)
            return max_eval
        else:
            min_eval = float("inf")
            legal_moves = self.generate_legal_moves()
            for move in legal_moves:
                self.play_domino(move, self.board[-1][1] if self.board else 0)
                eval_score = self.minimax(depth - 1, True)
                min_eval = min(min_eval, eval_score)
                if self.board:
                    self.board.pop()
                self.hands[self.current_player].append(move)
            return min_eval
        def get_best_move_with_alpha_beta(self, depth):
        legal_moves = self.generate_legal_moves()
        best_move = None
        alpha = float("-inf")
        beta = float("inf")
        for move in legal_moves:
            self.play_domino(move, self.board[-1][1] if self.board else 0)
            eval_score = self.minimax(depth - 1, False)  # Use the minimax function
            if eval_score > alpha:
                alpha = eval_score
                best_move = move
            self.board.pop()
            self.hands[self.current_player].append(move)
        return best_move

    def choose_best_move(self, depth, time_limit=None):
        best_move = None
        best_score = float("-inf")
        start_time = time.time()

        legal_moves = self.generate_legal_moves()

        for move in legal_moves:
            self.play_domino(move, self.board[-1][1] if self.board else 0)
            eval_score = self.minimax(depth - 1, False)  # Use the minimax function
            
            if eval_score > best_score:
                best_score = eval_score
                best_move = move

            if self.board:
                self.board.pop()
            self.hands[self.current_player].append(move)

            if time_limit and time.time() - start_time >= time_limit:
                break

        return best_move