from liste_chainee import *
           
def exemple():
    lc1 = Liste_chainee()
    lc1.placer(8)
    lc1.placer(0)
    lc1.placer(2)
    lc1.enlever()
    lc1.placer(3)
    lc1.placer(7)
    lc1.enlever()
    lc1.placer(4)
    lc1.placer(6)
    print(lc1)
    return lc1

lc1 = exemple()