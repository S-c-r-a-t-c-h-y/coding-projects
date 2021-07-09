x = 0
y = 0

def setup():
    size(600, 600)
    background(51)
    colorMode(HSB, 360, 100, 100, 100)
    
def draw():
    for _ in range(100):
        drawPoint()
        nextPoint()
        
def drawPoint():
    px = map(x, -2.182, 2.6558, 0, width)
    py = map(y, 0, 9.9983, height, 0)
    
    c = map(py, 0, height, 0, 360)
    stroke(c, 100, 100, 50)
    strokeWeight(2)
    
    point(px, py)
    
def nextPoint():
    global x, y
    
    n = random(1)
    
    if n < 0.01:
        nextX = 0
        nextY = 0.16 * y
    elif n < 0.86:
        nextX = 0.85 * x + 0.04 * y
        nextY = -0.04 * x + 0.85 * y + 1.6
    elif n < 0.93:
        nextX = 0.2 * x - 0.26 * y
        nextY = 0.23 * x + 0.22 * y + 1.6
    else:
        nextX = -0.15 * x + 0.28 * y
        nextY = 0.26 * x + 0.24 * y + 0.44

    x = nextX
    y = nextY
