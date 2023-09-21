from Tiles import Bones
from Tiles import Dominoes_Stack

#------------------------Class Board------------------------#
class Board:
    
    LeftTiles = Dominoes_Stack(True)
    RightTiles = Dominoes_Stack(False)

    playerSet = []
    
    Tiles = []
    
    start_Flag = False
    maximising_turn = False
    
    
    def __init__(self):
        self.create_Tiles()
        
                    
    def create_Tiles(self):
        for i in range(7):
            for j in range(7):
                aBone = Bones(i, j)
                if aBone not in self.Tiles:
                    self.Tiles.append(aBone)
                    
    def print_Tiles(self):
        cad = ""
        for obj in self.Tiles:
            cad += obj.print_values()
        return cad
    
    def add_to_player_set(self, bone):
        if (bone not in self.playerSet) and (bone in self.Tiles):
            self.playerSet.append(bone)
            self.Tiles.remove(bone)
        else:
            print("Cant add to player set, already used on the board")
            
    def set_initial_player_hand(self, bone):
        if len(self.playerSet) < 7:
            self.add_to_player_set(bone)
        else:
            print("Cant add to player set, already full at the beginning")
    
    def remove_from_player_set(self, bone):
        if (bone in self.playerSet):
            self.playerSet.remove(bone)
        else:
            print("Not in player set thus cant remove")
    
    def print_player_set(self):
        Atr = ""
        for obj in self.playerSet:
            Atr += obj.print_values()
        print(Atr)
        return Atr
    
    def show_svaliable_moves(self):
        avaliable = []
        if self.start_Flag:
            for obj in self.playerSet:
                if obj.has_val(self.LeftTiles.top_value()) or obj.has_val(self.RightTiles.top_value()):
                    avaliable.append(obj)
            if not len(avaliable)>0:
                print("No avaliable moves")
        else:
            print("Missing first played piece")
            
            
            
        Atr = ""
        for obj in self.playerSet:
            Atr += obj.print_values()
        print(Atr)
        return Atr
    
            
        
        
        
    
    
    
        
    

        
            
        
#----Tests of class Bones
ficha1 = Bones(0, 0)
ficha1.Atributes()

ficha2 = Bones(4, 6)
ficha2.Atributes()

ficha3 = Bones(2, 6)
ficha3.Atributes()

ficha4 = Bones(2, 2)
ficha4.Atributes()

ficha5 = Bones(1, 1)
ficha5.Atributes()

ficha6 = Bones(1, 2)
ficha6.Atributes()

ficha7 = Bones(3, 5)
ficha7.Atributes()

ficha8 = Bones(4, 4)
ficha8.Atributes()

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

new_Game = Board()
print(new_Game.print_Tiles())
print(len(new_Game.Tiles))

# new_Game.add_to_player_set(ficha1)
new_Game.print_player_set()
# new_Game.remove_from_player_set(ficha1)
# new_Game.remove_from_player_set(ficha2)

new_Game.set_initial_player_hand(ficha1)
new_Game.set_initial_player_hand(ficha2)
new_Game.set_initial_player_hand(ficha3)
new_Game.set_initial_player_hand(ficha4)
new_Game.set_initial_player_hand(ficha5)
new_Game.set_initial_player_hand(ficha6)
new_Game.set_initial_player_hand(ficha7)
new_Game.set_initial_player_hand(ficha8)
