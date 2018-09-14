from tkinter import ttk
import tkinter as tk


class TkViewer1d(ttk.Frame):
    LABEL_TEXT = 'Time: {:.1f}'
    def __init__(self, *args, solution, time_interval=.1, scale=30, block_size=10,**kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.time = 0
        self.time_label = ttk.Label(self, text=self.LABEL_TEXT.format(self.time))
        self.canvas = tk.Canvas(self)
        self.solution = solution
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
        width = self.winfo_width()
        height = self.winfo_height()
        half_size = self.block_size / 2
        for i, position in enumerate(positions):
            x, y = position * self.scale + self.block_size, height // 2
            self.canvas.create_rectangle(x - half_size, y - half_size, x + half_size, y + half_size)

    def draw_recursive(self, i):
        self.time += self.time_interval
        self.time_label.config(text=self.LABEL_TEXT.format(self.time))
        positions = self.solution[i][::2]
        self.canvas.delete(tk.ALL)
        self.draw_blocks(positions)
        if i < len(self.solution) - 1:
            self.after(int(self.time_interval * 200), lambda: self.draw_recursive(i + 1))

    def start(self):
        self.time = 0 - self.time_interval
        self.draw_recursive(0)


def view_1d(solution):
    root = tk.Tk()
    root.geometry('1600x600')
    viewer = TkViewer1d(root, solution=solution)
    button = ttk.Button(root, text='Start', command=lambda: viewer.start())
    viewer.pack(expand=tk.YES, fill=tk.BOTH)
    button.pack()
    root.mainloop()
