from liste_chainee import *
           
def exemple():
    lc1 = Liste_chainee()
    for i in range(6):
        lc1.placer(i)
    print(lc1)
    return lc1

lc1 = exemple()
lc1.placer_fin(8)
print(lc1)