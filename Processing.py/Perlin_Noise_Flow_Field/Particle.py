class Particle:

    def __init__(self, x, y, maxspeed, scl, ps):
        self.pos = PVector(x, y)
        self.vel = PVector.random2D()
        self.acc = PVector(0, 0)
        self.maxspeed = maxspeed
        self.prevPos = PVector(x, y)
        self.scl = scl
        self.ps = ps

    def update(self):
        self.vel.add(self.acc)
        self.vel.limit(self.maxspeed)
        self.pos.add(self.vel)
        self.edges()
        self.acc.mult(0)

    def display(self):
        stroke(255, 5)
        strokeWeight(1)

        line(self.pos.x, self.pos.y, self.prevPos.x, self.prevPos.y)
        self.updatePrev()

    def updatePrev(self):
        self.prevPos = PVector(self.pos.x, self.pos.y)

    def apply_force(self, force):
        self.acc.add(force)

    def edges(self):
        if self.pos.x > width - 1:
            self.pos.x = 0
            self.updatePrev()
        if self.pos.x < 0:
            self.pos.x = width - 1
            self.updatePrev()
        if self.pos.y > height - 1:
            self.pos.y = 0
            self.updatePrev()
        if self.pos.y < 0:
            self.pos.y = height - 1
            self.updatePrev()

    def follow(self, vectors):
        x = floor(self.pos.x / self.scl)
        y = floor(self.pos.y / self.scl)

        force = vectors[x][y]
        self.apply_force(force)

        '''
        for particle in self.ps.particles:
            d = dist(self.pos.x, self.pos.y, particle.pos.x, particle.pos.y)
            if d < 1 and d != 0:
                self.apply_force(PVector(self.pos.x - particle.pos.x, self.pos.y - particle.pos.y))
        '''
