from file import File


def hamming(n) :
    """ Fonction qui retourne les n premiers nombres de Hamming"""
    rep = []
    file2 = File()
    file3 = File()
    file5 = File()
    
    file2.enfiler(1)
    file3.enfiler(1)
    file5.enfiler(1)
    
    def min_files():
        m = min(file2.sommet(), file3.sommet(), file5.sommet())
        
        if m == file2.sommet():
            file2.defiler()
        if m == file3.sommet():
            file3.defiler()
        if m == file5.sommet():
            file5.defiler()
        return m
    
    for _ in range(n):
        m = min_files()
        
        rep.append(m)
        file2.enfiler(2 * m)
        file3.enfiler(3 * m)
        file5.enfiler(5 * m)
    
    return rep

print(hamming(20))