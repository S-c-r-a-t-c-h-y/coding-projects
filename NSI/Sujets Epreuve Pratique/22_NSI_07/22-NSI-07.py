def conv_bin(n):
    b = []
    while n > 0:
        b.append(n%2)
        n //= 2
    b.reverse()
    return b, len(b)

# print(conv_bin(9))

def tri_bulles(T):
    n = len(T)
    for i in range(n-1,0,-1):
        for j in range(i):
            if T[j] > T[j+1]:
                temp = T[j]
                T[j] = T[j+1]
                T[j+1] = temp
    return T

print(tri_bulles([9, 8, 7, 6, 5, 4, 3, 2, 1]))
print(tri_bulles([1, 4, 8, 2, 3, 0, 7, -1]))