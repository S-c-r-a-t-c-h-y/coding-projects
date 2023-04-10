def nb_1(n : int) -> int:
    """ Fonction récursive qui retourne le nombre de 1
    dans l'écriture binaire de n
    
    :param n: n positif
    """
    
    assert type(n) is int, "Le paramètre doit être un entier"
    assert n >= 0, "Le paramètre doit être positif"
    
    if n <= 1:
        return n
    return n % 2 + nb_1(n // 2)

print(nb_1(15))