from tkinter import ttk
import tkinter as tk
import datetime
import math

from src.simulation.blockarray import BlockArray
from viewers.intvalidate import int_validate


class BlockViewerGui(ttk.Frame):
    LABEL_TEXT = 'Time: {:.1f}'

    def __init__(self, parent, data, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.time = 0
        self._data = data

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
        rows, cols = self._data.run_info.rows, self._data.run_info.cols
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        distance = (self._data.run_info.spring_length * self.scale)
        start_x = (width - (cols-1)*distance - self.block_size) / 2
        start_y = (height - (rows-1)*distance - self.block_size) / 2
        block_array = BlockArray(positions, cols)
        for i in range(rows):
            for j in range(cols):
                velocity = block_array.velocities[i, j]
                color = 'black' if velocity > 0.01 else 'white'
                x_pos = block_array.positions[i, j]
                x, y = start_x + x_pos * self.scale, start_y + distance * i
                self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill=color)

        x1 = 0
        num = 0
        while x1 < width:
            x1 = int((width / 2) + num * self.scale)
            x2 = int((width / 2) - num * self.scale)
            self.canvas.create_line(x1, height, x1, height - 20)
            self.canvas.create_line(x2, height, x2, height - 20)
            self.canvas.create_text((x1, height - 30), text=str(num))
            self.canvas.create_text((x2, height - 30), text=str(-num))
            num += math.ceil(30 / self.scale)

    def draw_recursive(self, i):
        start = datetime.datetime.now().timestamp()
        self.update_values()
        self.time_label.config(text=self.LABEL_TEXT.format(self.time))
        self.canvas.delete(tk.ALL)
        self.draw_blocks(self._data.values_list[i].get())
        end = datetime.datetime.now().timestamp()
        if i < len(self._data.values_list) - 1:
            self.after(int(self._data.run_info.time_interval * self.wait_time) - int((end - start) * 1e3),
                       lambda: self.draw_recursive(i + 1))
        else:
            self.sidebar.button_start.state(['!disabled'])
        self.time += self._data.run_info.time_interval

    def draw_step(self, i):
        self.update_values()
        self.time_label.config(text=self.LABEL_TEXT.format(self.time))
        self.canvas.delete(tk.ALL)
        self.draw_blocks(self._data.values_list[i].get())
        self.time += self._data.run_info.time_interval
        array = BlockArray(self._data.values_list[i].get(), self._data.run_info.cols)
        print('Step: ', i)
        print('Positions: ', [pos for pos in array.positions])
        print('Velocities: ', [pos for pos in array.velocities])
        print()

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

    def start(self, step):
        self.time = 0
        self.draw_recursive(step)


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
        self.button_step = ttk.Button(self, text='Step')

        block_size_label.pack()
        block_size_spinbox.pack(pady=(0, 10))
        scale_label.pack()
        scale_spinbox.pack(pady=(0, 10))
        speed_label.pack()
        speed_spinbox.pack(pady=(0, 10))
        self.message.pack(fill=tk.BOTH)
        self.button_start.pack(pady=(6, 3))
        self.button_step.pack(pady=(3, 10))


class TkViewer:
    def __init__(self, *args, message='', **kwargs):
        self.gui = BlockViewerGui(*args, **kwargs)
        self.gui.sidebar.button_start.config(command=self.on_start)
        self.gui.sidebar.button_step.config(command=self.on_step)
        self.gui.sidebar.message.config(text=message)
        self.step = 0

    def on_start(self):
        self.gui.sidebar.button_start.state(['disabled'])
        self.gui.start(self.step)

    def on_step(self):
        self.gui.draw_step(self.step)
        self.step += 1


def view_2d(data, description):
    root = tk.Tk()
    root.wm_title('Block Viewer')
    viewer = TkViewer(root, data, message=description)
    viewer.gui.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
