# www.enseignement.polytechnique.fr/informatique/profs/Georges.Gonthier/pi98/compte.html

import random


class Arbre:
    def __init__(self, val, parent=None, op=None, operande=None):
        self.val = val
        self.parent = parent
        self.op = op
        self.operande = operande

    def elder(self):
        return self if self.parent is None else self.parent.elder()

    def __len__(self):
        if self.parent is None:
            return 1
        return 1 + len(self.parent)

    def __repr__(self):
        return f"Arbre({self.val}, {self.parent}, {self.op}, {self.operande})"


ensemble_plaques = list(range(1, 11)) * 2 + [25, 50, 75, 100] * 2
operations = "*+-/"


def sequence(but, plaques):
    trees = []

    def create_trees(arbre, plaques):
        resultats = []
        for i, plaque in enumerate(plaques):
            for op in operations:
                res = eval(f"{arbre.val}{op}{plaque}")
                ab = Arbre(res, arbre, op, plaque)

                if res == 0:
                    trees.append(ab)
                    return [True]
                elif len(plaques) == 1:
                    resultats.append(False)
                elif res != int(res) or res < 0:
                    resultats.append(False)
                else:
                    pl = plaques[:i] + plaques[i + 1 :]
                    resultats.append(True in create_trees(ab, pl))

        return resultats

    create_trees(Arbre(but), plaques)
    if not trees:
        return None
    return list(sorted(trees, key=lambda x: len(x)))[0]


def main():
    def afficher(arbre):
        arbre = arbre.parent
        res = int(arbre.val)
        while arbre.parent is not None:
            rep = f"{res} {operations[-(operations.index(arbre.op)+1)]} {arbre.operande}"
            res = int(eval(rep))
            print(f"{rep} = {res}")
            arbre = arbre.parent

    continuer = True
    while continuer:
        plaques = random.sample(ensemble_plaques, 6)
        nombre_init = random.randint(100, 999)
        plaques.sort()

        print(f"Nombre à trouver : {nombre_init}")
        print("Voici le tirage :", ", ".join(map(str, plaques)), "\n")

        op = "+"
        increment = 1
        nombre = nombre_init

        while (seq := sequence(nombre, plaques)) is None:
            nombre = eval(f"nombre{op}{increment}")
            op = "+" if op == "-" else "-"
            increment += 1

        if nombre_init == (val := seq.elder().val):
            print(f"Le compte est bon en {len(seq)-1} plaques!")
        else:
            print(f"J'ai trouvé {val}.")
        afficher(seq)

        continuer = (
            True
            if (rep := input("\nVoulez-vous continuer (O ou N) ? ").lower()) == "o"
            else False
            if rep == "n"
            else None
        )
        if continuer is None:
            print("Réponse invalide.")
            break
        print()


if __name__ == "__main__":
    main()
