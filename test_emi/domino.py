import random

class Domino:
    """
        Inicializa una ficha de dominó con dos extremos: izquierdo y derecho.

        Parámetros:
        - izquierda (int): El valor del extremo izquierdo del dominó.
        - right (int): El valor del lado derecho del dominó.
        """
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    """
        Voltea el dominó, intercambiando sus valores izquierdo y derecho.

        Devuelve:
        - Dominó: Devuelve la instancia de dominó volteada.
        """
    def flip(self):
        self.left, self.right = self.right, self.left
        return self

    """
        Devuelve una representación en forma de cadena de la ficha de dominó.
        """
    def __repr__(self):
        return f"({self.left},{self.right})"
    
    """
        Comprueba si dos fichas de dominó son iguales. 
        Dos fichas de dominó se consideran iguales si sus valores, independientemente de la orientación, son iguales.

        Parámetros:
        - other (Dominó): La otra ficha de dominó con la que comparar.

        Devuelve:
        - bool: True si las fichas de dominó son iguales, False en caso contrario.
        """
    def __eq__(self, other):
        return (self.left == other.left and self.right == other.right) or \
           (self.left == other.right and self.right == other.left)

"""
    Calcula la suma de los dos extremos de una ficha de dominó.

    Parámetros:
    - dominó (Dominó): La ficha de dominó cuya suma de extremos hay que calcular.

    Devuelve:
    - int: La suma de los dos extremos del dominó.
    """         
def mula(domino):
        return domino.left + domino.right

class Game:
    """
        Inicializa el juego creando un juego completo de fichas de dominó, barajándolas y distribuyéndolas entre el jugador, el ordenador y la reserva.
        """
    def __init__(self):
        self.tiles = [Domino(a, b) for a in range(7) for b in range(a, 7)]
        random.shuffle(self.tiles)
        
        self.jugador_hand = self.tiles[:7]
        self.computadora_hand = self.tiles[7:14]
        self.pool = self.tiles[14:]
        self.tablero = []
        self.history = []
    
    """
        Muestra el estado actual del tablero de forma concisa, mostrando sólo el principio, el final y el recuento de las fichas intermedias.
        """
    def display_tablero(self):
        if len(self.tablero) == 0:
            print("tablero: []\n")
        elif len(self.tablero) == 1:
            print(f"tablero: {self.tablero}\n")
        elif len(self.tablero) == 2:
            print(f"tablero: {self.tablero[0]}, {self.tablero[1]}\n")
        else:
            print(f"tablero: {self.tablero[0]}, ...{len(self.tablero) - 2} tiles..., {self.tablero[-1]}\n")
    
    """
        Determina los posibles movimientos que un jugador o la computadora pueden hacer basándose en el estado actual del tablero.

        Parámetros:
        - mano (lista[Dominó]): El conjunto de fichas de dominó que tiene el jugador o la computadora.

        Devuelve:
        - list[Dominó]: Una lista de fichas de dominó válidas que se pueden jugar.
        """
    def possible_moves(self, hand):
        if not self.tablero:
            return hand

        left, right = self.tablero[0].left, self.tablero[-1].right
        return [tile for tile in hand if tile.left == left or tile.right == left or tile.left == right or tile.right == right]


    # Inicia y ejecuta el bucle principal del juego en el que el jugador y el ordenador se turnan para jugar.
        
    def play(self):
        if input("Quieres asignar manualmente las fichas? (si/no): ").strip().lower() == "si":
            self.manual_tile_assignment()
        
        # Determina quien empieza el juego
        jugador_max_fine = max(self.jugador_hand, key=mula)
        computadora_max_fine = max(self.computadora_hand, key=mula)

        if mula(jugador_max_fine) >= mula(computadora_max_fine):
            turn = "jugador"
        else:
            turn = "computadora"

        print(f"{turn} empieza el juego.\n")

        while True:
            
            
            print(f"Mano de la computadora: {self.computadora_hand}\n")
            # Sopa de fichas
            print(f"Sopa: {self.pool}\n")
            
            self.save_state()
            if turn == "jugador":
                move, direction = self.get_jugador_move()  
                if move:
                    if direction == "left":
                        self.tablero.insert(0, move)
                    else:
                        self.tablero.append(move)
                
                if not self.jugador_hand:
                    print("Ganasteeeee :D")
                    return

                turn = 'computadora'
            else:
                _, move, direction = self.minimax_move(self.computadora_hand, 3, True)
                if move:
                    print(f"\nLa computadora jugó: {move}\n")
                    if direction == "left":
                        self.tablero.insert(0, move)
                    else:
                        self.tablero.append(move)
                
                if not self.computadora_hand:
                    print("computadora gana")
                    return

                turn = "jugador"

            if len(self.pool) == 0 and not self.possible_moves(self.computadora_hand) and not self.possible_moves(self.jugador_hand):
                print("\nEmpate :/!")
                break


        #Solicita un movimiento al jugador. Si el jugador no puede realizar un movimiento, permite robar de la reserva o deshacer el último movimiento.

        #Devuelve:
        #tupla: Una tupla que contiene la ficha de dominó seleccionada y la dirección en la que jugarla ("izquierda" o "derecha").
        
    def get_jugador_move(self):
        possible = self.possible_moves(self.jugador_hand)

        while not possible and self.pool:
            input("Comes! presiona enter")
            tile = self.pool.pop()
            self.jugador_hand.append(tile)
            print(f"Sacaste {tile} de la sopa.\n")
            possible = self.possible_moves(self.jugador_hand)

        if not possible:
            if self.pool:
                tile = self.pool.pop()
                self.jugador_hand.append(tile)
                print(f"Sacaste {tile} de la sopa.\n")
            return None, None

        while True:
            print(f"Tu mano: {self.jugador_hand}\n")
            print(f"tablero: {self.tablero}\n")
            move = input("Pon la ficha que deseas (e.g. 2,1) o undo para regresar al ultimo movimiento: ")
            
            if move.lower() == 'undo':
                self.undo_last_move()
                continue
            
            left, right = map(int, move.split(","))
            selected_tile = Domino(left, right)
            
            if selected_tile not in self.jugador_hand:
                print("\nNo tienes esa ficha, come de la sopa o pon una que si este!!.\n")
                continue

            direction = None

            if not self.tablero:
                direction = "right"
            else:
                if selected_tile.right == self.tablero[0].left:
                    direction = "left"
                    selected_tile.flip()
                elif selected_tile.left == self.tablero[0].left:
                    direction = "left"
                elif selected_tile.left == self.tablero[-1].right:
                    direction = "right"
                elif selected_tile.right == self.tablero[-1].right:
                    direction = "right"
                    selected_tile.flip()
            
            if self.tablero:
                if direction == "left" and selected_tile.right != self.tablero[0].left:
                    selected_tile.flip()
                elif direction == "right" and selected_tile.left != self.tablero[-1].right:
                    selected_tile.flip()

            

            if direction:
                for tile in self.jugador_hand:
                    if tile == selected_tile:
                        self.jugador_hand.remove(tile)
                        break
                return selected_tile, direction

            print("\nMovimiento invalido. Selecciona una valida o come de la sopa.\n")

            
    def minimax_move(self, hand, depth, is_maximizing):
        moves = self.possible_moves(hand)

        # Caso base: si no hay jugadas posibles o se acaba la partida
        if not moves or depth == 0 or len(self.pool) == 0 and not self.possible_moves(self.computadora_hand) and not self.possible_moves(self.jugador_hand):
            # Heurística: simplemente la diferencia en dominoes 
            return len(self.jugador_hand) - len(self.computadora_hand), None, None

        # Turno computadora, maximizando el puntaje
        if is_maximizing:
            max_eval = float('-inf')
            best_move = None
            best_dir = None

            for move in moves:
                self.computadora_hand.remove(move)
                if not self.tablero:
                    self.tablero.append(move)
                    direction = "right"
                else:
                    direction = None
                    if move.right == self.tablero[0].left:
                        self.tablero.insert(0, move.flip())
                        direction = "left"
                    elif move.left == self.tablero[0].left:
                        self.tablero.insert(0, move)
                        direction = "left"
                    elif move.left == self.tablero[-1].right:
                        self.tablero.append(move)
                        direction = "right"
                    elif move.right == self.tablero[-1].right:
                        self.tablero.append(move.flip())
                        direction = "right"
                    
                eval_score, _, _ = self.minimax_move(self.jugador_hand, depth-1, False)

                # Undo el movimiento    
                if direction == "left":
                    self.tablero.pop(0)
                else:
                    self.tablero.pop()
                self.computadora_hand.append(move)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                    best_dir = direction

            return max_eval, best_move, best_dir

        # Turno del jugador (minimizar)
        else:
            min_eval = float('inf')
            for move in moves:
                self.jugador_hand.remove(move)
                if not self.tablero:
                    self.tablero.append(move)
                    direction = "right"
                else:
                    direction = None
                    if move.right == self.tablero[0].left:
                        self.tablero.insert(0, move.flip())
                        direction = "left"
                    elif move.left == self.tablero[0].left:
                        self.tablero.insert(0, move)
                        direction = "left"
                    elif move.left == self.tablero[-1].right:
                        self.tablero.append(move)
                        direction = "right"
                    elif move.right == self.tablero[-1].right:
                        self.tablero.append(move.flip())
                        direction = "right"

                eval_score, _, _ = self.minimax_move(self.computadora_hand, depth-1, True)

                # Undo the move
                if direction == "left":
                    self.tablero.pop(0)
                else:
                    self.tablero.pop()
                self.jugador_hand.append(move)

                if eval_score < min_eval:
                    min_eval = eval_score

            return min_eval, None, None  # We only return moves for the computer, not the player



    #Guarda el estado actual de la partida, incluyendo el tablero, la mano del jugador, la mano de la computadora y el pool en el historial.
        
    def save_state(self):
        state = {
            "tablero": self.tablero.copy(),
            "jugador_hand": self.jugador_hand.copy(),
            "computadora_hand": self.computadora_hand.copy(),
            "pool": self.pool.copy()
        }
        self.history.append(state)


    # Devuelve el juego al estado anterior guardado en el historial, deshaciendo efectivamente el último movimiento.
        
    def undo_last_move(self):
        if not self.history:
            print("No hay movimientos!")
            return

        state = self.history.pop()
        self.tablero = state["tablero"]
        self.jugador_hand = state["jugador_hand"]
        self.computadora_hand = state["computadora_hand"]
        self.pool = state["pool"]


    # Permite al usuario distribuir manualmente las fichas de dominó entre el jugador, el ordenador y la reserva.
        
    def manual_tile_assignment(self):
        all_tiles = set()  #Lleve un registro de todas las fichas añadidas para evitar repeticiones
        
        def get_unique_tile():
            while True:
                tile = input("Pon una ficha (e.g. 2,1) o escribe 'done' para terminar: ")
                if tile == "done":
                    return None
                left, right = map(int, tile.split(","))
                if (left, right) not in all_tiles and (right, left) not in all_tiles:
                    all_tiles.add((left, right))
                    return Domino(left, right)
                else:
                    print("Ya se agregó esta ficha, pon otra.")

        print("Fichas para el jugador:")
        for i in range(7): 
            self.jugador_hand.append(get_unique_tile())

        print("\nFichas para la computadora:")
        for i in range(7):  
            self.computadora_hand.append(get_unique_tile())

        print("\nFichas para la sopa:")
        while True:
            tile = get_unique_tile()
            if tile:
                self.pool.append(tile)
            else:
                break


Game().play()
