from src.graphing.curve_fit import CurveFit


class Graph:
    """
    Provides values that should be plotted on a subplot. Optionally a linear regression can be calculated for the data

    Attributes:
        x_values: A sequence of values to be plotted on the x axis. Should have the same length as y_values
        y_values: A sequence of values to be plotted on the y axis. Should have the same length as x_values
        regression: If this is true this will draw a linear regression for the plot
        legend_label: If a string is provided the graph will be included in the subplot legend

    """
    def __init__(self, x_values, y_values, *, x_errors=None, y_errors=None,
                 curve_fits=None, curve_store=None, legend_label=None, color=None,
                 plot_type='o', plot_size=13):
        """
        Creates a new GraphSettings object

        Args:
            x_values: A sequence of values to be plotted on the x axis. Should have the same length as y_values
            y_values: A sequence of values to be plotted on the y axis. Should have the same length as x_values
            regression: If this is true this will draw a linear regression for the plot
            legend_label: If a string is provided the graph will be included in the subplot legend
        """
        self.x_values = x_values
        self.y_values = y_values
        self.legend_label = legend_label
        self.plot_type = plot_type
        self.x_error = x_errors
        self.y_error = y_errors
        self.color = color
        if type(curve_fits) == CurveFit:
            curve_fits = [curve_fits]
        self.curve_fits = curve_fits
        self.curve_store = curve_store
        self.plot_size = plot_size
