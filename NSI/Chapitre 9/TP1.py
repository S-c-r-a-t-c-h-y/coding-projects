# coding: utf-8


def somme(n):
    s = 0  # affectation : 1
    compteur = 1
    for i in range(n):
        s += i  # affectation + addition : 2
        compteur += 2
    print(f"{compteur} opérations")
    return s


print(somme(10))
