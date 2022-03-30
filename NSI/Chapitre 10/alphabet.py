def rang(c):
    """Fonction qui retourne le rang dans l'alphabet majuscule
    du caractère c passé en paramètre
    """
    return ord(c) - 65


def majuscule(n):
    """Fonction qui retourne la lettre majuscule de rang n"""
    return chr(n + 65)


if __name__ == "__main__":
    print(rang("A"))
    print(rang("B"))
    print(rang("Z"))
    print(majuscule(0))
    print(majuscule(25))
