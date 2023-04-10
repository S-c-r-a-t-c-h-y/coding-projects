from attractor import *

attractor = Attractor(1, 0, 0, 28, 10, 8/3, 0.01)

def setup():
    size(500, 500, P3D)
    background(0)
    attractor.display()
    
def draw():
    background(0)
    translate(width/2, height/2)
    scale(5)
    attractor.update()
    attractor.display()
    
