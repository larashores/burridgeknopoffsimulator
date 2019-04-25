"""
Provides facilities for graphing in matplotlib. See draw_graph for the main drawing function
"""
from graphing.suplot import SubPlot
from signal import Signal

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk


class TkFigure(ttk.Frame):
    DEFAULT_FONT_SIZE = 23
    DEFAULT_TITLE_SIZE = 25

    def __init__(self, root, subplots, title=''):
        ttk.Frame.__init__(self, root)
        self.signal_mouse_press = Signal()
        self.signal_mouse_release = Signal()
        self._fig = Figure()
        self._subplots = []
        self._canvas = FigureCanvas(self._fig, self)
        self._canvas.get_tk_widget().pack(expand=tk.YES, fill=tk.BOTH)
        self._canvas.mpl_connect('button_press_event', self.signal_mouse_press)
        self._canvas.mpl_connect('button_release_event', self.signal_mouse_release)
        toolbar = NavigationToolbar2Tk(self._canvas, self)
        toolbar.update()

        num_rows = len(subplots)
        num_columns = max(len(graphs) for graphs in subplots)
        for i in range(num_rows):
            for j in range(num_columns):
                subplot = subplots[i][j]
                if subplot is not None:
                    index = (i * num_columns) + j + 1
                    ax = self._fig.add_subplot(num_rows, num_columns, index)
                    subplot.set_axis(ax)
                    self._subplots.append(subplot)
        self._fig.suptitle(title, fontweight='bold', fontsize=self.DEFAULT_TITLE_SIZE)
        self._fig.subplots_adjust(hspace=.6, wspace=.3)

    def draw(self):
        for subplot in self._subplots:
            subplot.draw()

    def update_plot(self):
        self._canvas.draw()
        self._canvas.flush_events()


def draw(subplots, title=''):
    """
    Draws subplots on a new Tk root window and runs mainloop until it's closed

    Args:
        subplots: A 2d sequence of SubPlot objects. It's a list of columns and each column contains the SubPlot's that
            need to be drawn
        title: The title for the tk window and for the plot
    """
    if type(subplots) == SubPlot:
        subplots = [[subplots]]
    root = tk.Tk()
    root.title(title if title else 'Plot')
    root.geometry("1050x700")
    figure = TkFigure(root, subplots, title)
    figure.draw()
    figure.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
