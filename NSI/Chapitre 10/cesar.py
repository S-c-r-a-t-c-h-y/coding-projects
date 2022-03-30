from alphabet import *


def chiffrer_cesar(texte, cle):
    """Fonction qui chiffre le texte en utilisant le code de César
    avec la clé passée en paramètre
    """
    return "".join(majuscule((rang(car) + cle) % 26) for car in texte)


def dechiffrer_cesar(texte, cle):
    """Fonction qui dechiffre le texte en utilisant le code de César
    avec la clé passée en paramètre
    """
    return "".join(majuscule((rang(car) - cle) % 26) for car in texte)


if __name__ == "__main__":
    print(chiffrer_cesar("PYTHON", 3))
    print(dechiffrer_cesar("SBWKRQ", 3))

    print(chiffrer_cesar("BONJOUR", 7))
    print(dechiffrer_cesar("IVUQVBY", 7))
