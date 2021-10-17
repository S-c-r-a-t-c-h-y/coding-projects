from liste_chainee import *
           
def exemple():
    lc1 = Liste_chainee()
    for i in range(6):
        lc1.placer(i)
    lc1.placer(6, 2)
    lc1.placer(7, 3)
    lc1.placer(8, 5)
    lc1.placer(9, 20)
    print(lc1)
    return lc1

exemple()