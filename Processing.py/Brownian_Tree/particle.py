class Particle:
    
    def __init__(self, radius):
        self.pos = PVector.random2D() * min(width, height)
        self.pos.set(abs(self.pos.x), abs(self.pos.y))
        self.radius = radius
        self.lifespan = 500
        self.alive = True
        
    def update(self):
        self.pos.add(PVector.random2D() * random(10))
        x = constrain(self.pos.x, 0, width)
        y = constrain(self.pos.y, 0, height)
        self.pos = PVector(x, y)
        
        self.lifespan -= 1
        if self.lifespan <= 0:
            self.alive = False
    
    def show(self):
        fill(100, 200, 255, 150)
        stroke(255, 50)
        ellipse(self.pos.x, self.pos.y, self.radius * 2, self.radius * 2)
        
    def intersects(self, tree):
        for p in tree:
            if dist(p.pos.x, p.pos.y, self.pos.x, self.pos.y) < self.radius * 2:
                return True
        return False
