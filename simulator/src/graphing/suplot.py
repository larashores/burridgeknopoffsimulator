from src.graphing.line import Line
import enum
import warnings
import numpy as np


class LogType(enum.Enum):
    X = 0
    Y = 1
    BOTH = 2
    NONE = 3


class SubPlot:
    """
    Creates a holder class that stores the info to make a single matplotlib subplot. Many GraphSettings could be added
    and various configurations can be changed

    Attributes:
        graphs: A list of GraphSettings that should be plotted
        x_label: The label for the x-axis of this subplot
        y_label: The label for the y-axis of this subplot
        title: The title for this subplot
    """

    def __init__(self, *graphs, x_label='', y_label='', title='', log=None, tick_size=None, axis_label_size=23,
                 title_font_size=23, legend_size=None, x_range=None, y_range=None):
        """
        Creates a new SubPlot object

        Args:
            args: A list of GraphSettings may be provided or they may be provided separately and collected
            x_label: The label for the x-axis of this subplot
            y_label: The label for the y-axis of this subplot
            title: The title for this subplot
        """
        self.graphs = list(graphs)
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.x_log = log in (LogType.X, LogType.BOTH)
        self.y_log = log in (LogType.Y, LogType.BOTH)
        self.tick_size = tick_size
        self.axis_label_size = axis_label_size
        self.title_size = title_font_size
        self.legend_size = legend_size
        self.x_range = x_range
        self.y_range = y_range
        self._axis = None

    def set_axis(self, ax):
        self._axis = ax
        ax.set_ylabel(self.y_label, fontsize=self.axis_label_size)
        ax.set_xlabel(self.x_label, fontsize=self.axis_label_size)
        ax.set_title(self.title, fontsize=self.title_size, fontweight='bold')
        ax.ticklabel_format(axis='y', style='sci')
        ax.ticklabel_format(useOffset=False)
        if self.tick_size:
            for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(self.tick_size)
            for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(self.tick_size)
        if self.x_log:
            ax.set_xscale('log', basey=np.e)
            ax.grid(which='major')
        if self.y_log:
            ax.set_yscale('log', basey=np.e)
            ax.grid(which='minor')
        if self.x_range is not None:
            ax.set_xlim(*self.x_range)
        if self.y_range is not None:
            ax.set_ylim(*self.y_range)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            ax.legend(loc='best', fontsize=self.legend_size)

    def draw(self):
        for graph in self.graphs:
            graph.draw(self._axis, self.x_log, self.y_log)

    def add_graph(self, graph):
        self.graphs.append(graph)
        if self._axis:
            handle = graph.draw(self._axis, self.x_log, self.y_log)
            self._axis.legend()
            return handle
