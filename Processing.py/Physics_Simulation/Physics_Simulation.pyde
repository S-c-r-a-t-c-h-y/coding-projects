from ball import *
from square import *

gravity = 0
friction = 1
debug = False

def setup():
    size(600, 600)
    #fullScreen(1)
    background(255)    
    
    for _ in range(100):
        radius = ceil(random(10, 30))
        mass = floor(random(1, 50))
        initial_velocity = PVector.random2D().mult(random(1, 10))
        movable = random(1, 4) < 3
        movable = True
        
        x = random(radius, width-radius)
        y = random(radius, height-radius)
        
        Ball(x, y, radius, mass=mass, initial_velocity=initial_velocity, movable=movable, debug=debug)
    
    Rectangle(width/2, height/2, 50, 50, movable=False)
    
    
    """
    Ball(width/4, height/2, 15, mass=50, initial_velocity=PVector(2, 0), debug=True)
    Ball(width/2, height/2, 15, mass=5, initial_velocity=PVector(-0.1, 0), debug=True)
    """
    
def draw():
    background(255)
    
    for ball in Ball.balls:
        ball.apply_force(PVector(0, gravity))
        ball.vel.mult(friction)
        ball.update()
        ball.display()
        
    for rectangle in Rectangle.rectangles:
        rectangle.update()
        rectangle.display()
