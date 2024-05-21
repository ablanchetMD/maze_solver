from tkinter import Tk,ttk,BOTH, Canvas
import time
import random

print("Running main.py")


import tkinter as tk

directions = [(-1,0),(1,0),(0,-1),(0,1)]

directions_lib = {
    "b":(0,-1),
    "t":(0,1),
    "l":(-1,0),
    "r":(1,0)
}

class Point():
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

class Line():
    def __init__(self,point1,point2,app):
        self.x1 = point1.x
        self.y1 = point1.y
        self.x2 = point2.x
        self.y2 = point2.y
        self.app = app
        self.canvas = app.canvas
    
    def draw(self,fill_color):
        self.canvas.create_line(
            self.x1,self.y1,self.x2,self.y2,fill=fill_color,width=2
        )

    def draw_animate(self,fill_color,steps):
        # self.draw(fill_color)
        step_x = (self.x2 - self.x1) / steps
        step_y = (self.y2 - self.y1) / steps
        current_x, current_y = self.x1, self.y1

        for i in range(1, steps + 1):
            # Schedule each step of the drawing
            self.app.after(i * 100, self.draw_step, self.x1, self.y1, current_x, current_y,fill_color)
            current_x += step_x
            current_y += step_y
        self.app.after(i * 100, self.draw_step, self.x1, self.y1, current_x, current_y,fill_color)

    def draw_step(self, x1, y1, x2, y2,fill_color):
        # Draw a step in the rectangle animation
        self.canvas.create_line(x1, y1, x2, y2, fill=fill_color,width=2)

class Cell():
    def __init__(self,walls,x,y,size,app,matrix):
        self.walls = walls.copy()
        self.matrix=matrix
        self.x = x
        self.y = y
        self._x1 = x - (size / 2)
        self._x2 = x + (size / 2)
        self._y1 = y - (size / 2)
        self._y2 = y + (size / 2)
        self._canvas = app.canvas
        self.exit = False
        self.enter = False
        self.app = app
        self.visited = False

    def set_status(self,typ,bool):
        if typ == "exit":
            self.exit = bool
        if type == "enter":
            self.enter = bool
    
    def _break_walls_r(self,delay=0):
        self.visited = True
        current_pos = self.matrix
        current_pos = (current_pos[0] -1, current_pos[1] -1)
        max_y = self.app.maze.num_rows -1
        max_x = self.app.maze.num_cols -1
        cells = self.app.maze.cells               
        list = []
        for dir in directions:
            new_dir = (current_pos[0] + dir[0], current_pos[1] + dir[1])           
            
            if new_dir[0] < 0 or new_dir[0] > max_x or new_dir[1] < 0 or new_dir[1] > max_y:
                # We're going off map.
                continue
            if cells[new_dir[0]][new_dir[1]].visited == True:
                continue
            list.append((new_dir[0],new_dir[1]))
        
        while len(list) > 0:
            next_cell = random.choice(list)
            if cells[next_cell[0]][next_cell[1]].visited == True:
                list.remove(next_cell)
                continue
            heading_to = (current_pos[0] - next_cell[0], current_pos[1] - next_cell[1])
            # print(f"new_dir = {heading_to}")          
            if (-1,0) == heading_to:
                self.walls.remove("r")
                cells[next_cell[0]][next_cell[1]].walls.remove("l")
            elif (1,0) == heading_to:
                self.walls.remove("l")
                cells[next_cell[0]][next_cell[1]].walls.remove("r")
            elif (0,1) == heading_to:
                self.walls.remove("t")
                cells[next_cell[0]][next_cell[1]].walls.remove("b")
            elif (0,-1) == heading_to:
                self.walls.remove("b")
                cells[next_cell[0]][next_cell[1]].walls.remove("t")
            delay += 10
            self.app.after(delay,self.draw)
            list.remove(next_cell)
            cells[next_cell[0]][next_cell[1]]._break_walls_r(delay)


    def draw(self):
        # print(f"drawing : {self} with {self.walls}")
        color = "black"

        if "r" in self.walls:
            Line(Point(self._x2,self._y1),Point(self._x2,self._y2),self.app).draw_animate(color,5)
        else:    
            Line(Point(self._x2,self._y1),Point(self._x2,self._y2),self.app).draw_animate("white",5)
        if "l" in self.walls:
            Line(Point(self._x1,self._y1),Point(self._x1,self._y2),self.app).draw_animate(color,5)
        else:    
            Line(Point(self._x1,self._y1),Point(self._x1,self._y2),self.app).draw_animate("white",5)
        if "t" in self.walls:
            Line(Point(self._x1,self._y1),Point(self._x2,self._y1),self.app).draw_animate(color,5)
        else:   
            Line(Point(self._x1,self._y1),Point(self._x2,self._y1),self.app).draw_animate("white",5)
        if "b" in self.walls:        
            Line(Point(self._x1,self._y2),Point(self._x2,self._y2),self.app).draw_animate(color,5)
        else:    
            Line(Point(self._x1,self._y2),Point(self._x2,self._y2),self.app).draw_animate("white",5)

    def draw_move(self,to_cell,undo=False,delay=0):
        fillcolor = "red"
        if undo == True:
            fillcolor = "gray"
        self.app.after(delay,Line(Point(self.x,self.y),Point(to_cell.x,to_cell.y),self.app).draw_animate,fillcolor,5)
    
    def __repr__(self):
        return f"C({self.matrix})"


class Maze():
    def __init__(self,x1,y1,num_rows,num_cols,cell_size,app,seed=None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.x = x1
        self.y = y1
        self.cell_size = cell_size
        self.canvas = app.canvas
        self.app = app
        if seed != None:
            self.seed = random.seed(seed)
        else:
            self.seed = random.seed()
    
    def _create_cells(self):
        self.cells = []
        max_width = self.num_cols * self.cell_size
        max_height = self.num_rows * self.cell_size

        # if self.canvas.width < max_width or self.canvas.height < max_height:
        #     raise Exception(f"[MAZE] exceeds canvas. W: {self.canvas.width} < {max_width} or H: {self.canvas.height} < {max_height}")
        
        increment_x = self.cell_size
        increment_y = self.cell_size
        walls = ["r","l","t","b"]
        constant_x = (self.x * 2) / self.num_cols
        constant_y = (self.y * 2) / self.num_rows        
        
        for i in range(1,self.num_rows+1):
            x = increment_x * i          
            row = []            
            for j in range(1,self.num_cols+1):
                y = increment_y * j
                current = Cell(walls,x,y,self.cell_size,self.app,(i,j))
                row.append(current)
                self.app.after((i+j)*50,current.draw)
            # row.append(current)
            self.cells.append(row)
        # self.cells.append(row)
    
    def _break_entrance_and_exit(self):
        # print(f"MAZE h : {self.num_cols} w: {self.num_rows}, \n{self}")
        enter_cell = self.cells[0][self.num_cols-1]
        # print(f"enter cell = {enter_cell}")
        exit_cell = self.cells[self.num_rows-1][0]
        # print(f"exit cell = {exit_cell}")
        exit_cell.set_status("exit",True)
        exit_cell.walls.remove("t")
        enter_cell.set_status("enter",True)
        enter_cell.walls.remove("b")
        exit_cell.draw()
        enter_cell.draw()
        enter_cell._break_walls_r()
    
    def solve(self):
        enter_cell = self.cells[0][self.num_cols-1]
        return self.solve_r(enter_cell)
    
    def solve_r(self,current_cell,delay=0):
        current_cell.visited = True
        current_pos = current_cell.matrix
        current_pos = (current_pos[0] -1, current_pos[1] -1)
        max_y = self.app.maze.num_rows -1
        max_x = self.app.maze.num_cols -1
        cells = self.app.maze.cells               
        list = []
        new_delay = delay + 100
        for dir in directions:
            new_dir = (current_pos[0] + dir[0], current_pos[1] + dir[1])
            if dir[0] == -1 and "l" in current_cell.walls:
                continue
            elif dir[0] == 1 and "r" in current_cell.walls:
                continue
            elif dir[1] == -1 and "t" in current_cell.walls:
                continue
            elif dir[1] == 1 and "b" in current_cell.walls:
                continue
            if new_dir[0] < 0 or new_dir[0] > max_x or new_dir[1] < 0 or new_dir[1] > max_y:
                # We're going off map.
                continue
            if cells[new_dir[0]][new_dir[1]].visited == True:
                # Already went there.
                continue            
            if cells[new_dir[0]][new_dir[1]].exit == True:
                self.app.after(new_delay,current_cell.draw_move,cells[new_dir[0]][new_dir[1]],False,new_delay)
                return True
            list.append((new_dir[0],new_dir[1]))
        
        
        while len(list) > 0:
            next_cell = random.choice(list)
            if cells[next_cell[0]][next_cell[1]].visited == True:
                list.remove(next_cell)
                continue
            heading_to = (current_pos[0] - next_cell[0], current_pos[1] - next_cell[1])           
            
            to_cell = cells[next_cell[0]][next_cell[1]]
            self.app.after(new_delay,current_cell.draw_move,to_cell,False,new_delay)
            list.remove(next_cell)
            response,new_delay = self.solve_r(to_cell,new_delay)
            if response == True:
                return True
            new_delay += 100
            self.app.after(delay,current_cell.draw_move,to_cell,True,new_delay)        
        
        return False,new_delay
            
            

        
    
    def _reset_visited(self):
        cells = self.cells
        for i in range(0,len(cells)):                      
            for j in range(0,len(cells[i])):
                cells[i][j].visited = False


    
    def __repr__(self):
        
        return f"{self.cells}"



class MyApp(tk.Tk):
    def __init__(self,h,w):
        super().__init__()
        self.title("Maze Solver")
        self.geometry(f"{h}x{w}")
        self.create_widgets()
        # Create a canvas widget
        self.canvas = tk.Canvas(self, width=h//5*4, height=w//5*4, bg='white')
        self.canvas.height = h //5 * 4
        self.canvas.width = w //5 * 4
        self.canvas.pack(pady=50)  # Center the canvas vertically
        self.running = False

        # self.protocol("WM_DELETE_WINDOW",self.close)
    
    def draw_lines(self, lines,fill_color):
        for line in lines:
            line.draw(self.canvas,fill_color)
    
    def draw_cells(self,cells):
        for cell in cells:
            cell.draw()

    def create_widgets(self):
        # Create a label widget
        label = tk.Label(self, text="Hello, Tkinter!")
        label.pack(pady=20)

        # Create a button widget
        button = tk.Button(self, text="Draw Maze!", command=self.on_button_click)
        button.pack(pady=20)

        solve_btn = tk.Button(self, text="Solve", command=self.solve_maze)
        solve_btn.pack(pady=20)

    def on_button_click(self):
        self.maze = Maze(self.canvas.height,self.canvas.width,10,10,100,self)
        self.clear_canvas()  
        self.maze._create_cells()
        app.after(1000,self.maze._break_entrance_and_exit)
    
    def solve_maze(self):
        self.maze._reset_visited()
        self.maze.solve()

    def clear_canvas(self):
        self.canvas.delete("all")    
    
    


    
if __name__ == "__main__":
    app = MyApp(1500,1500)
    app.mainloop()


# root = Tk()
# root.title = "Maze Solver"
# frm = ttk.Frame(root,padding=10)
# frm.grid()
# ttk.Label(frm, text="Trying this out !").grid(column=0,row=0)
# ttk.Button(frm, text="Quit",command=root.destroy).grid(column=0,row=1)
# root.mainloop()