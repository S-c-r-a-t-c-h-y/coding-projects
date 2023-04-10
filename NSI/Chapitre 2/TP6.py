def syracuse(n):
    """ fonction récursive qui retourne la valeur
    de la suite de Syracuse au rang n """
    
    if n == 0:
        return 10
    if (u := syracuse(n-1)) % 2:
        return 3 * u + 1
    else:
        return u/2
    
for i in range(16):
    print(f'syracuse({i}) = {syracuse(i)}')