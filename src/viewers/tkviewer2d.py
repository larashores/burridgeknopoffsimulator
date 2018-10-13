from tkinter import ttk
import tkinter as tk
import numpy as np

from src.simulation.blockarray import BlockArray


class TkViewer2d(ttk.Frame):
    LABEL_TEXT = 'Time: {:.1f}'
    def __init__(self, parent, rows, cols, solution, time_interval=.1, spring_length=1, velocity=.1, scale=30, block_size=10, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.rows = rows
        self.cols = cols
        self.solution = solution
        self.time = 0
        self.spring_length = spring_length
        self.velocity = velocity
        self.time_label = ttk.Label(self, text=self.LABEL_TEXT.format(self.time))
        self.canvas = tk.Canvas(self)
        self.scale = scale
        self.block_size = block_size
        self.time_interval = time_interval
        self.time_label.pack()
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    def draw_blocks(self, positions):
        width = self.winfo_width()
        height = self.winfo_height()
        distance = (self.spring_length * self.scale)
        start_x = (width - (self.rows-1)*distance - self.block_size) / 2
        start_y = (height - (self.cols-1)*distance - self.block_size) / 2
        block_array = BlockArray(positions, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                x_pos = block_array.positions[i, j]
                x, y = start_x + x_pos * self.scale, start_y + distance * i
                self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size)

    def draw_recursive(self, i):
        self.time += self.time_interval
        self.time_label.config(text=self.LABEL_TEXT.format(self.time))
        self.canvas.delete(tk.ALL)
        self.draw_blocks(np.array(self.solution[i]))
        if i < len(self.solution) - 1:
            self.after(int(self.time_interval * 200), lambda: self.draw_recursive(i + 1))

    def start(self):
        self.time = 0 - self.time_interval
        self.draw_recursive(0)


def view_2d(rows, cols, solution, velocity):
    root = tk.Tk()
    viewer = TkViewer2d(root, rows, cols, solution, velocity=velocity)
    button = ttk.Button(root, text='Start', command=lambda: viewer.start())
    viewer.pack(expand=tk.YES, fill=tk.BOTH)
    button.pack()
    root.mainloop()
