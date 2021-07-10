from branch import *

class Blob:
    
    def __init__(self, x, y, nb_branch, growth_rate=1, mutation_rate=0.05):
        self.x = x
        self.y = y
        self.branches = []
        self.growth_rate = growth_rate
        self.mutation_rate = mutation_rate
        
        angle = TWO_PI / nb_branch

        for i in range(nb_branch):
            self.branches.append(Branch(self.x, self.y, i * angle, self.growth_rate, self.mutation_rate, 4))
        
    def update(self):
        for branch in self.branches:
            branch.update()
        
    def show(self):
        for branch in self.branches:
            branch.show()
