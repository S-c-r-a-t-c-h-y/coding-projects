def rechercher1(e, liste):
    for elem in liste:
        if elem == e:
            return True
    return False

def test():
    liste1 = list(range(100))
    print("recherche1 :", rechercher1(48, liste1))
    print("recherche2 :", rechercher1(150, liste1))
    
if __name__ == '__main__':
    test()