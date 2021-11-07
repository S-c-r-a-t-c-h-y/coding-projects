
values = {}
def s(n):
    """ calcul la nième valeur de la suite de Stern-Brocot """
    if n in values:
        return values[n]
    if n <= 1:
        v = n
    elif n % 2 == 0:
        v = s(n//2)
    else:
        v = s(n//2) + s(n//2 + 1)
    values[n] = v
    return v


# for i in range(51):
#     print(f's({i}) = {s(i)}')

print(f"{s(10**20) = }")
print(f"{s(10**30) = }")
print(f"{s(10**40) = }")
print(f"{s(10**50) = }")