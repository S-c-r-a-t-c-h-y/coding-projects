def tri_bulle(liste: list):
    nb_permutation = 1
    while nb_permutation:
        print()
        nb_permutation = 0
        for i in range(len(liste) - 1):
            if liste[i] > liste[i + 1]:
                liste[i], liste[i + 1] = liste[i + 1], liste[i]
                nb_permutation += 1
            print(liste)


def tri_bulle_nb_itération(liste: list):
    nb_permutation = 1
    nb_iterations = 0
    while nb_permutation:
        nb_permutation = 0
        for i in range(len(liste) - 1):
            nb_iterations += 1
            if liste[i] > liste[i + 1]:
                liste[i], liste[i + 1] = liste[i + 1], liste[i]
                nb_permutation += 1
    return nb_iterations


def tri_rapide(liste: list):
    if len(liste) <= 1:
        return liste

    pivot = liste[0]
    liste1 = []
    liste2 = []

    for elem in liste[1:]:
        if elem <= pivot:
            liste1.append(elem)
        else:
            liste2.append(elem)

    liste = tri_rapide(liste1)
    liste.append(pivot)
    liste.extend(tri_rapide(liste2))
    return liste


# print(tri_bulle_nb_itération(list(range(10, 0, -1))))
# print(tri_bulle_nb_itération(list(range(20, 0, -1))))
# print(tri_bulle_nb_itération(list(range(50, 0, -1))))
# print(tri_bulle_nb_itération(list(range(100, 0, -1))))
# print(tri_bulle_nb_itération(list(range(500, 0, -1))))
# print(tri_bulle_nb_itération(list(range(1000, 0, -1))))

print(tri_rapide([9, 6, 2, 3, 8, 5, 1, 4, 0, 7]))
