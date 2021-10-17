def palindrome(chaine):
    """Fonction récursive qui teste si la chaine donnée
       en paramètre est un palindrome
    """
    if len(chaine) == 1:
        return True
    elif len(chaine) == 2:
        return chaine[0] == chaine[-1]
    return False not in [chaine[0] == chaine[-1], palindrome(chaine[1:-1])]

    
print(palindrome('carte'))
print(palindrome('radar'))
print(palindrome('serres'))
print(palindrome('rester'))
