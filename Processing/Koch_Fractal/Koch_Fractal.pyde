
steps = 5
l = 500

def setup():
    size(600,600)
    
def draw():
    background(51)
    stroke(255)
    translate(l/steps/2, l/steps*1.5)
    
    koch(l, steps)
    rotate(radians(120))
    koch(l, steps)
    rotate(radians(120))
    koch(l, steps)
    
    
    

def koch(l, n):
    if n <= 0:
        line(0, 0, l, 0)
        translate(l, 0)
    else:
        koch(l/3, n-1)
        rotate(radians(-60))
        koch(l/3, n-1)
        rotate(radians(120))
        koch(l/3, n-1)
        rotate(radians(-60))
        koch(l/3, n-1)
