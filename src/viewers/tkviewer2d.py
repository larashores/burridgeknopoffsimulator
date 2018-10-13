from tkinter import ttk
import tkinter as tk
import numpy as np

from src.simulation.blockarray import BlockArray
from viewers.integercheck import int_validate


class TkViewer2dGui(ttk.Frame):
    LABEL_TEXT = 'Time: {:.1f}'
    def __init__(self, parent, rows, cols, solution, time_interval=.1, spring_length=1,  **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.time = 0
        self.rows = rows
        self.cols = cols
        self.solution = solution
        self.spring_length = spring_length
        self.time_interval = time_interval

        self.sidebar = Sidebar(self)
        self.separator = ttk.Separator(self, orient=tk.VERTICAL)
        self.time_label = ttk.Label(self, text=self.LABEL_TEXT.format(self.time))
        self.canvas = tk.Canvas(self)

        self.sidebar.pack(fill=tk.Y, side=tk.RIGHT)
        self.separator.pack(fill=tk.Y, padx=5, pady=10, side=tk.RIGHT)
        self.time_label.pack()
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.update_values()

    def draw_blocks(self, positions):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        distance = (self.spring_length * self.scale)
        start_x = (width - (self.cols-1)*distance - self.block_size) / 2
        start_y = (height - (self.rows-1)*distance - self.block_size) / 2
        block_array = BlockArray(positions, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                x_pos = block_array.positions[i, j]
                x, y = start_x + x_pos * self.scale, start_y + distance * i
                self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size)

    def draw_recursive(self, i):
        self.update_values()
        self.time_label.config(text=self.LABEL_TEXT.format(self.time))
        self.canvas.delete(tk.ALL)
        self.draw_blocks(np.array(self.solution[i]))
        if i < len(self.solution) - 1:
            self.after(int(self.time_interval * self.wait_time), lambda: self.draw_recursive(i + 1))
        else:
            self.sidebar.button_start.state(['!disabled'])
        self.time += self.time_interval

    def update_values(self):
        try:
            self.wait_time = 1000 // self.sidebar.speed_var.get()
        except tk.TclError:
            pass
        try:
            self.scale = self.sidebar.scale_var.get()
        except tk.TclError:
            pass
        try:
            self.block_size = self.sidebar.block_size_var.get()
        except tk.TclError:
            pass

    def start(self):
        self.time = 0
        self.draw_recursive(0)


class Sidebar(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.block_size_var = tk.IntVar()
        block_size_label = ttk.Label(self, text='Block Size')
        block_size_spinbox = ttk.Spinbox(self, textvariable=self.block_size_var, justify=tk.CENTER, from_=2, to_=30)
        int_validate(block_size_spinbox, (2, 30))
        self.block_size_var.set(10)

        self.scale_var = tk.IntVar()
        scale_label = ttk.Label(self, text='Scale')
        scale_spinbox = ttk.Spinbox(self, textvariable=self.scale_var, justify=tk.CENTER, from_=5, to_=100)
        int_validate(scale_spinbox, (5, 50))
        self.scale_var.set(30)

        self.speed_var = tk.IntVar()
        speed_label = ttk.Label(self, text='Speed')
        speed_spinbox = ttk.Spinbox(self, textvariable=self.speed_var, justify=tk.CENTER, from_=1, to_=30)
        int_validate(speed_spinbox, (5, 50))
        self.speed_var.set(1)

        self.message = tk.Message(self, font=('consolas', 10))
        self.button_start = ttk.Button(self, text='Start')

        block_size_label.pack()
        block_size_spinbox.pack(pady=(0, 10))
        scale_label.pack()
        scale_spinbox.pack(pady=(0, 10))
        speed_label.pack()
        speed_spinbox.pack(pady=(0, 10))
        self.message.pack(fill=tk.BOTH)
        self.button_start.pack(pady=(6, 10))


class TkViewer:
    def __init__(self, *args, message='', **kwargs):
        self.gui = TkViewer2dGui(*args, **kwargs)
        self.gui.sidebar.button_start.config(command=self.on_start)
        self.gui.sidebar.message.config(text=message)

    def on_start(self):
        self.gui.sidebar.button_start.state(['disabled'])
        self.gui.start()


def view_2d(rows, cols, solution, description):
    root = tk.Tk()
    root.wm_title('Block Viewer')
    viewer = TkViewer(root, rows, cols, solution, message=description)
    viewer.gui.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
