from tkinter import ttk
import tkinter as tk
import numpy as np

from src.simulation.blockarray import BlockArray


class TkViewer2d(ttk.Frame):
    LABEL_TEXT = 'Time: {:.1f}'
    def __init__(self, parent, rows, cols, solution, time_interval=.1, velocity=.1, scale=30, block_size=10, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.rows = rows
        self.cols = cols
        self.solution = solution
        self.time = 0
        self.velocity = velocity
        self.time_label = ttk.Label(self, text=self.LABEL_TEXT.format(self.time))
        self.canvas = tk.Canvas(self)
        self.scale = scale
        self.block_size = block_size
        self.time_interval = time_interval
        self.time_label.pack()
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    def draw_blocks(self, positions):
        height = self.winfo_height()
        half_size = self.block_size / 2
        block_array = BlockArray(positions, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                x_pos = block_array.positions[i, j]
                x, y = x_pos * self.scale + self.block_size, (height // 2) - (i * self.block_size * 2)
                self.canvas.create_rectangle(x - half_size, y - half_size, x + half_size, y + half_size)
        x1 = self.block_size
        x2 = self.block_size + (self.cols * self.scale)
        offset = self.time * self.velocity * self.scale
        y = (height // 2) - (2 * self.block_size * self.rows)
        self.canvas.create_line(x1 + offset, y, x2 + offset, y)

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
    root.geometry('1600x600')
    viewer = TkViewer2d(root, rows, cols, solution, velocity=velocity)
    button = ttk.Button(root, text='Start', command=lambda: viewer.start())
    viewer.pack(expand=tk.YES, fill=tk.BOTH)
    button.pack()
    root.mainloop()
