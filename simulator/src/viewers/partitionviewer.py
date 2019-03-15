import tkinter as tk
from tkinter import ttk
import numpy as np
import bisect

from graphing.draw import TkFigure
from graphing.graphing import *
from viewers.floatvalidate import float_validate
from styles import configure_styles
from signal import Signal
from files.util import write_data
import utilities


def gutenburg_richter_law(magnitude, a, b):
    return np.e**(a - b * magnitude)


def gutenburg_richter_law_logarthimic(magnitude, a, b):
    return a - b * magnitude


class Sidebar(ttk.Frame):
    def __init__(self, parent, min_, max_, fit_start, fit_end):
        ttk.Frame.__init__(self, parent)
        fit_settings_label = ttk.Label(self, text='Fit Settings', style='Subtitle.TLabel')

        self.start_var = tk.DoubleVar()
        start_label = ttk.Label(self, text='Start Magnitude')
        start_spinbox = ttk.Spinbox(self, textvariable=self.start_var, justify=tk.CENTER,
                                    from_=min_, to_=max_-1, increment=0.1, format='%.02f')
        float_validate(start_spinbox)
        self.start_var.set(f'{round(fit_start, 1):.02f}')

        self.end_var = tk.DoubleVar()
        end_label = ttk.Label(self, text='End Magnitude')
        end_spinbox = ttk.Spinbox(self, textvariable=self.end_var, justify=tk.CENTER,
                                  from_=min_, to_=max_-1, increment=0.1, format='%.02f')
        float_validate(end_spinbox)
        self.end_var.set(f'{round(fit_end, 1):.02f}')

        self.button_fit_signal = Signal()
        self.button_save_signal = Signal()
        self.button_reset_signal = Signal()
        self._button_fit = ttk.Button(self, text='Curve Fit', command=self.button_fit_signal)
        self._button_save = ttk.Button(self, text='Save', command=self.button_save_signal)
        self._button_reset = ttk.Button(self, text='Reset', command=self.button_reset_signal)

        fit_settings_label.pack()
        start_label.pack()
        start_spinbox.pack(pady=(0, 10))
        end_label.pack()
        end_spinbox.pack(pady=(0, 10))
        self._button_fit.pack(pady=3)
        self._button_save.pack(pady=3)
        self._button_reset.pack(pady=(3, 10))


class PartitionViewer(ttk.Frame):
    def __init__(self, parent, partition, file_name):
        ttk.Frame.__init__(self, parent)
        self._partition = partition
        self._file_name = file_name
        self._make_data()
        self._make_subplots()
        self._last_fits = []
        self._sidebar = Sidebar(parent, self._event_magnitudes[0], self._event_magnitudes[-1],
                                partition.fit_start, partition.fit_end)
        self._figure = TkFigure(self, self._subplots, title=f'{partition.run_info.rows}x{partition.run_info.cols}')
        self._figure.draw()
        self._sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        self._figure.pack(expand=tk.YES, fill=tk.BOTH)

        self._sidebar.button_fit_signal.connect(self.on_fit)
        self._sidebar.button_save_signal.connect(self.on_save)
        self._sidebar.button_reset_signal.connect(self.on_reset)

        self.on_fit()

    def _make_data(self):
        magnitudes = []
        for slip_event in self._partition.slip_events:
            distance = sum(single_slip_event.distance for single_slip_event in slip_event)
            if distance > 0:
                magnitudes.append(np.log(distance))

        self._event_magnitudes = np.array(sorted(magnitudes))
        self._magnitude_range = np.linspace(self._event_magnitudes[0], self._event_magnitudes[-1], 100)
        self._events_of_at_least_magnitude = np.empty(len(self._magnitude_range))
        for ind, magnitude in enumerate(self._magnitude_range):
            self._events_of_at_least_magnitude[ind] = sum((lambda x: x >= magnitude)(x) for x in self._event_magnitudes)
        self._log_events_of_at_least_magnitude = np.log(self._events_of_at_least_magnitude)

    def _make_subplots(self):
        options = {'line_width': 2, 'plot_type': '-'}
        subplot_options = {'legend_size': 14}

        linear_graph = Graph(self._magnitude_range, self._events_of_at_least_magnitude, **options)
        logarithmic_graph = Graph(self._magnitude_range, self._log_events_of_at_least_magnitude, **options)

        linear_subplot = SubPlot(linear_graph, x_label='M (Magnitude)', y_label='N', **subplot_options)
        log_subplot = SubPlot(logarithmic_graph, x_label='M (Magnitude)', y_label='log$_{10}$(N)',
                              **subplot_options)
        self._subplots = [[linear_subplot, log_subplot]]

    def on_save(self):
        self._partition.fit_start = self._sidebar.start_var.get()
        self._partition.fit_end = self._sidebar.end_var.get()
        write_data(self._file_name, self._partition)

    def on_reset(self):
        self._sidebar.start_var.set(self._partition.fit_start)
        self._sidebar.end_var.set(self._partition.fit_end)
        self.on_fit()

    def on_fit(self):
        options = {'line_width': 2, 'plot_type': '-'}
        for fit in self._last_fits:
            fit.remove()

        start = bisect.bisect_right(self._magnitude_range, self._sidebar.start_var.get())
        end = bisect.bisect_right(self._magnitude_range, self._sidebar.end_var.get())
        fit_range = slice(start, end)
        try:
            linear_values, _ = utilities.fit_func(gutenburg_richter_law, self._magnitude_range,
                                                  self._events_of_at_least_magnitude, limits=fit_range)
            log_values, _ = utilities.fit_func(gutenburg_richter_law_logarthimic, self._magnitude_range,
                                               self._log_events_of_at_least_magnitude, limits=fit_range)
            gutenburg_x = self._magnitude_range[fit_range]
            gutenburg_y_linear = gutenburg_richter_law(gutenburg_x, *linear_values)
            gutenburg_y_log = gutenburg_richter_law_logarthimic(gutenburg_x, *log_values)
            label = 'a={:.1f} b={:.3f}'

            linear_graph = Graph(gutenburg_x, gutenburg_y_linear, legend_label=label.format(*linear_values), **options)
            log_graph = Graph(gutenburg_x, gutenburg_y_log, legend_label=label.format(*log_values), **options)
            handle1 = self._subplots[0][0].add_graph(linear_graph)
            handle2 = self._subplots[0][1].add_graph(log_graph)
            self._last_fits = handle1, handle2
            self._figure.update_plot()
        except TypeError:
            return


def view_partition(data, file_name):
    root = tk.Tk()
    root.wm_title('Partition Viewer')
    configure_styles()
    viewer = PartitionViewer(root, data, file_name)
    viewer.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
