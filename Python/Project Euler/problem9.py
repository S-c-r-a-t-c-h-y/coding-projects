def is_triplet(a, b, c):
    return a ** 2 + b ** 2 == c ** 2


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
