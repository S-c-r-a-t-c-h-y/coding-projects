def occurences(sequence):
    dico = {}
    for element in sequence:
        if element in dico:
            dico[element] += 1
        else:
            dico[element] = 1
        
    return dico

print(occurences('radar'))
print(occurences([1, 1, 1, 2, 2, 5]))
print(occurences(('a', 'a', 5, True, True, True)))