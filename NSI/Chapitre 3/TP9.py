from file import File
from pile import Pile

def inversion(p):
    """ fonction qui inverse une pile """
    
    f = File()
    while not(p.est_vide()):
        f.enfiler(p.depiler())
        
    while not(f.est_vide()):
        p.empiler(f.defiler())

p = Pile([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(f"pile avant :\n{p}")

inversion(p)
print(f"pile après :\n{p}")