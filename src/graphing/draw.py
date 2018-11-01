"""
Provides facilities for graphing in matplotlib. See draw_graph for the main drawing function
"""
from src.graphing.histogram import Histogram
from src.graphing.graph import Graph
from src.graphing.suplot import SubPlot

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas, NavigationToolbar2Tk
from matplotlib.figure import Figure
import warnings

import numpy as np

import tkinter as tk
from tkinter import ttk

from src.utilities import uncertainty_str, fit_func


def create_figure(root_window):
    """
    Given a tkinter widget, this will create a FigureCanvas as a root of that widget and pack it

    Args:
        root_window: A tkinter widget to pack the canvas in

    Returns:
        The Figure object
    """
    frame = ttk.Frame(root_window)
    fig = Figure()
    canvas = FigureCanvas(fig, frame)
    toolbar = NavigationToolbar2Tk(canvas, frame)

    frame.pack(expand=tk.YES, fill=tk.BOTH)
    canvas.get_tk_widget().pack(expand=tk.YES, fill=tk.BOTH)

    toolbar.update()

    return fig


def make_fit_string(fit_string, values, dvalues):
    strings = []
    for value, dvalue in zip(values, dvalues):
        strings.append('(' + uncertainty_str(value, dvalue) + ')')
    return fit_string.format(*strings)


def _draw_historgram(axis, histogram):
    if histogram.bins is not None:
        axis.hist(histogram.values, bins=histogram.bins)
    else:
        axis.hist(histogram.values)


def _draw_graph(axis, graph, x_log=False):
    if not (graph.x_error is None and graph.y_error is None):
        line = axis.errorbar(graph.x_values, graph.y_values, graph.y_error, graph.x_error, graph.plot_type,
                             color=graph.color)[0]
    else:
        line = axis.plot(graph.x_values, graph.y_values, graph.plot_type, ms=graph.plot_size, color=graph.color)[0]
    if graph.curve_fits is not None:
        for fit in graph.curve_fits:
            optimal, stddev = fit_func(fit.func,
                                       graph.x_values, graph.y_values, graph.x_error, graph.y_error, limits=fit.limits,
                                       guesses=fit.guesses)
            fit.values = optimal
            fit.dvalues = stddev
            trimmed = graph.x_values[fit.limits[0]:fit.limits[1]] if fit.limits else graph.x_values
            min_ = min(trimmed)
            max_ = max(trimmed)
            if x_log:
                values = np.logspace(np.log10(min_), np.log10(max_), 1000)
            else:
                values = np.linspace(min_, max_, 1000)
            regression = axis.plot(values, fit.func(values, *optimal))[0]
            regression.set_color(line._color)
            if fit.string:
                name = ' for ' + graph.legend_label if graph.legend_label is not None else ''
                print("Best-fit{}: {}".format(name, make_fit_string(fit.string, optimal, stddev)))

        if graph.legend_label is not None:
            if graph.curve_fits:
                regression.set_label(graph.legend_label)
            else:
                line.set_label(graph.legend_label)
        axis.legend().remove()


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
    font_size = 23
    title_size = 25
    root = tk.Tk()
    root.title(title if title else 'Plot')
    root.geometry("1050x700")
    fig = create_figure(root)

    num_rows = len(subplots)
    num_columns = max(len(graphs) for graphs in subplots)

    for i in range(num_rows):
        for j in range(num_columns):
            subplot = subplots[i][j]
            if subplot is None:
                continue
            axis_label_size = font_size if subplot.axis_label_size is None else subplot.axis_label_size
            index = (i*num_columns)+j+1
            ax = fig.add_subplot(num_rows, num_columns, index)
            ax.set_ylabel(subplot.y_label, fontsize=axis_label_size)
            ax.set_xlabel(subplot.x_label, fontsize=axis_label_size)
            ax.set_title(subplot.title, fontsize=font_size, fontweight='bold')
            ax.ticklabel_format(axis='y', style='sci')
            ax.ticklabel_format(useOffset=False)
            for graph in subplot.graphs:
                if type(graph) == Histogram:
                    _draw_historgram(ax, graph)
                elif type(graph) == Graph:
                    _draw_graph(ax, graph, x_log=subplot.x_log)
            if subplot.tick_size:
                for tick in ax.xaxis.get_major_ticks():
                    tick.label.set_fontsize(subplot.tick_size)
                for tick in ax.yaxis.get_major_ticks():
                    tick.label.set_fontsize(subplot.tick_size)
            spacing = 2
            if subplot.x_log:
                ax.set_xscale('log')
                # x_lim = ax.get_xlim()
                # ax.set_xlim(x_lim[0]/spacing, x_lim[1]*spacing)
                ax.grid(which='both')
            if subplot.y_log:
                ax.set_yscale('log')
                # y_lim = ax.get_ylim()
                # ax.set_ylim(y_lim[0]/spacing, y_lim[1]*spacing*3)
                ax.grid(which='both')

            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                ax.legend(loc='best')

    fig.suptitle(title, fontweight='bold', fontsize=title_size)
    fig.subplots_adjust(hspace=.6, wspace=.3)
    root.mainloop()
