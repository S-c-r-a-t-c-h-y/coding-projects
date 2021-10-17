def somme(n):
    """Fonction récursive qui renvoie la valeur
       Sn = 1 + 2 + 3 + ... + n
    """
    if n == 0:
        return 0
    return n + somme(n - 1)
    
for i in range(11):
    print('Somme(', i, ') =', somme(i))