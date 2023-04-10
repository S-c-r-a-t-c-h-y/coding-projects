def tri_selection(liste):
    for i in range(len(liste) - 1):
        k = i
        for j in range(i + 1, len(liste)):
            if liste[j] < liste[k]:
                k = j
        liste[i], liste[k] = liste[k], liste[i]
