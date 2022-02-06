from random import randint


def tri_selection(liste):
    compteur = 0
    for i in range(len(liste) - 1):
        k = i
        for j in range(i + 1, len(liste)):
            compteur += 1
            if liste[j] < liste[k]:
                k = j
        liste[i], liste[k] = liste[k], liste[i]
    return compteur


taille = int(input("Saisir la taille de la liste : "))
somme = 0
for _ in range(10):
    liste1 = [randint(0, 2 * taille) for _ in range(taille)]
    somme += tri_selection(liste1)

moyenne = somme // 10
print(moyenne)
print(0.5 * taille ** 2 - 0.5 * taille)
