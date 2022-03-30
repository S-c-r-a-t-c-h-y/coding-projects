from alphabet import *


def chiffrer_vigenere(texte, cle):
    """Fonction qui chiffre le texte en utilisant le code de Vigenère
    avec la clé passée en paramètre
    """
    return "".join(majuscule((rang(car) + rang(cle[i % len(cle)])) % 26) for i, car in enumerate(texte))


def dechiffrer_vigenere(texte, cle):
    """Fonction qui chiffre le texte en utilisant le code de Vigenère
    avec la clé passée en paramètre
    """
    return "".join(majuscule((rang(car) - rang(cle[i % len(cle)])) % 26) for i, car in enumerate(texte))


if __name__ == "__main__":
    print(chiffrer_vigenere("PYTHON", "NSI"))
    print(dechiffrer_vigenere("CQBUGV", "NSI"))

    print(chiffrer_vigenere("MATH", "BC"))
    print(dechiffrer_vigenere("NCUJ", "BC"))
