class Ficha:
    __val1 = -1
    __val2 = -1
    val_no_disp = -1
    val_jugable = -1
    
    def __init__(self, valor1, valor2):
        self.__val1 = max(valor1, valor2)
        self.__val2 = min(valor1, valor2)
        
 #------Getters and Setters------#   
    def get_val1(self):
        return self.__val1
    
    def set_val1(self, aux_val):
        self.__val1 = aux_val
    
    def get_val2(self):
        return self.__val2
    
    def set_val2(self, aux_va2):
        self.__val2 = aux_va2
    
    
    def print_Atr (self):
        print("valor 1: ", self.__val1)
        print("valor 2: ", self.__val2)
        print("valor Jugable: ", self.val_jugable)
        print("valor Jugado: ", self.val_no_disp)
        
    def compare_to_val(self, val):
        #[x, y] x el valor no disponible
        #y y el valor jugable
        if val == self.__val1:
            return [self.__val1,self.__val2]
        else:
            if val == self.__val2: 
                return [self.__val2, self.__val1]
            else:
                return [-1,-1]
            
    def  Jugar_ficha(self, val_j):
        [self.val_no_disp, self.val_jugable] = self.compare_to_val(val_j)
        if self.val_jugable >= 0:
            return True
        else:
            return False
    
    def getStatus(self, is_Left):
        if is_Left:
            return [self.val_jugable, self.val_no_disp]
        else:
            return [self.val_no_disp, self.val_jugable]

    def primera_Jugada(self, is_Left):
        aux_valJ = -1
        if is_Left:
            aux_valJ = self.__val1
        else:
            aux_valJ = self.__val2
        self.val_jugable = aux_valJ
        return aux_valJ


ficha1 = Ficha(5, 6)

ficha1.print_Atr()

ficha1.Jugar_ficha(6)

ficha1.primera_Jugada(True)
ficha1.primera_Jugada(False)


ficha1.getStatus(True)



        
    