import tkinter as tk
from grid_editor import grid_editor

class MyApp:
    def __init__(self, root):
        #建立主Canvas與兩個Scrollbar
        self.main_canvas = tk.Canvas(root)
        self.v_scrollbar = tk.Scrollbar(root, orient="vertical", command=self.main_canvas.yview)
        self.h_scrollbar = tk.Scrollbar(root, orient="horizontal", command=self.main_canvas.xview)

        self.main_canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.main_canvas.pack(side="left", fill="both", expand=True)

        #建立可捲動Frame
        self.scrollable_frame = tk.Frame(self.main_canvas)

        #把Frame放到Canvas裡
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        #當scrollable_frame尺寸變動更新捲動區域邊界
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        #Canvas與背景圖
        self.canvas = tk.Canvas(self.scrollable_frame, width=1358, height=686)
        self.background = tk.PhotoImage(file="image/image001.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background)
        self.canvas.pack()

        #控制方格
        self.editor = grid_editor(self.canvas, self)

        #底下工具列容器
        self.container = tk.Frame(self.scrollable_frame)
        self.container.pack(fill='x')

        #設定欄位寬度配置
        self.container.grid_columnconfigure(0, weight=4)
        self.container.grid_columnconfigure(1, weight=6)

        #左側：輸入 + Apply 按鈕
        self.left_container = tk.Frame(self.container)
        self.left_container.grid(row=0, column=0, sticky='w', padx=10)

        self.width_entry = tk.Entry(self.left_container, width=8)
        self.height_entry = tk.Entry(self.left_container, width=8)
        self.width_entry.insert(0, "width")
        self.height_entry.insert(0, "height")
        self.width_entry.pack(side='left', padx=2)
        self.height_entry.pack(side='left', padx=2)

        self.apply_btn = tk.Button(self.left_container, text='Apply', command=self.editor.applySize)
        self.apply_btn.pack(side='left', padx=5)

        #右側：功能按鈕們（置中排列）
        self.right_container = tk.Frame(self.container)
        self.right_container.grid(row=0, column=1, sticky='w')

        self.btns_row = tk.Frame(self.right_container)
        self.btns_row.pack(anchor='center')

        self.add_btn = tk.Button(self.btns_row, text='New', command=lambda: self.editor.addGrid([100, 100, 200, 200]))
        self.del_btn = tk.Button(self.btns_row, text='Delete', command=lambda: self.editor.delGrid(self.editor.selectedGrid))
        self.save_btn = tk.Button(self.btns_row, text='Save', command=self.editor.saveLayout)
        self.load_btn = tk.Button(self.btns_row, text='Load', command=self.editor.loadLayout)

        self.add_btn.pack(side='left', padx=5, pady=5)
        self.del_btn.pack(side='left', padx=5, pady=5)
        self.save_btn.pack(side='left', padx=5, pady=5)
        self.load_btn.pack(side='left', padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("assignment")
    root.geometry("1380x750+10+10") 
    app = MyApp(root)
    root.mainloop()