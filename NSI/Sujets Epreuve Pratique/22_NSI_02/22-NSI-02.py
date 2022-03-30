def moyenne(note_avec_coeffs):
    somme = 0
    somme_coeffs = 0
    for note, coeff in note_avec_coeffs:
        somme += note * coeff
        somme_coeffs += coeff
    return somme / somme_coeffs


def pascal(n):
    C= [[1]]
    for k in range(1,n+1):
        Ck = [1]
        for i in range(1,k):
            Ck.append(C[k-1][i-1]+C[k-1][i] )
        Ck.append(1)
        C.append(Ck)
    return C

print(pascal(5))