from pile import Pile


def f(n):
    """ calcul le nième terme de la suite de fibonacci """
    
    p = Pile()
    p.empiler(n)
    
    f = 0
    
    while not(p.est_vide()):
        print(p, f)
        s = p.depiler()
        if s <= 1:
            f += s
        else:
            p.empiler(s-1)
            p.empiler(s-2)
            
    return f

print(f(5))