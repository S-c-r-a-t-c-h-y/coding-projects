from Particle import *

class Particle_System:
    
    def __init__(self, nb_particles, scl, maxspeed):
        
        self.particles = []
        for _ in range(nb_particles):
            self.particles.append(Particle(random(width-1), random(height-1), maxspeed, scl, self))
            
    def display(self):
        for p in self.particles:
            p.display()

            
    def update(self):
        for p in self.particles:
            p.update()
            
    def follow(self, vectors):
        for p in self.particles:
            p.follow(vectors)
