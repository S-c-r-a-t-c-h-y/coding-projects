"""
    JEU DE DAME
    JOUEUR CONTRE JOUEUR, INTERFACE CONSOLE
"""

# 1 = pion blanc
# 2 = pion noir
# 3 = dmae blanche
# 4 = dame noire

class Pion:
    
    def __init__(self, valeur: int, i, j):
        self.valeur = valeur # détermine la couleur
        self.i = i
        self.j = j
        
    def __repr__(self):
        return f'Pion({self.valeur}, i={self.i}, j={self.j})'
      
class Board:
    
    def __init__(self):
        self.board = [[Pion(1 if (i%2 + j%2)%2 != 0 else 0, i, j) if j >= 6 else Pion(2 if (i%2 + j%2)%2 != 0 else 0, i, j) if j <= 3 else Pion(0, i, j) for i in range(10)] for j in range(10)]
        
    def is_empty(self):
        return self.board == [[Pion(0, i, j) for i in range(10)] for j in range(10)]
    
    def copy(self):
        new_board = Board()
        new_board.board = self.board
        return new_board
    
    def voisins(self, i, j):
        
        voisins = []
        pion = self.board[j][i]

        nb_iter = 2 if pion.valeur in [1, 2] else 11
        
        for k in range(1, nb_iter):
            if pion.i-k >= 0 and pion.j-k >= 0:
                voisins.append(self.board[pion.j-k][pion.i-k])
            if pion.i-k >= 0 and pion.j+k <= 9:
                voisins.append(self.board[pion.j+k][pion.i-k])
            if pion.i+k <= 9 and pion.j-k >= 0:
                voisins.append(self.board[pion.j-k][pion.i+k])
            if pion.i+k <= 9 and pion.j+k <= 9:
                voisins.append(self.board[pion.j+k][pion.i+k])

        return voisins
    
    def playable_moves_for_pawn(self, i, j):
        
        pion = self.board[j][i]
        
        if pion.valeur == 0: # si il n'y a pas de pion alors on ne peut pas jouer
            return []
        
        voisins = self.voisins(i, j)
        coups = []
        
        if pion.valeur in [1, 2]: # gère les coups possibles pour les pions
            
            cibles = [2, 4] if pion.valeur == 1 else [1, 3]
            offset = -1 if pion.valeur == 1 else 1
            
            coups.extend(((pion.j+offset, pion.i-1), (pion.j+offset, pion.i+1)))
            
            try:
                if (case1 := self.board[pion.j+offset][pion.i-1]).valeur in cibles and case1 in voisins:
                    coups.append((pion.j+offset*2, pion.i-2))
            except IndexError:
                pass
            
            try:   
                if (case1 := self.board[pion.j+offset][pion.i+1]).valeur in cibles and case1 in voisins:
                    coups.append((pion.j+offset*2, pion.i+2))
            except IndexError:
                pass
                
        elif pion.valeur == 3:
            coups.extend([voisin for voisin in self.voisins(i, j) if voisin.j < pion.i])
        elif pion.valeur == 4:
            coups.extend([voisin for voisin in self.voisins(i, j) if voisin.j > pion.i])
                    
        return [(i, j) for j, i in coups if 0 <= i <= 9 and 0 <= j <= 9 and self.board[j][i].valeur == 0]
        
    def move(self, i1, j1, i2, j2) -> bool:
        
        pion = self.board[j1][i1]
        
        if (i2, j2) not in self.playable_moves_for_pawn(i1, j1):
            return False

        if pion.valeur in [1, 2] and pion.i - i2 in [-1, 1] and pion.j - j2 in [-1, 1]:
            self.board[j2][i2] = Pion(pion.valeur, i2, j2)
            self.board[pion.j][pion.i] = Pion(0, pion.i, pion.j)

        elif pion.valeur in [1, 3]:
            for k in range(1, pion.j - j2 + 1):
                if pion.i - i2 > 0:
                    if self.board[pion.j-k][pion.i-k].valeur in [2, 4]:
                        self.board[pion.j-k][pion.i-k] = Pion(0, pion.i-k, pion.j-k)
                elif self.board[pion.j-k][pion.i+k].valeur in [2, 4]:
                    self.board[pion.j-k][pion.i+k] = Pion(0, pion.i+k, pion.j-k)
            self.board[j2][i2] = Pion(pion.valeur, i2, j2)
            
        elif pion.valeur in [2, 4]:
            for k in range(1, j2 - pion.j + 1):
                if pion.i - i2 > 0:
                    if self.board[pion.j+k][pion.i-k].valeur in [1, 3]:
                        self.board[pion.j+k][pion.i-k] = Pion(0, pion.i-k, pion.j+k)
                elif self.board[pion.j+k][pion.i+k].valeur in [1, 3]:
                    self.board[pion.j+k][pion.i+k] = Pion(0, pion.i+k, pion.j+k)
            self.board[j2][i2] = Pion(pion.valeur, i2, j2)
    
        return True

    def __repr__(self):
        repr = ""
        for colon in self.board:
            for pawn in colon:
                repr += " " if pawn.valeur == 0 else str(pawn.valeur)
            repr += '\n'
        repr += '\n'
        return repr
        
        

def jouer():
    board = Board()
    
    tour = 'j1'
    
    while not board.is_empty():
        print(board)
        
        valid = False

        while not valid:
            i = int(input('x : '))
            j = int(input('y : '))
            i2 = int(input('destination x : '))
            j2 = int(input('destination y : '))
            print()
            
            if tour == 'j1' and (case := board.board[j][i]).valeur not in [1, 3]:
                continue
            elif tour == 'j2' and (case := board.board[j][i]).valeur not in [2, 4]:
                continue
            
            valid = board.move(i, j, i2, j2)
            
        tour = 'j1' if tour == 'j2' else 'j2'
            
            
if __name__ == '__main__':
    jouer()