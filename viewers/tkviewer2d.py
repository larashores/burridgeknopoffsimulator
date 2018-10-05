from tkinter import ttk
import tkinter as tk

from util import TwoDimBlockArray


class TkViewer2d(ttk.Frame):
    LABEL_TEXT = 'Time: {:.1f}'
    def __init__(self, parent, rows, cols, solution, time_interval=.1, scale=30, block_size=10, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.rows = rows
        self.cols = cols
        self.solution = solution
        self.time = 0
        self.time_label = ttk.Label(self, text=self.LABEL_TEXT.format(self.time))
        self.canvas = tk.Canvas(self)
        self.scale = scale
        self.block_size = block_size
        self.time_interval = time_interval
        num_blocks = solution.shape[1] // 2
        min_position = -float('inf')
        max_position = float('inf')
        for values in solution:
            for i in range(num_blocks):
                position = values[2*i]
                min_position = min(min_position, position)
                max_position = max(max_position, position)
        self.time_label.pack()
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    def draw_blocks(self, positions):
        height = self.winfo_height()
        half_size = self.block_size / 2
        block_array = TwoDimBlockArray(positions, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                x_pos = block_array.positions[i, j]
                x, y = x_pos * self.scale + self.block_size, (height // 2) - (i * self.block_size * 2)
                self.canvas.create_rectangle(x - half_size, y - half_size, x + half_size, y + half_size)

    def draw_recursive(self, i):
        self.time += self.time_interval
        self.time_label.config(text=self.LABEL_TEXT.format(self.time))
        self.canvas.delete(tk.ALL)
        self.draw_blocks(self.solution[i])
        if i < len(self.solution) - 1:
            self.after(int(self.time_interval * 200), lambda: self.draw_recursive(i + 1))

    def start(self):
        self.time = 0 - self.time_interval
        self.draw_recursive(0)


def view_2d(rows, cols, solution):
    root = tk.Tk()
    root.geometry('1600x600')
    viewer = TkViewer2d(root, rows, cols, solution)
    button = ttk.Button(root, text='Start', command=lambda: viewer.start())
    viewer.pack(expand=tk.YES, fill=tk.BOTH)
    button.pack()
    root.mainloop()
