from collections import deque
from fourier import *

USER = 0
FOURIER = 1

x = []
fourierX = None
time = 0
drawing = []
path = deque([])
state = -1

# --------------------------------------------------------------------------------

def mousePressed():
    global time, drawing, x, state
    state = USER
    drawing = []
    x = []
    time = 0
    path.clear()

# --------------------------------------------------------------------------------

def mouseReleased():
    global fourierX, state
    state = FOURIER
    skip = 1
    for i in range(0, len(drawing), skip):
        x.append(Complex(drawing[i].x, drawing[i].y))
        
    fourierX = dft(x)
    fourierX.sort(key=lambda x: x['amp'], reverse=True)
    

# --------------------------------------------------------------------------------

def setup():
    fullScreen()
    
    background(51)
    strokeWeight(4)
    textSize(32)
    textAlign(CENTER)
    text("Draw anything you want !", width / 2, 40)
    strokeWeight(1)
    
# --------------------------------------------------------------------------------
    
def epicycles(x, y, rotation, fourier):
    
    for i in range(len(fourier)):
        prevx = x
        prevy = y
        
        freq = fourier[i] ['freq']
        radius = fourier[i] ['amp']
        phase = fourier[i] ['phase']
        x += radius * cos(freq * time + phase + rotation)
        y += radius * sin(freq * time + phase + rotation)
        
        stroke(255, 50)
        noFill()
        ellipse(prevx, prevy, radius * 2, radius * 2)
        stroke(255, 150)
        line(prevx, prevy, x, y)
        
    return PVector(x, y)
    
# --------------------------------------------------------------------------------

def draw():
    global time, path
    
    if state != -1:
        background(51)
        
    if state == USER:
        
        point = PVector(mouseX - width / 2, mouseY - height / 2)
        drawing.append(point)
        stroke(255)
        noFill()
        beginShape()
        for v in drawing:
            vertex(v.x + width / 2, v.y + height / 2)
        endShape()
        
    elif state == FOURIER:

        v = epicycles(width / 2, height / 2, 0, fourierX)
        path.appendleft(v)
        
        stroke(255)
        noFill()
        beginShape()
        for i in range(len(path)):
            vertex(path[i].x, path[i].y)
        endShape()
        
        dt = TWO_PI / len(fourierX)
        time += dt
        
        if time > TWO_PI:
            time = 0
            
        if len(path) >= len(fourierX):
            path.pop()
