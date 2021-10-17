from pile import Pile


def evaluer(chaine) :
    """ Fonction qui évalue le résultat d'une expression en NPI"""
    pile1 = Pile()
    for c in chaine :
        if c in '+-*' :
            op2 = pile1.depiler()
            op1 = pile1.depiler()
            pile1.empiler(eval(f'{op1} {c} {op2}'))
        elif c != ' ' :
            pile1.empiler(int(c))
            pile1.afficher()
    return pile1.depiler()


print('Entrer une expression en NPI :')
expression = input()
print(evaluer(expression))