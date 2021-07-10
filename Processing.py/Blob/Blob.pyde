from blob import *
from branch import *

b = None

def setup():
    global b
    size(600, 600)
    b = Blob(width / 2, height / 2, 8, 1)
    
def draw():
    background(51)
    
    b.show()
    b.update()
