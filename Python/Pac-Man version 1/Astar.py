import heapq
from main import *
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
        if self.start[0] >= self.grid_width: self.start = self.grid_width - 1, self.start[1]
        elif self.start[0] < 0: self.start = 0, self.start[1]
        if self.start[1] >= self.grid_height: self.start = self.start[0], self.grid_height - 1
        elif self.start[1] < 0: self.start = self.start[0], 0

        self.end = end
        if self.end[0] >= self.grid_width: self.end = self.grid_width - 1, self.end[1]
        elif self.end[0] < 0: self.end = 0, self.end[1]
        if self.end[1] >= self.grid_height: self.end = self.end[0], self.grid_height - 1
        elif self.end[1] < 0: self.end = self.end[0], 0

        
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
        return self.cells[int(x) * self.grid_height + int(y)]
    
    
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
        try:
            while cell.parent is not self.start:
                cell = cell.parent
        except:
            return
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