from ParticleSystem import *

scl = 20
x_offset, y_offset, z_offset = 0, 0, 0
offset_inc = 0.05

def setup():
    global grid, p
    size(400, 400, P3D)
    background(51)
    grid = [[None for _ in range(height // scl)] for _ in range(width // scl)]
    fill_grid(0.05, x_offset, y_offset, z_offset)
    p = Particle_System(500, scl, 5)

    
def draw():
    global grid, p
       
    do_grid_operations()
    
    
    p.follow(grid)
    p.update()
    p.display()
    

def do_grid_operations():
    '''
    Does every operations on the grid
    '''
    
    global x_offset, y_offset, z_offset
    fill_grid(0.05, x_offset, y_offset, z_offset)
    #draw_grid()
    
    #x_offset += offset_inc
    #y_offset += offset_inc
    z_offset += offset_inc
    
    
def fill_grid(noiseScale, off_x, off_y, z):
    '''
    Assign a noise value to each vector of the
    cells of the grid
    '''
    
    global grid
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            grid[x][y] = PVector.fromAngle(map(noise((x + off_x) * noiseScale, (y + off_y) * noiseScale, z * noiseScale), 0, 1, -TWO_PI, TWO_PI))
            grid[x][y].z = map(noise((x + off_x) * noiseScale, (y + off_y) * noiseScale, z * noiseScale), 0, 1, -1, 1)
            
def draw_grid():
    '''
    draws the vectors of the grid
    '''
    
    global grid
    background(51)
    stroke(255, 50)
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            line(x * scl, y * scl, 0, x * scl + grid[x][y].x * scl, y * scl + grid[x][y].y * scl, grid[x][y].z * scl)
