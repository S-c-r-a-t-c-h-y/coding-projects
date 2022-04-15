def verifie(tab):
    if len(tab) <= 1:
        return True
    for i in range(1, len(tab)):
        if tab[i] < tab[i - 1]:
            return False
    return True


def test1():
    assert verifie([0, 5, 8, 8, 9]) is True
    assert verifie([8, 12, 4]) is False
    assert verifie([-1, 4]) is True
    assert verifie([5]) is True


def depouille(urne):
    resultat = {}
    for bulletin in urne:
        if bulletin in resultat:
            resultat[bulletin] = resultat[bulletin] + 1
        else:
            resultat[bulletin] = 1
    return resultat


def vainqueur(election):
    vainqueur = ""
    nmax = 0
    for candidat in election:
        if election[candidat] > nmax:
            nmax = election[candidat]
            vainqueur = candidat
    liste_finale = [nom for nom in election if election[nom] == nmax]
    return liste_finale


def test2():
    urne = ["A", "A", "A", "B", "C", "B", "C", "B", "C", "B"]
    election = depouille(urne)
    assert election == {"B": 4, "A": 3, "C": 3}
    assert vainqueur(election) == ["B"]


if __name__ == "__main__":
    test1()
    test2()
