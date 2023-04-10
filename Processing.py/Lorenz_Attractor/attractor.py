class Attractor:
    def __init__(self, x, y, z, rho, sigma, beta, dt):
        self.pos = PVector(x, y, z)
        self.vel = PVector(0, 0, 0)
        self.points = []
        
        self.rho = rho
        self.sigma = sigma
        self.beta = beta
        
        self.dt = dt
        
    def calculate_vel(self):
        self.vel.x = self.sigma * (self.pos.y - self.pos.x)
        self.vel.y = self.pos.x * (self.rho - self.pos.z) - self.pos.y
        self.vel.z = self.pos.x * self.pos.y - self.beta * self.pos.z
        
    def update(self):
        self.calculate_vel()
        self.pos.add(self.vel * self.dt)
        self.points.append(self.pos)
        
        print(self.pos)
        
    def display(self):
        stroke(255)
        noFill()
        #strokeWeight(1)

        beginShape()
        for pt in self.points:
            vertex(pt.x + width/2, pt.y + height/2, pt.z)
        endShape()
