from blob import *

class Branch:
    
    def __init__(self, x, y, angle, growth_rate=1, mutation_rate=0.05, stroke_weight=4):
        self.core = [PVector(x, y), PVector(x, y) + PVector.fromAngle(angle)]
        self.head = None
        self.growth_rate = growth_rate
        self.mutation_rate = mutation_rate
        self.sub_branches = []
        self.stroke_weight = stroke_weight
        
    def update(self):
        if random(1) <= self.growth_rate:
            a = self.core[-2]
            b = self.core[-1]
            angle = PVector(b.x - a.x, b.y - a.y).heading()
            angle += random(-PI/20, PI/20)
            new_part = self.core[-1] + PVector.fromAngle(angle)
            self.core.append(new_part)
            
            if random(1) <= self.mutation_rate:
                self.sub_branches.append(Branch(self.core[-1].x, self.core[-1].y, angle + random(-HALF_PI, HALF_PI), self.growth_rate * 0.5, self.mutation_rate, self.stroke_weight * 0.75))
                
        for branch in self.sub_branches:
            branch.update()
            
        
    def show(self):
        noFill()
        stroke(255, 150)
        strokeWeight(self.stroke_weight)
        beginShape()
        for part in self.core:
            vertex(part.x, part.y)
        endShape()
        
        for branch in self.sub_branches:
            branch.show()
