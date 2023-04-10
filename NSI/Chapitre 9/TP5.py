from random import randint


def tri_insertion(liste):
    compteur = 0
    for i in range(len(liste) - 1):
        val = liste[i + 1]

        j = i
        while j >= 0 and liste[j] > val:
            liste[j + 1] = liste[j]
            j -= 1
            compteur += 1

        liste[j + 1] = val

    return compteur


taille = int(input("Saisir la taille de la liste : "))
somme = 0
for _ in range(10):
    liste1 = [2 * n for n in range(taille)]
    liste1.reverse()
    somme += tri_insertion(liste1)

moyenne = somme // 10
print(moyenne)
print(0.5 * taille ** 2 - 0.5 * taille)
