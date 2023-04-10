from alphabet import *


def inverse_modulo(n, modulo=26):
    m = 0
    while (n * m) % modulo != 1:
        m += 1
    return m


def chiffrer_affine(texte, a, b):
    return "".join(majuscule((a * rang(car) + b) % 26) for car in texte)


def dechiffrer_affine(texte, a, b):
    a1 = inverse_modulo(a)
    b1 = -a1 * b

    return "".join(majuscule((a1 * rang(car) + b1) % 26) for car in texte)


if __name__ == "__main__":
    print(chiffrer_affine("LAC", 3, 5))
    print(dechiffrer_affine("MFL", 3, 5))

    print(chiffrer_affine("PYTHON", 5, 11))
    print(dechiffrer_affine("IBCUDY", 5, 11))