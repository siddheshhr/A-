from tkinter import *
from functools import partial
from time import sleep
import math

class App:
    def __init__(self, master):
        self.master = master
        master.wm_title("Ship Routing Simulator")
        self.buttons = []
        self.grid_size = 50  
        self.start = [25, 11]  # Start point
        self.goal = [7, 47] 
        
        # Define geographical features
        self.obstacles = []
        self.shallow_waters = []
        
        # Create simplified India's East Coast 
        for i in range(0, 45):
            curve_offset = int(i / 15) 
            self.obstacles.append([i, 3 + curve_offset])
            for j in range(0, 3 + curve_offset):
                self.obstacles.append([i, j])
        
        # Add sparse shallow waters along Indian coast
        for i in range(0, 45):
            for j in range(4, 8):
                if [i, j] not in self.obstacles: 
                    self.shallow_waters.append([i, j])
        
        # Create smaller Sri Lanka 
        sri_lanka_center = [25, 15]
        for i in range(-2, 3):
            for j in range(-2, 3):
                if math.sqrt(i**2 + j**2) <= 2:  # Smaller circular shape
                    self.obstacles.append([sri_lanka_center[0] + i, sri_lanka_center[1] + j])
        
        # Add minimal shallow waters around Sri Lanka (only top and left sides)
        for i in range(-3, 4):
            for j in range(-3, 4):
                    point = [sri_lanka_center[0] + i, sri_lanka_center[1] + j]
                    if (point not in self.obstacles and 
                        (i <= 1 or j <= 1)):
                        self.shallow_waters.append(point)

        # Create simplified Andaman Islands (top-right)
        for i in range(5, 10):  # Smaller island chain
            self.obstacles.extend([[i, 42], [i, 43]])
            if i % 2 == 0:  # Fewer small islands
                self.obstacles.append([i, 44])
        for i in range(4, 11):
            for j in range(41, 45):
                if [i, j] not in self.obstacles and i % 2 == 0:
                    self.shallow_waters.append([i, j])

        self.initialize_grid()
        self.enable_buttons()
        self.set_predefined_points()
        self.create_ocean_background()
        self.path_found = False
        self.resize_window()

    def resize_window(self):
        grid_width = self.grid_size * 30 
        grid_height = self.grid_size * 30 

        self.master.geometry(f"{grid_width}x{grid_height}")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - grid_width) // 2
        y = (screen_height - grid_height) // 2
        self.master.geometry(f"+{x}+{y}")

    def initialize_grid(self):
        for i in range(self.grid_size):
            self.buttons.append([])
            for j in range(self.grid_size):
                button = Button(self.master, width=2, height=1,
                                command=partial(self.button_operation, i, j), 
                                state="disabled",
                                relief=FLAT,
                                borderwidth=1,
                                highlightthickness=0)
                self.buttons[i].append(button)
                self.buttons[i][j].grid(row=i, column=j, padx=1, pady=1)

    def create_ocean_background(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if ([i, j] not in self.obstacles and 
                    [i, j] not in self.shallow_waters and 
                    [i, j] != self.start and 
                    [i, j] != self.goal):
                    self.buttons[i][j].configure(bg='dark blue')

    def enable_buttons(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].configure(state="normal")

    def disable_buttons(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].configure(state="disable")

    def set_predefined_points(self):
        self.buttons[self.start[0]][self.start[1]].configure(bg='lime green') 
        self.buttons[self.goal[0]][self.goal[1]].configure(bg='red') 
        for obstacle in self.obstacles:
            self.buttons[obstacle[0]][obstacle[1]].configure(bg='saddle brown')

        # Set shallow waters
        for shallow in self.shallow_waters:
            self.buttons[shallow[0]][shallow[1]].configure(bg='medium turquoise')

    def heuristic(self, node1, node2):
        return math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)  # Euclidean distance

    def get_movement_cost(self, current, neighbor):
        if neighbor in self.shallow_waters:
            base_cost = 1.5 
        else:
            base_cost = 1.0
        if abs(current[0] - neighbor[0]) + abs(current[1] - neighbor[1]) == 2:
            return base_cost * 1.4
        return base_cost

    def find_neighbors(self, current):
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        for direction in directions:
            neighbor = [current[0] + direction[0], current[1] + direction[1]]
            if (0 <= neighbor[0] < self.grid_size and 
                0 <= neighbor[1] < self.grid_size and 
                neighbor not in self.obstacles):
                neighbors.append(neighbor)
        return neighbors

    def a_star_algorithm(self, start, goal):
        open_set = {tuple(start)}
        closed_set = set()
        came_from = {}
        g_score = {tuple(start): 0}
        f_score = {tuple(start): self.heuristic(start, goal)}
        while open_set:
            self.master.update_idletasks()
            sleep(0.02) 
            current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
            current_list = list(current)
            if current_list == goal:
                path = []
                while current_list != start:
                    path.append(current_list)
                    self.buttons[current_list[0]][current_list[1]].configure(bg='yellow')
                    current_list = came_from[tuple(current_list)]
                return True
            open_set.remove(current)
            closed_set.add(current)
            
            for neighbor in self.find_neighbors(current_list):
                neighbor_tuple = tuple(neighbor)
                if neighbor_tuple in closed_set:
                    continue
                tentative_g_score = g_score[current] + self.get_movement_cost(current_list, neighbor)
                if neighbor_tuple not in open_set:
                    open_set.add(neighbor_tuple)
                    if neighbor not in self.shallow_waters:
                        self.buttons[neighbor[0]][neighbor[1]].configure(bg='light blue')  # Explored nodes
                elif tentative_g_score >= g_score.get(neighbor_tuple, float('inf')):
                    continue
                    
                came_from[neighbor_tuple] = current_list
                g_score[neighbor_tuple] = tentative_g_score
                f_score[neighbor_tuple] = g_score[neighbor_tuple] + self.heuristic(neighbor, goal)

        return False

    def button_operation(self, row, col):
        self.disable_buttons()
        if not self.path_found:
            self.path_found = self.a_star_algorithm(self.start, self.goal)
        else:
            self.enable_buttons()
            self.path_found = False

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
