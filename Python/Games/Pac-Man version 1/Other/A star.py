import heapq
from copy import deepcopy

class Cell:
    
    def __init__(self, x, y, reachable):
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        
    def __lt__(self, other):
        return self.f < other.f
        
class AStar:
    
    def __init__(self, walls, start, end):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = 22
        self.grid_width = 19
        self.w = deepcopy(walls)
        self.start = start
        self.end = end
        
        self.init_grid()
        
        
    def init_grid(self):
        walls = deepcopy(self.w)
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                reachable = False if [x, y] in walls else True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(self.start[0], self.start[1])
        self.end = self.get_cell(self.end[0], self.end[1])
       
       
    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))
    
    
    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]
    
    
    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x + 1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y - 1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x - 1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y + 1))
            
        return cells
        
        
    def display_path(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            print(f'path: cell {cell.x}, {cell.y}')
            
    def get_first_step(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
        return cell.x, cell.y
            
            
    def update_cell(self, adj, cell):
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g
        
        
    def process(self):
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            f, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            if cell is self.end:
                return self.get_first_step()
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))
    
walls = [[0, 0], [0, 420], [20, 0], [20, 420], [40, 0], [40, 420], [60, 0], [60, 420], [80, 0], [80, 420], [100, 0], [100, 420], [120, 0], [120, 420], [140, 0], [140, 420], [160, 0], [160, 420], [0, 0], [0, 20], [0, 40], [0, 60], [0, 80], [0, 100], [0, 120], [0, 140], [0, 180], [0, 220], [0, 260], [0, 280], [0, 300], [0, 320], [0, 340], [0, 360], [0, 380], [0, 400], [0, 420], [0, 140], [20, 140], [40, 140], [60, 140], [0, 180], [20, 180], [40, 180], [60, 180], [0, 220], [20, 220], [40, 220], [60, 220], [0, 260], [20, 260], [40, 260], [60, 260], [40, 380], [60, 380], [80, 380], [100, 380], [120, 380], [140, 380], [100, 300], [120, 300], [140, 300], [100, 220], [100, 240], [100, 260], [100, 100], [100, 120], [100, 140], [100, 160], [100, 180], [140, 100], [160, 100], [140, 180], [160, 180], [140, 220], [160, 220], [140, 260], [160, 260], [140, 340], [160, 340], [60, 300], [60, 320], [60, 340], [40, 40], [60, 40], [40, 60], [60, 60], [40, 100], [60, 100], [100, 40], [120, 40], [140, 40], [100, 60], [120, 60], [140, 60], [180, 0], [180, 20], [180, 40], [180, 60], [180, 340], [180, 360], [180, 380], [180, 260], [180, 280], [180, 300], [180, 100], [180, 120], [180, 140], [60, 160], [60, 240], [20, 340], [100, 360], [100, 340], [180, 420], [40, 300], [180, 220], [140, 200], [120, 140], [140, 140], [360, 0], [360, 420], [340, 0], [340, 420], [320, 0], [320, 420], [300, 0], [300, 420], [280, 0], [280, 420], [260, 0], [260, 420], [240, 0], [240, 420], [220, 0], [220, 420], [200, 0], [200, 420], [360, 0], [360, 20], [360, 40], [360, 60], [360, 80], [360, 100], [360, 120], [360, 140], [360, 180], [360, 220], [360, 260], [360, 280], [360, 300], [360, 320], [360, 340], [360, 360], [360, 380], [360, 400], [360, 420], [360, 140], [340, 140], [320, 140], [300, 140], [360, 180], [340, 180], [320, 180], [300, 180], [360, 220], [340, 220], [320, 220], [300, 220], [360, 260], [340, 260], [320, 260], [300, 260], [320, 380], [300, 380], [280, 380], [260, 380], [240, 380], [220, 380], [260, 300], [240, 300], [220, 300], [260, 220], [260, 240], [260, 260], [260, 100], [260, 120], [260, 140], [260, 160], [260, 180], [220, 100], [200, 100], [220, 180], [200, 180], [220, 220], [200, 220], [220, 260], [200, 260], [220, 340], [200, 340], [300, 300], [300, 320], [300, 340], [320, 40], [300, 40], [320, 60], [300, 60], [320, 100], [300, 100], [260, 40], [240, 40], [220, 40], [260, 60], [240, 60], [220, 60], [180, 0], [180, 20], [180, 40], [180, 60], [180, 340], [180, 360], [180, 380], [180, 260], [180, 280], [180, 300], [180, 100], [180, 120], [180, 140], [300, 160], [300, 240], [340, 340], [260, 360], [260, 340], [180, 420], [320, 300], [180, 220], [220, 200], [240, 140], [220, 140]]
for wall in walls:
    wall[0] //= 20
    wall[1] //= 20
    
a = AStar(walls, [4, 20], [9, 10])
print(a.process())