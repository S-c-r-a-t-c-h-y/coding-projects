def tri_insertion(liste):
    for i in range(len(liste) - 1):
        print(liste)
        val = liste[i + 1]

        j = i
        while j >= 0 and liste[j] > val:
            liste[j + 1] = liste[j]
            j -= 1

        liste[j + 1] = val


liste1 = [7, 4, 8, 5, 6, 2, 1, 3]
tri_insertion(liste1)
