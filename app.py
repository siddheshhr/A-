from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from typing import List, Optional

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adjusted grid size for 32x32 grid
GRID_SIZE = 32

# Initialize a 32x32 grid with random values between 0.3 and 1.0 (open water)
grid = np.random.uniform(0.3, 1.0, (GRID_SIZE, GRID_SIZE))

# Set some cells as obstacles (representing land or other barriers)
# Top-left land mass
grid[0:5, 0:5] = 0
# Mid-right land mass
grid[10:15, 20:25] = 0
# Bottom-left land mass
grid[25:32, 2:7] = 0

class RouteRequest(BaseModel):
    start: int
    end: int

def get_coordinates(cell_number: int) -> tuple:
    """Convert cell number to grid coordinates"""
    row = cell_number // GRID_SIZE
    col = cell_number % GRID_SIZE
    return (row, col)

def get_cell_number(row: int, col: int) -> int:
    """Convert grid coordinates to cell number"""
    return row * GRID_SIZE + col

def heuristic(start: tuple, goal: tuple) -> float:
    """Manhattan distance heuristic"""
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def get_neighbors(current: tuple) -> List[tuple]:
    """Get valid neighboring cells"""
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    
    for dx, dy in directions:
        new_x, new_y = current[0] + dx, current[1] + dy
        if (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and 
            grid[new_x][new_y] > 0):  # Check if not an obstacle
            neighbors.append((new_x, new_y))
    
    return neighbors

def a_star(start: tuple, goal: tuple) -> Optional[List[int]]:
    """A* pathfinding algorithm"""
    if grid[start[0]][start[1]] == 0 or grid[goal[0]][goal[1]] == 0:
        return None
        
    open_set = {start}
    came_from = {}
    
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
        
        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(get_cell_number(current[0], current[1]))
                current = came_from[current]
            path.append(get_cell_number(start[0], start[1]))
            return path[::-1]
            
        open_set.remove(current)
        
        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + (1 / grid[neighbor[0]][neighbor[1]])
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                open_set.add(neighbor)
                
    return None

@app.post("/find_route")
async def find_route(request: RouteRequest):
    start_coords = get_coordinates(request.start)
    end_coords = get_coordinates(request.end)
    
    path = a_star(start_coords, end_coords)
    if path is None:
        raise HTTPException(status_code=400, detail="No valid path found")
        
    return {
        "path": path,
        "grid_values": grid.tolist()  # Send grid values to visualize terrain
    }

@app.get("/grid_info")
async def get_grid_info():
    return {
        "size": GRID_SIZE,
        "grid_values": grid.tolist()
    }

# Add a test route to verify the API is working
@app.get("/")
async def root():
    return {"message": "Ship Routing API is running"}
