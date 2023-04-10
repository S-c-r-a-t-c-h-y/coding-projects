import itertools
from typing import List


def desequilibre(accroches: List[int]) -> int:
    return (max(accroches) - min(accroches)) ** 2


def stabilite(accroches: List[int], p: int) -> int:
    return p - desequilibre(accroches)


def possibilites(accroches: List[int]) -> List[List[int]]:
    n = len(accroches)
    if n < 4:
        return []
    accs = []
    for i, j, l, m in itertools.product(range(n), range(n), range(n), range(n)):
        if j == i or l in {i, j} or m in {i, j, l}:
            continue
        combi = [sorted([accroches[i], accroches[j], accroches[l], accroches[m]])]
        if combi not in accs:
            accs.append(combi)
    return accs


def stabilite_maximale(n: int, k: int, p: int, accroches: List[int]) -> int:
    """
    :param n: nombre d'accroches
    :param k: nombre de stabilisateurs
    :param p: indice de stabilité parfaite
    :param accroches: hauteur de chaque accroche
    """
    # TODO Afficher l'indice de stabilité maximal obtenable.
    # if len(accroches) <= 3 : return 0
    # if len(accroches) == 4: return stabilite(accroches, p)

    # accroches.sort()
    accs = possibilites(accroches)
    debut = 0
    fin = len(accs)
    for _ in range(k - 1):
        new_accs = []
        for i in range(debut, fin):
            poss = possibilites([e for e in accroches if e not in accs[i][0]])
        debut = fin
        fin = len(accs)

    return max(sum(stabilite(a, p) for a in acc) for acc in accs)


if __name__ == "__main__":
    # n = int(input())
    n = 9
    n = 10
    # k = int(input())
    k = 2
    k = 3
    # p = int(input())
    p = 10
    p = 100
    # accroches = list(map(int, input().split()))
    accroches = [3, 1, 4, 5, 5, 9, 2, 5, 7]
    accroches = [3, 1, 4, 4, 5, 9, 2, 6, 7, 4]
    print(stabilite_maximale(n, k, p, accroches))
