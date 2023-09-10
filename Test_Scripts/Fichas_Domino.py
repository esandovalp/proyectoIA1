#------------Class Bones------------#   
class Bones:
    #Bone refers to the name of each domino piece
    __val1 = -1
    __val2 = -1
        #This variables has been initialized to -1 as the piece has not been played yet.
    played_value = -1
    playable_value = -1
    
#Constructor
    def __init__(self, valor1, valor2):
        self.__val1 = max(valor1, valor2)
        self.__val2 = min(valor1, valor2)
        
 #Getters and Setters
    def get_val1(self):
        return self.__val1
    
    def set_val1(self, aux_val):
        self.__val1 = aux_val
    
    def get_val2(self):
        return self.__val2
    
    def set_val2(self, aux_va2):
        self.__val2 = aux_va2

    def get_Status(self):
        return [self.playable_value, self.played_value]
    
    def print_for_game(self):
        atr = "["+str(self.played_value) + ":" + str(self.playable_value)+"], "
        return atr
    
    def get_playable_value(self):
        return self.playable_value
    
#toString   
    def Atributes (self):
        atr = ""
        atr += "\nvalor 1: " + str(self.__val1)
        atr += "\nvalor 2: " + str(self.__val2)
        atr += "\nvalor Jugado: " + str(self.played_value)
        atr += "\n\tvalor Jugable: " + str(self.playable_value)
        print(atr)
        
#CompareTo
    #returns [x, y] where x and y refers to played and playable values        
    def compare_to_val(self, val):
        if val == self.__val1:
            return [self.__val1,self.__val2]
        else:
            if val == self.__val2: 
                return [self.__val2, self.__val1]
            else:
                return [-1,-1]
            
    def __eq__(self, other):
        return (self.__val1, self.__val2) == (other.__val1, other.__val2)
    
#Play_piece            
    #Set the values of played and playable variables            
    def  play_piece(self, val_j):
        [self.played_value, self.playable_value] = self.compare_to_val(val_j)
        if self.playable_value >= 0:
            return True
        else:
            return False
        
#first_in_game
    #Set the piece as the first played piece
    def first_in_game(self, is_Left):
        aux_valJ = -1
        aux_valNoJ = -1
        if is_Left:
            aux_valJ = self.__val1
            aux_valNoJ = self.__val2
        else:
            aux_valJ = self.__val2
            aux_valNoJ = self.__val1

        self.playable_value = aux_valJ
        self.played_value = aux_valNoJ
        return aux_valJ
    
 #------------Class Bones------------#   
class Dominoes_Stack:
    d_Stack = []
    top_piece = Bones(-1, -1)
    left_flag = False
    def __init__(self, isLeft):
        self.left_flag = isLeft

    def is_empty(self):
        return len(self.d_Stack)==0
    
    def size(self):
        return len(self.d_Stack)

    def top(self):
        return self.top_piece
    
    def top_value(self):
        return self.top_piece.get_playable_value()
    
#return true if the piece is already on the stack
    def alredy_in_stack(self, bone):
        already = False
        for auxBone in self.d_Stack:
            if auxBone == bone:
                already = True
        return already
    
#return true if the piece is pushed to the stack
    def push(self, bone):
        if not(self.alredy_in_stack(bone)):
            self.d_Stack.append(bone)
            self.top_piece = bone
            return True
        else:
            return False
        
    def pop(self):
        return self.d_Stack.pop(self.size()-1)
    
    def display_game_stack(self):
        Atr = ""
        for auxBone in self.d_Stack:
            Atr += auxBone.print_for_game()
        return Atr
    
    def push_piece(self, bone):
        if not(self.alredy_in_stack(bone)):
            if bone.play_piece(self.top_value()):
                self.push(bone)
            else:
                return "Error: No coincidence"
        else:
            return "Error: Already played"

    def place_first(self, bone):
        if not(self.alredy_in_stack(bone)):
            bone.first_in_game(self.left_flag)
            self.push(bone)
        else:
            return "Error: Already played"
        
        
            
        
#----Tests of class Bones
ficha1 = Bones(5, 6)
ficha1.Atributes()

ficha2 = Bones(4, 6)
ficha2.Atributes()

ficha3 = Bones(2, 6)
ficha3.Atributes()

ficha4 = Bones(2, 2)
ficha4.Atributes()

ficha5 = Bones(1, 1)
ficha5.Atributes()

ficha1 == ficha3
    # ficha1.play_piece(6)

    # ficha1.first_in_game(True)
    # ficha1.first_in_game(False)

    # ficha1.get_Status(True)
#----Tests of class Stack
s_Izq = Dominoes_Stack(False)
print(s_Izq.is_empty())
print(s_Izq.size())
    # s_Izq.push(ficha3)
    # print(s_Izq.alredy_in_stack(ficha2))
    # s_Izq.push(ficha2)
    # s_Izq.top().Atributes()
    # s_Izq.push(ficha4)
    # s_Izq.top().Atributes()
s_Izq.display_game_stack()
s_Izq.top_value()
    # s_Izq.top_value()
    # fichaAux = s_Izq.pop()
    # fichaAux.Atributes()

s_Izq.place_first(ficha4)
s_Izq.push_piece(ficha3)
s_Izq.push_piece(ficha3)
s_Izq.push_piece(ficha2)
s_Izq.push_piece(ficha5)

        
    