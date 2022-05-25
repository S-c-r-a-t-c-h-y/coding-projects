from random import randint
from pprint import pprint

def creer_tableau(n, m, min=1, max=9):
    return [[randint(min, max) for _ in range(n)] for _ in range(m)]


def max_recursif(tableau, i=0, j=None):
    """
    Fonction recursive trouvant le chemin avec la somme maximale dans le tableau
    i et j sont les bornes des cases atteignables lors du parcours    
    """
    n, m = len(tableau[0]), len(tableau)
    if j is None:
        j = n - 1
    
    if m == 1:
        return max(tableau[0][i:j+1])
    
    vmax = -1
    for k in range(i, j+1):
        vmax = max(vmax, tableau[0][k] + max_recursif(tableau[1:], max(0, k-1), min(n-1, k+1)))
    return vmax

memo = {}
def max_recursif_memo(tableau, i=0, j=None, i_global=0):
    """
    Fonction recursive trouvant le chemin avec la somme maximale dans le tableau
    i et j sont les bornes des cases atteignables lors du parcours    
    """
    n, m = len(tableau[0]), len(tableau)
    if j is None:
        j = n - 1
    
    if m == 1:
        return max(tableau[0][i:j+1])
    
    vmax = -1
    for k in range(i, j+1):
        if (i_global, k) in memo:
            val = memo[(i_global, k)]
        else:    
            new_i, new_j = max(0, k-1), min(n-1, k+1)
            val = tableau[0][k] + max_recursif_memo(tableau[1:], new_i, new_j, i_global+1)
        vmax = max(vmax, val)
        memo[(i_global, k)] = vmax
    return vmax

def max_ascendant(tableau):
    n, m = len(tableau[0]), len(tableau)
    memo = {(m-1, k): tableau[m-1][k] for k in range(n)}
    for j in range(2, m+1):
        for i in range(n):
            vmax = -1
            for k in range(max(0, i-1), min(n-1, i+1)+1):
                vmax = max(vmax, tableau[m-j][i] + memo[(m-j+1, k)])
            memo[(m-j, i)] = vmax
    return max(value for key, value in memo.items() if key[0] == 0)
    
    
tableau = creer_tableau(4, 7)
pprint(tableau)
print(max_ascendant(tableau))
# print(max_recursif(tableau))
# print(max_recursif_memo(tableau))