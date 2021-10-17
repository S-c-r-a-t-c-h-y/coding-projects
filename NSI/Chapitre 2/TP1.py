def factorielle(n):
    """Fonction récursive qui renvoie la valeur
       n! = 1 x 2 x 3 x ... x n
    """
    if n == 0:
        return 1
    return n * factorielle(n - 1)
    
for i in range(7):
    print('Factorielle(', i, ') =', factorielle(i))