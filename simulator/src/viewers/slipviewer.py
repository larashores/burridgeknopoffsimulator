from tkinter import ttk
import tkinter as tk
import numpy as np
import datetime

from src.simulation.blockarray import BlockArray
from viewers.intvalidate import int_validate


class SlipViewerGui(ttk.Frame):
    LABEL_TEXT = 'Time: {:.1f}'
    def __init__(self, parent, data, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.time = 0
        self.data = data
        self.time_interval = data.run_info.time_interval

        self.sidebar = SlipSidebar(self)
        self.separator = ttk.Separator(self, orient=tk.VERTICAL)
        self.time_label = ttk.Label(self, text=self.LABEL_TEXT.format(self.time))
        self.canvas = tk.Canvas(self)

        self.sidebar.pack(fill=tk.Y, side=tk.RIGHT)
        self.separator.pack(fill=tk.Y, padx=5, pady=10, side=tk.RIGHT)
        self.time_label.pack()
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.update_values()

    def draw_blocks(self, timeslice):
        rows, cols = self.data.run_info.rows, self.data.run_info.cols
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        start_x = (width - cols*self.block_size) / 2
        start_y = (height - rows*self.block_size) / 2
        block_array = BlockArray(timeslice, cols)
        for i in range(rows):
            for j in range(cols):
                velocity = block_array.velocities[i, j]
                color = 'black' if velocity > 0.01 else 'white'
                x, y = start_x + self.block_size * j, start_y + self.block_size * i
                self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill=color)

    def draw_recursive(self, i):
        start = datetime.datetime.now().timestamp()
        self.update_values()
        self.time_label.config(text=self.LABEL_TEXT.format(self.time))
        self.canvas.delete(tk.ALL)
        self.draw_blocks(self.data.values_list[i].get())
        end = datetime.datetime.now().timestamp()
        if i < len(self.data.values_list) - 1:
            self.after(int(self.time_interval * self.wait_time - (end - start) * 1e3), lambda: self.draw_recursive(i + 1))
        else:
            self.sidebar.button_start.state(['!disabled'])
        self.time += self.time_interval

    def update_values(self):
        try:
            self.block_size = self.sidebar.block_size_var.get()
        except tk.TclError:
            pass
        try:
            self.wait_time = 1000 // self.sidebar.speed_var.get()
        except tk.TclError:
            pass

    def start(self):
        self.time = 0
        self.draw_recursive(0)


class SlipSidebar(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.block_size_var = tk.IntVar()
        block_size_label = ttk.Label(self, text='Block Size')
        block_size_spinbox = ttk.Spinbox(self, textvariable=self.block_size_var, justify=tk.CENTER, from_=5, to_=100)
        int_validate(block_size_spinbox, (5, 50))
        self.block_size_var.set(30)

        self.speed_var = tk.IntVar()
        speed_label = ttk.Label(self, text='Speed')
        speed_spinbox = ttk.Spinbox(self, textvariable=self.speed_var, justify=tk.CENTER, from_=1, to_=30)
        int_validate(speed_spinbox, (5, 50))
        self.speed_var.set(1)

        self.message = tk.Message(self, font=('consolas', 10))
        self.button_start = ttk.Button(self, text='Start')

        block_size_label.pack()
        block_size_spinbox.pack(pady=(0, 10))
        speed_label.pack()
        speed_spinbox.pack(pady=(0, 10))
        self.message.pack(fill=tk.BOTH)
        self.button_start.pack(pady=(6, 10))


class SlipViewer:
    def __init__(self, *args, message='', **kwargs):
        self.gui = SlipViewerGui(*args, **kwargs)
        self.gui.sidebar.button_start.config(command=self.on_start)
        self.gui.sidebar.message.config(text=message)

    def on_start(self):
        self.gui.sidebar.button_start.state(['disabled'])
        self.gui.start()


def view_slip(data, description):
    root = tk.Tk()
    root.wm_title('Block Viewer')
    viewer = SlipViewer(root, data, message=description)
    viewer.gui.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
