import tkinter as tk
import json

def isOverlap(rect1, rect2):
    x11, y11, x12, y12 = rect1
    x21, y21, x22, y22 = rect2
    if x11 >= x22 or x21 >= x12:
        return False
    if y11 >= y22 or y21 >= y12:
        return False
    return True

class grid_editor:
    def __init__(self, canvas, app):
        self.canvas = canvas
        self.app = app  #Store the app instance for accessing width_entry, height_entry
        self.grid = [] #record grid's id
        self.handlers = {}
        self.startx = 0
        self.starty = 0
        self.selectedGrid = None
        self.selectedHandlers = None

        #bind
        self.canvas.bind('<ButtonPress-1>', self.pressGrid)
        self.canvas.bind('<B1-Motion>', self.moveGrid)
    
        pass

    def addGrid(self, coords):
        for grid in self.grid:
            if isOverlap(coords, self.canvas.coords(grid)):
                print('overlap!')
                return

        new_grid = self.canvas.create_rectangle(*coords, outline='red', width=4)
        self.grid.append(new_grid)
        self.addHandlers(new_grid)
        # self.canvas.tag_bind(new_grid, '<ButtonPress-1>', self.pressGrid)
        # self.canvas.tag_bind(new_grid, '<B1-Motion>', self.moveGrid)
        
    def pressGrid(self, event):
        found = False
        #忽略點到handler
        current = self.canvas.find_withtag("current") #closest id
        if current and "handler" in self.canvas.gettags(current[0]):
            return

        for grid in self.grid:
            x1, y1, x2, y2 = self.canvas.coords(grid)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.selectedGrid = grid
                self.canvas.itemconfig(grid, outline='orange')
                found = True

                #即時更新輸入框內容
                width = int(x2 - x1)
                height = int(y2 - y1)
                self.app.width_entry.delete(0, tk.END)
                self.app.width_entry.insert(0, width)
                self.app.height_entry.delete(0, tk.END)
                self.app.height_entry.insert(0, height)
            else:
                self.canvas.itemconfig(grid, outline='red')
        if not found:
            self.selectedGrid = None        
        self.startx, self.starty = event.x, event.y
       

    def moveGrid(self, event):
        if self.selectedGrid is None:
            return
        dx = event.x - self.startx 
        dy = event.y - self.starty  
        old_coords = self.canvas.coords(self.selectedGrid)
        new_coords = [old_coords[0]+dx, old_coords[1]+dy, old_coords[2]+dx, old_coords[3]+dy]
        if new_coords[0] < 0 or new_coords[1] < 0 or new_coords[2] > 1358 or new_coords[3] > 686:
            print("exceed!")
            return
        for grid in self.grid:
            if grid != self.selectedGrid and isOverlap(new_coords, self.canvas.coords(grid)):
                print('overlap!')
                return
        self.canvas.move(self.selectedGrid, dx, dy)
        for hs in self.handlers[self.selectedGrid]:
            self.canvas.move(hs, dx, dy)

        self.startx, self.starty = event.x, event.y


    def addHandlers(self, grid):
        x1, y1, x2, y2 = self.canvas.coords(grid)
        hs = [
            self.canvas.create_rectangle(x1-4, y1-4, x1+4, y1+4, fill='blue'),
            self.canvas.create_rectangle(x2-4, y1-4, x2+4, y1+4, fill='blue'),
            self.canvas.create_rectangle(x2-4, y2-4, x2+4, y2+4, fill='blue'),
            self.canvas.create_rectangle(x1-4, y2-4, x1+4, y2+4, fill='blue')
        ]
        self.handlers[grid] = hs
        for h in hs:
            self.canvas.tag_bind(h, '<ButtonPress-1>', self.pressHandlers)
            self.canvas.tag_bind(h, '<B1-Motion>', self.dragHandlers)
            self.canvas.itemconfig(h, tags=("handler",))

    def pressHandlers(self, event):
        self.startx, self.starty = event.x, event.y
        self.selectedHandlers = self.canvas.find_closest(event.x, event.y)[0]
        for grid in self.grid:
            if self.selectedHandlers in self.handlers[grid]:
                self.selectedGrid = grid
                self.canvas.itemconfig(grid, outline="orange")
            else:
                self.canvas.itemconfig(grid, outline="red")   
   
    def dragHandlers(self, event):
        dx = event.x - self.startx 
        dy = event.y - self.starty 
        coords = self.canvas.coords(self.selectedGrid)
        item = self.canvas.find_closest(event.x, event.y)[0]

        index = self.handlers[self.selectedGrid].index(self.selectedHandlers)
        if index == 0:
            coords[0] += dx
            coords[1] += dy
        elif index == 1:
            coords[2] += dx
            coords[1] += dy
        elif index == 2:
            coords[2] += dx
            coords[3] += dy
        elif index == 3:
            coords[0] += dx
            coords[3] += dy
        for grid in self.grid:
            if grid != self.selectedGrid and isOverlap(coords, self.canvas.coords(grid)):
                print("overlap!")
                return
        if coords[0] < 0 or coords[1] < 0 or coords[2] > 1358 or coords[3] > 686:
            print("exceed!")
            return
        if abs(coords[2] - coords[0]) < 20 or abs(coords[3] - coords[1]) < 20:
            print("too small!")
            return
        
        self.canvas.coords(self.selectedGrid, *coords)
        #更新控制點位置
        self.canvas.coords(self.handlers[self.selectedGrid][0], coords[0]-4, coords[1]-4, coords[0]+4, coords[1]+4) #左上
        self.canvas.coords(self.handlers[self.selectedGrid][1], coords[2]-4, coords[1]-4, coords[2]+4, coords[1]+4) #右上
        self.canvas.coords(self.handlers[self.selectedGrid][2], coords[2]-4, coords[3]-4, coords[2]+4, coords[3]+4) #右下
        self.canvas.coords(self.handlers[self.selectedGrid][3], coords[0]-4, coords[3]-4, coords[0]+4, coords[3]+4) #左下
        
        #即時更新輸入框內容
        width = int(coords[2] - coords[0])
        height = int(coords[3] - coords[1])
        self.app.width_entry.delete(0, tk.END)
        self.app.width_entry.insert(0, width)
        self.app.height_entry.delete(0, tk.END)
        self.app.height_entry.insert(0, height)

        self.startx, self.starty = event.x, event.y

    def applySize(self):
        try:
            width = int(self.app.width_entry.get())
            height = int(self.app.height_entry.get())
        except ValueError:
            print("請輸入正確數字")
            return

        grid = self.selectedGrid
        if grid is None:
            print("未選取方格")
            return

        x1, y1, _, _ = self.canvas.coords(grid)
        x2 = x1 + width
        y2 = y1 + height
        new_coords = [x1, y1, x2, y2]

        #檢查邊界與重疊
        if x2 > 1358 or y2 > 686 or width < 20 or height < 20:
            print("exceed")
            return
        for other in self.grid:
            if other != grid and isOverlap(new_coords, self.canvas.coords(other)):
                print("overlap!")
                return

        self.canvas.coords(grid, *new_coords)
        self.canvas.coords(self.handlers[self.selectedGrid][0], x1-4, y1-4, x1+4, y1+4) #左上
        self.canvas.coords(self.handlers[self.selectedGrid][1], x2-4, y1-4, x2+4, y1+4) #右上
        self.canvas.coords(self.handlers[self.selectedGrid][2], x2-4, y2-4, x2+4, y2+4) #右下
        self.canvas.coords(self.handlers[self.selectedGrid][3], x1-4, y2-4, x1+4, y2+4) #左下

    
    def delGrid(self, grid):
        if grid:
            self.canvas.delete(grid)
            for h in self.handlers.get(grid, []):
                self.canvas.delete(h)
            self.grid.remove(grid)
            del self.handlers[grid]

    def saveLayout(self, filename="layout.json"):
        coords_list = [self.canvas.coords(g) for g in self.grid]
        with open(filename, "w") as f:
            json.dump(coords_list, f)
        print("saved!")

    def loadLayout(self, filename="layout.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Layout file not found!")
            return

        #清除現有
        for grid in self.grid[:]:
            self.delGrid(grid)

        for coords in data:
            self.addGrid(coords)
        print("Layout loaded!")  