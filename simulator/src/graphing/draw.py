"""
Provides facilities for graphing in matplotlib. See draw_graph for the main drawing function
"""
from src.graphing.suplot import SubPlot

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk


class TkFigure(ttk.Frame):
    DEFAULT_FONT_SIZE = 23
    DEFAULT_TITLE_SIZE = 25

    def __init__(self, root, subplots, title=''):
        ttk.Frame.__init__(self, root)
        self._fig = Figure()
        canvas = FigureCanvas(self._fig, self)
        canvas.get_tk_widget().pack(expand=tk.YES, fill=tk.BOTH)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()

        num_rows = len(subplots)
        num_columns = max(len(graphs) for graphs in subplots)
        for i in range(num_rows):
            for j in range(num_columns):
                subplot = subplots[i][j]
                if subplot is not None:
                    index = (i * num_columns) + j + 1
                    ax = self._fig.add_subplot(num_rows, num_columns, index)
                    subplot.draw(ax)
        self._fig.suptitle(title, fontweight='bold', fontsize=self.DEFAULT_TITLE_SIZE)
        self._fig.subplots_adjust(hspace=.6, wspace=.3)


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
    figure.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
