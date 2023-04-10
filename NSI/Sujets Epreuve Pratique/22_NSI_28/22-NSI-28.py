def moyenne(tab):
    return sum(tab) / len(tab)


def moyenne(tab):
    somme = 0
    for nombre in tab:
        somme += nombre
    return somme / len(tab)

# print(moyenne([1.0, 2.0, 4.0]))


def dec_to_bin(a):
    bin_a = str(a%2)
    a = a//2
    while a > 0 :
        bin_a = str(a%2) + bin_a
        a = a // 2
    return bin_a

print(dec_to_bin(83))
print(dec_to_bin(127))