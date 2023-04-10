def nb_chiffres(n: int) -> int:
    """
    fonction récursive qui prend en paramètre un entier
    naturel n et retourne le nombre de chiffres de cet entier
    
    :param n: n positif
    """
    
    assert type(n) is int, "Le paramètre doit être un entier"
    assert n >= 0, "Le paramètre doit être positif"
    
    if n < 10:
        return 1
    return nb_chiffres(n // 10) + 1

print("\n", nb_chiffres(123456))