"""
    JEU DE DAME
    JOUEUR CONTRE MINIMAX
    PAS D'OPTIMISATION
"""

from copy import deepcopy

# 1 = pion blanc
# 2 = pion noir
# 3 = dmae blanche
# 4 = dame noire

class Pion:
    
    def __init__(self, valeur: int, i, j):
        self.valeur = valeur # détermine la couleur
        self.i = i
        self.j = j
        
    def voisins(self, board):
        """ retourne les voisins du pion sur la grille """
        
        voisins = []

        if self.valeur in [1, 2]:
            for voisin in [board[self.j-1][self.i-1], board[self.j-1][self.i+1], board[self.j+1][self.i-1], board[self.j+1][self.i+1]]:
                if self.i - voisin.i in [-1, 1] and self.j - voisin.j in [-1, 1]:
                    voisins.append(voisin)
        else:
            for k in range(1, 11):
                if self.i-k >= 0 and self.j-k >= 0:
                    voisins.append(board[self.j-k][self.i-k])
                if self.i-k >= 0 and self.j+k <= 9:
                    voisins.append(board[self.j+k][self.i-k])
                if self.i+k <= 9 and self.j-k >= 0:
                    voisins.append(board[self.j-k][self.i+k])
                if self.i+k <= 9 and self.j+k <= 9:
                    voisins.append(board[self.j+k][self.i+k])

        return voisins
        
    def coups_jouables(self, board):
        
        if self.valeur == 0: # si il n'y a pas de pion alors on ne peut pas jouer
            return []
        
        voisins = self.voisins(board)
        coups = []
        
        if self.valeur in [1, 2]: # gère les coups possibles pour les pions
            
            cibles = [2, 4] if self.valeur == 1 else [1, 3]
            offset = -1 if self.valeur == 1 else 1
            
            coups.extend((board[self.j+offset][self.i-1], board[self.j+offset][self.i+1]))
            
            if (case1 := board[self.j+offset][self.i-1]).valeur in cibles and case1 in voisins:
                coups.append(board[self.j+offset*2][self.i-2])
                
            if (case1 := board[self.j+offset][self.i+1]).valeur in cibles and case1 in voisins:
                coups.append(board[self.j+offset*2][self.i+2])
                
        elif self.valeur == 3:
            coups.extend([voisin for voisin in self.voisins(board) if voisin.j < self.i])
        elif self.valeur == 4:
            coups.extend([voisin for voisin in self.voisins(board) if voisin.j > self.i])
                    
        return [coup for coup in coups if coup.valeur == 0]
        
    def deplacer(self, i, j, board) -> bool:

        if board[j][i] not in self.coups_jouables(board):
            return False

        if self.valeur in [1, 2] and self.i - i in [-1, 1] and self.j - j in [-1, 1]:
            board[j][i] = Pion(self.valeur, i, j)
            board[self.j][self.i] = Pion(0, self.i, self.j)

        elif self.valeur in [1, 3]:
            for k in range(1, self.j - j + 1):
                if self.i - i > 0:
                    if board[self.j-k][self.i-k].valeur in [2, 4]:
                        board[self.j-k][self.i-k] = Pion(0, self.i-k, self.j-k)
                elif board[self.j-k][self.i+k].valeur in [2, 4]:
                    board[self.j-k][self.i+k] = Pion(0, self.i+k, self.j-k)
            board[j][i] = Pion(self.valeur, i, j)
            
        elif self.valeur in [2, 4]:
            for k in range(1, j - self.j + 1):
                if self.i - i > 0:
                    if board[self.j+k][self.i-k].valeur in [1, 3]:
                        board[self.j+k][self.i-k] = Pion(0, self.i-k, self.j+k)
                elif board[self.j+k][self.i+k].valeur in [1, 3]:
                    board[self.j+k][self.i+k] = Pion(0, self.i+k, self.j+k)
            board[j][i] = Pion(self.valeur, i, j)
    
        return True
        
    def __repr__(self):
        return f'Pion({self.valeur}, i={self.i}, j={self.j})'
      
        
board = [[Pion(1 if (i%2 + j%2)%2 != 0 else 0, i, j) if j >= 6 else Pion(2 if (i%2 + j%2)%2 != 0 else 0, i, j) if j <= 3 else Pion(0, i, j) for i in range(10)] for j in range(10)]

def childrens(board):
    childrens = []
    for col in board:
        for pion in col:
            if pion.valeur != 0:
                for mvt in pion.coups_jouables(board):
                    new_board = deepcopy(board)
                    pion.deplacer(mvt.i, mvt.j, new_board)
                    childrens.append(new_board)
    return childrens         

def evaluate_board(board):
    nb_white_pawn = nb_black_pawn = nb_white_queen = nb_black_queen = 0
    for col in board:
        for elem in col:
            if elem.valeur == 1:
                nb_white_pawn += 1
            elif elem.valeur == 2:
                nb_black_pawn += 1
            elif elem.valeur == 3:
                nb_white_queen += 1
            elif elem.valeur == 4:
                nb_black_queen += 1
    
    return nb_white_pawn + nb_white_queen * 5 - (nb_black_pawn + nb_black_queen * 5)

def minimax(board, depth: int, maximizing: bool):
    if depth == 0 or board_is_empty(board):
        return evaluate_board(board)
    
    if maximizing:
        max_eval = float('-inf')
        for child in childrens(board):
            eval = minimax(child, depth - 1, False)
            max_eval = max(eval, max_eval)
        return max_eval
    
    else:
        min_eval = float('inf')
        for child in childrens(board):
            eval = minimax(child, depth - 1, True)
            min_eval = min(eval, min_eval)
        return min_eval
    
def find_best_movement(board, maximizing, depth):
    best_move = float('-inf')
    new_board = None
    for child in childrens(board):
        if (eval := minimax(child, depth, maximizing)) > best_move:
            best_move = eval
            new_board = child
    return new_board

def board_is_empty(board) -> bool:
    return board == [[Pion(0, i, j) for i in range(10)] for j in range(10)]

def print_board():
    for col in board:
        for elem in col:
            print(f'{elem.valeur if elem.valeur != 0 else " "}', end=' ')
        print()
    print()

def jouer():
    global board
    tour = 'j1'
    
    while not board_is_empty(board):
        print_board()
        
        valid = False

        if tour == 'j1':
            while not valid:
                i = int(input('x : '))
                j = int(input('y : '))
                i2 = int(input('destination x : '))
                j2 = int(input('destination y : '))
                print()
                
                if tour == 'j1' and (case := board[j][i]).valeur not in [1, 3]:
                    continue
                elif tour == 'j2' and (case := board[j][i]).valeur not in [2, 4]:
                    continue
                
                valid = board[j][i].deplacer(i2, j2, board)
        else:
            new_board = find_best_movement(board, False, 3)
            board = new_board
            
        tour = 'j1' if tour == 'j2' else 'j2'
            
        
        

if __name__ == '__main__':
    jouer()