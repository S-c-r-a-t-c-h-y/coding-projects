def tri_selection(liste):
    for i in range(len(liste) - 1):
        print(liste)
        k = i
        for j in range(i + 1, len(liste)):
            if liste[j] < liste[k]:
                k = j
        liste[i], liste[k] = liste[k], liste[i]


liste1 = [7, 4, 8, 5, 6, 2, 1, 3]
tri_selection(liste1)
