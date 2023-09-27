import time

# falta documentar 
class juego_domino:
    def __init__(self, jugadores):
        # Initialize the game with a list of jugador names
        self.jugadores = jugadores
        self.tablero = []  # The current state of the tablero (list of played dominoes)
        self.manos = {jugador: [] for jugador in jugadores}  # Dictionary to store each jugador's hand
        self.jugador_actual = jugadores[0]  # Start with the first jugador's turn

    def cambiar_jugador(self):
        # Switch to the next jugador's turn
        indice_actual = self.jugadores.index(self.jugador_actual)
        sig_indice = (indice_actual + 1) % len(self.jugadores)
        self.jugador_actual = self.jugadores[sig_indice]

    # test def
    def juega_ficha(self, ficha, cola_tablero):
        # Play a domino on the tablero
        if ficha in self.manos[self.jugador_actual]:
            self.manos[self.jugador_actual].remove(ficha)
            if not self.tablero:
                # If the tablero is empty, add the domino
                self.tablero.append(ficha)
            elif ficha[0] == cola_tablero:
                # If the domino matches the end value, add it to the beginning of the tablero
                self.tablero.insert(0, ficha)
            elif ficha[1] == cola_tablero:
                # If the domino matches the end value, add it to the end of the tablero
                self.tablero.append(ficha)
            else:
                # Invalid move
                print("Movimiento ilegal. La ficha no coincide con la del tablero.")
                return False
            self.cambiar_jugador()
            return True
        else:
            print("Movimiento imposible. La ficha no está disponible.")
            return False

    def get_estado_actual(self):
        # Get the current state of the game
        return {
            "jugador_actual": self.jugador_actual,
            "tablero": self.tablero,
            "manos": self.manos
        }

    def acabo_juego(self):
        # Check if the game is over (a jugador has an empty hand)
        for jugador in self.jugadores:
            if not self.manos[jugador]:
                return True
        return False
    
    def mov_legales(self):
        mov_legal = []
        
        # check if tablero is empty or if the ficha matches either end 
        for ficha in self.manos[self.jugador_actual]:
            if (
                not self.tablero  # If the tablero is empty, all dominoes are legal moves
                or ficha[0] == self.tablero[0][0]  # Match the left end
                or ficha[0] == self.tablero[-1][1]  # Match the right end
                or ficha[1] == self.tablero[0][0]  # Match the left end (reversed)
                or ficha[1] == self.tablero[-1][1]  # Match the right end (reversed)
            ):
                mov_legal.append(ficha)
        return mov_legal
    
    # funcion heurística
    def evalua_estado_actual(self):
        # Evaluation function for the current game state
        puntuacion = 0

        # Factor 1: Number of tiles in hand
        no_fichas_en_mano = len(self.manos[self.jugador_actual])
        puntuacion += no_fichas_en_mano

        # Factor 2: Number of tiles played
        no_fichas_jugadas = len(self.tablero)
        puntuacion -= no_fichas_jugadas

        # Factor 3: tablero configuration (e.g., try to play doubles early)
        if no_fichas_jugadas > 0:
            primera_ficha = self.tablero[0]
            ultima_ficha = self.tablero[-1]
            if primera_ficha[0] == primera_ficha[1]:
                # If the first tile on the tablero is a double, give a bonus
                puntuacion += 2
            if ultima_ficha[0] == ultima_ficha[1]:
                # If the last tile on the tablero is a double, give a bonus
                puntuacion += 2
         
        # lo agregamos o no?         
        #factor_de_probabilidad = random.uniform(0,1)
        #puntuacion += factor_de_probabilidad

        return puntuacion
    
    def minimax(self, depth, jugador_max):
        if depth == 0 or self.acabo_juego():
            return self.evalua_estado_actual()

        if jugador_max:
            max_eval = float("-inf")
            mov_legal = self.mov_legales()
            for mov in mov_legal:
                self.juega_ficha(mov, self.tablero[-1][1] if self.tablero else 0)
                eval_puntuacion = self.minimax(depth - 1, False)
                max_eval = max(max_eval, eval_puntuacion)
                if self.tablero:
                    self.tablero.pop()
                self.manos[self.jugador_actual].append(mov)
            return max_eval
        else:
            min_eval = float("inf")
            mov_legal = self.mov_legales()
            for mov in mov_legal:
                self.juega_ficha(mov, self.tablero[-1][1] if self.tablero else 0)
                eval_puntuacion = self.minimax(depth - 1, True)
                min_eval = min(min_eval, eval_puntuacion)
                if self.tablero:
                    self.tablero.pop()
                self.manos[self.jugador_actual].append(mov)
            return min_eval

    # quitamos el limite de tiempo
    def escoge_mejor_mov(self, depth, limite_tiempo=None):
        mejor_mov = None
        mejor_puntuacion = float("-inf")
        empieza_tiempo = time.time()

        mov_legal = self.mov_legales()

        for mov in mov_legal:
            self.juega_ficha(mov, self.tablero[-1][1] if self.tablero else 0)
            eval_puntuacion = self.minimax(depth - 1, False)  # Use the minimax function
            
            if eval_puntuacion > mejor_puntuacion:
                mejor_puntuacion = eval_puntuacion
                mejor_mov = mov

            if self.tablero:
                self.tablero.pop()
            self.manos[self.jugador_actual].append(mov)

            if limite_tiempo and time.time() - empieza_tiempo >= limite_tiempo:
                break

        return mejor_mov

    def jugar(self, max_depth, limite_tiempo=None):
        while not self.acabo_juego():
            print("\nEstado actual del juego:")
            print(self.get_estado_actual())
            print(f"Turno de: {self.jugador_actual}")

            if self.jugador_actual == "Computadora":
                # Computadora jugador's turn
                mejor_mov = self.escoge_mejor_mov(max_depth, limite_tiempo)
                if mejor_mov:
                    print(f"Movimiento de la computadora: {mejor_mov}")
                    self.juega_ficha(mejor_mov, self.tablero[-1][1] if self.tablero else 0)
                else:
                    print("La computadora no tiene movimientos válidos.")
            else:
                # Human jugador's turn
                print(f"Tus fichas disponibles: {self.jugadores['Jugador']['mano']}") # 'Human' 'hand' ?
                mov_valido = False
                while not mov_valido:
                    try:
                        no_de_la_ficha = int(input("Escribe el numero de la ficha que deseas colocar: "))
                        domino = self.jugadores['Jugador']['mano'][no_de_la_ficha]
                        if  domino in self.mov_legales: # self.es_mov_valido(domino):
                            self.juega_ficha(domino, self.tablero[-1][1] if self.tablero else 0)
                            mov_valido = True
                        else:
                            print("Movimiento inválido.")
                    except (ValueError, IndexError):
                        print("Movimiento inválido. Inténtalo de nuevo.")

            # Switch to the next jugador's turn
            self.cambiar_jugador()

        print("\nFin del juego.")
        print("Estado final:")
        print(self.get_estado_actual())

    def guarda_estado_del_juego(self):
        # Store the current game state for possible undo
        state = {
            "jugador_actual": self.jugador_actual,
            "tablero": self.tablero.copy(),
            "manos": {jugador: hand.copy() for jugador, hand in self.manos.items()},
        }
        self.estados_del_juego.append(state)

    def control_z(self):
        # Revert to the previous game state
        if len(self.estados_del_juego) >= 2:
            self.estados_del_juego.pop()  # Remove the current state
            estado_previo = self.estados_del_juego.pop()  # Get the previous state
            self.jugador_actual = estado_previo["jugador_actual"]
            self.tablero = estado_previo["tablero"]
            self.manos = estado_previo["manos"]
            