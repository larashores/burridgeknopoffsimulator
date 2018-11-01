import collections


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
    def __init__(self, *args, x_label='', y_label='', title='', log=None, tick_size=None, axis_label_size=None):
        """
        Creates a new SubPlot object

        Args:
            args: A list of GraphSettings may be provided or they may be provided separately and collected
            x_label: The label for the x-axis of this subplot
            y_label: The label for the y-axis of this subplot
            title: The title for this subplot
        """
        if isinstance(args[0], collections.Sequence):
            self.graphs = args[0]
        else:
            self.graphs = args
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.x_log = True if log == 'x' or log == 'both' else False
        self.y_log = True if log == 'y' or log == 'both' else False
        self.tick_size = tick_size
        self.axis_label_size = axis_label_size