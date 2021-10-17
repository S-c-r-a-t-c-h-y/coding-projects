
values = {}
def s(n):
    """ calcul la nième valeur de la suite de Stern-Brocot """
    
    if n <= 1:
        return n
    if n in values:
        return values[n]
    if n % 2 == 0:
        res = s(n//2)
        values[n] = res
        return res
    res = s(n//2) + s(n//2 + 1)
    values[n] = res
    return res


# for i in range(51):
#     print(f's({i}) = {s(i)}')

print(f"{s(10**20) = }")
print(f"{s(10**30) = }")
print(f"{s(10**40) = }")
print(f"{s(10**50) = }")