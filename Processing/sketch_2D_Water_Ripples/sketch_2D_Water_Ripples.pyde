cols = None
rows = None

current = []
previous = []

damping = 0.99

def setup():
    global cols, rows, current, previous
    
    size(600, 600)
    cols = width
    rows = height
    
    current = [[0 for _ in range(rows)] for _ in range(cols)]
    previous = [[0 for _ in range(rows)] for _ in range(cols)]
    
def mouseDragged():
    global previous
    previous[mouseX][mouseY] = 500
    
    
def draw():
    global current, previous
    background(0)
    
    loadPixels()
    for i in range(1, cols-1):
        for j in range(1, rows-1):
            current[i][j] = (previous[i-1][j] + previous[i+1][j] + previous[i][j-1] + previous[i][j+1]) / 2 - current[i][j]
            current[i][j] *= damping
            
            index = int(i + j * cols)
            pixels[index] = color(current[i][j])
    updatePixels()
    
    current, previous = previous, current
