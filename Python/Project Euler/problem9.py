# https://fr.wikipedia.org/wiki/Triplet_pythagoricien#Th%C3%A9or%C3%A8me_fondamental_d%C3%A9crivant_tous_les_triplets_primitifs

p = 3
q = 1
go = True

while go:

    p += 1
    q = 1 if p % 2 == 0 else 2

    while q < p:
        a = p ** 2 - q ** 2
        b = 2 * p * q
        c = p ** 2 + q ** 2

        if a + b + c == 1000:
            go = False
            break

        q += 2

print(a, b, c)
print(a * b * c)
