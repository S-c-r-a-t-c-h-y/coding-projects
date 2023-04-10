def tri_insertion(liste):
    for i in range(len(liste) - 1):
        val = liste[i + 1]

        j = i
        while j >= 0 and liste[j] > val:
            liste[j + 1] = liste[j]
            j -= 1

        liste[j + 1] = val
