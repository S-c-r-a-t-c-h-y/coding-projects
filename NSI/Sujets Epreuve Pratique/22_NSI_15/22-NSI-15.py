def nb_repetions(elt, tab):
    return tab.count(elt)


def nb_repetions(elt, tab):
    repetition = 0
    for elem in tab:
        if elem == elt:
            repetition += 1
    return repetition


# print(nb_repetions(5, [2, 5, 3, 5, 6, 9, 5]))


def binaire(a):
    bin_a = str(a % 2)
    a = a // 2
    while a >= 1:
        bin_a = str(a % 2) + bin_a
        a //= 2
    return bin_a

print(binaire(0))
print(binaire(77))