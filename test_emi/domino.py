import random

class Domino:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def flip(self):
        self.left, self.right = self.right, self.left
        return self

    def __repr__(self):
        return f"({self.left},{self.right})"
    
    def __eq__(self, other):
        return (self.left == other.left and self.right == other.right) or \
           (self.left == other.right and self.right == other.left)
           
def domino_fine(domino):
        return domino.left + domino.right

class Game:
    def __init__(self):
        self.tiles = [Domino(a, b) for a in range(7) for b in range(a, 7)]
        random.shuffle(self.tiles)
        
        self.player_hand = self.tiles[:7]
        self.computer_hand = self.tiles[7:14]
        self.pool = self.tiles[14:]
        self.board = []
        self.history = []
    
    def display_board(self):
        if len(self.board) == 0:
            print("Board: []\n")
        elif len(self.board) == 1:
            print(f"Board: {self.board}\n")
        elif len(self.board) == 2:
            print(f"Board: {self.board[0]}, {self.board[1]}\n")
        else:
            print(f"Board: {self.board[0]}, ...{len(self.board) - 2} tiles..., {self.board[-1]}\n")
    
    def possible_moves(self, hand):
        if not self.board:
            return hand

        left, right = self.board[0].left, self.board[-1].right
        return [tile for tile in hand if tile.left == left or tile.right == left or tile.left == right or tile.right == right]

    def play(self):
        if input("Would you like to manually assign tiles? (yes/no): ").strip().lower() == "yes":
            self.manual_tile_assignment()
        
        # Determine the starting player based on the highest "fine"
        player_max_fine = max(self.player_hand, key=domino_fine)
        computer_max_fine = max(self.computer_hand, key=domino_fine)

        if domino_fine(player_max_fine) >= domino_fine(computer_max_fine):
            turn = "Player"
        else:
            turn = "Computer"

        print(f"{turn} starts the game.\n")

        while True:
            
            
            print(f"Computer's hand: {self.computer_hand}\n")
            # Display pool
            print(f"Pool: {self.pool}\n")
            
            self.save_state()
            if turn == "Player":
                move, direction = self.get_player_move()  # Get the move and the direction
                if move:
                    if direction == "left":
                        self.board.insert(0, move)
                    else:
                        self.board.append(move)
                turn = 'Computer'
            else:
                move, direction = self.minimax_move(self.computer_hand)
                if move:
                    print(f"\nComputer played: {move}\n")
                    if direction == "left":
                        self.board.insert(0, move)
                    else:
                        self.board.append(move)
                turn = "Player"

            if len(self.pool) == 0 and not self.possible_moves(self.computer_hand) and not self.possible_moves(self.player_hand):
                print("\nIt's a draw!")
                break

    def get_player_move(self):
        possible = self.possible_moves(self.player_hand)

        while not possible and self.pool:
            input("No valid moves. Press enter to draw from the pool...")
            tile = self.pool.pop()
            self.player_hand.append(tile)
            print(f"You drew {tile} from the pool.\n")
            possible = self.possible_moves(self.player_hand)

        # If the pool is empty and no valid move can be made

        if not possible:
            if self.pool:
                tile = self.pool.pop()
                self.player_hand.append(tile)
                print(f"You drew {tile} from the pool.\n")
            return None, None

        while True:
            print(f"Your hand: {self.player_hand}\n")
            print(f"Board: {self.board}\n")
            move = input("Enter your move (e.g. 2,1) or undo to revert to last move: ")
            
            if move.lower() == 'undo':
                self.undo_last_move()
                continue
            
            left, right = map(int, move.split(","))
            selected_tile = Domino(left, right)

            direction = None

            if not self.board:
                direction = "right"
            else:
                if selected_tile.right == self.board[0].left:
                    direction = "left"
                    selected_tile.flip()
                elif selected_tile.left == self.board[0].left:
                    direction = "left"
                elif selected_tile.left == self.board[-1].right:
                    direction = "right"
                elif selected_tile.right == self.board[-1].right:
                    direction = "right"
                    selected_tile.flip()
            
            if self.board:
                if direction == "left" and selected_tile.right != self.board[0].left:
                    selected_tile.flip()
                elif direction == "right" and selected_tile.left != self.board[-1].right:
                    selected_tile.flip()

            

            if direction:
                for tile in self.player_hand:
                    if tile == selected_tile:
                        self.player_hand.remove(tile)
                        break
                return selected_tile, direction

            print("\nInvalid move. Please select a valid domino or draw from the pool.\n")

            
    def minimax_move(self, hand):
        moves = self.possible_moves(hand)

        if not moves:
            if self.pool:
                tile = self.pool.pop()
                self.computer_hand.append(tile)
            return None, None

        valid_moves = []

        if not self.board:
            valid_moves = [(move, "right") for move in moves]
        else:
            for move in moves:
                # Check if move matches the left end of the board
                if move.right == self.board[0].left:
                    valid_moves.append((move.flip(), "left"))
                elif move.left == self.board[0].left:
                    valid_moves.append((move, "left"))
                    
                # Check if move matches the right end of the board
                elif move.left == self.board[-1].right:
                    valid_moves.append((move, "right"))
                elif move.right == self.board[-1].right:
                    valid_moves.append((move.flip(), "right"))

        if not valid_moves:
            return None, None

        move, direction = random.choice(valid_moves)
        
            # Ensure correct orientation of the tile relative to the board
        if direction == "left" and move.right != self.board[0].left:
            move.flip()
        elif direction == "right" and move.left != self.board[-1].right:
            move.flip()
        
        self.computer_hand.remove(move)
        return move, direction

    def save_state(self):
        state = {
            "board": self.board.copy(),
            "player_hand": self.player_hand.copy(),
            "computer_hand": self.computer_hand.copy(),
            "pool": self.pool.copy()
        }
        self.history.append(state)

    def undo_last_move(self):
        if not self.history:
            print("No moves to undo!")
            return

        state = self.history.pop()
        self.board = state["board"]
        self.player_hand = state["player_hand"]
        self.computer_hand = state["computer_hand"]
        self.pool = state["pool"]


    def manual_tile_assignment(self):
        self.player_hand = []
        self.computer_hand = []

        print("Assigning tiles for Player:")
        for i in range(7):  # assuming each player gets 7 tiles to start
            tile = input(f"Enter tile {i+1} for Player (e.g. 2,1): ")
            left, right = map(int, tile.split(","))
            self.player_hand.append(Domino(left, right))

        print("\nAssigning tiles for Computer:")
        for i in range(7):  # assuming each player gets 7 tiles to start
            tile = input(f"Enter tile {i+1} for Computer (e.g. 2,1): ")
            left, right = map(int, tile.split(","))
            self.computer_hand.append(Domino(left, right))


Game().play()
