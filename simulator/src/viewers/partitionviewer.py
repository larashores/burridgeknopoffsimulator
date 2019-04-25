import tkinter as tk
from tkinter import ttk
import numpy as np
import bisect

from files.partition import FitLimit, FitList
from graphing.draw import TkFigure
from graphing.graphing import *
from viewers.floatvalidate import float_validate
from viewers.listchoice import ListChoice
from styles import configure_styles
from signal import Signal
from files.util import write_data
import utilities


def gutenburg_richter_law(magnitude, a, b):
    return np.e**(a - b * magnitude)


def gutenburg_richter_law_logarthimic(magnitude, a, b):
    return a - b * magnitude


class Sidebar(ttk.Frame):
    def __init__(self, parent, min_, max_, fit_list):
        ttk.Frame.__init__(self, parent)
        self._fit_list = fit_list
        fit_settings_label = ttk.Label(self, text='Fit Settings', style='Subtitle.TLabel')

        self.start_var = tk.DoubleVar()
        start_label = ttk.Label(self, text='Start Magnitude')
        start_spinbox = ttk.Spinbox(self, textvariable=self.start_var, justify=tk.CENTER,
                                    from_=min_, to_=max_-1, increment=0.1, format='%.02f')
        float_validate(start_spinbox)
        self.start_var.trace('w', self._on_set_start)

        self.end_var = tk.DoubleVar()
        end_label = ttk.Label(self, text='End Magnitude')
        end_spinbox = ttk.Spinbox(self, textvariable=self.end_var, justify=tk.CENTER,
                                  from_=min_, to_=max_-1, increment=0.1, format='%.02f')
        float_validate(end_spinbox)
        self.end_var.trace('w', self._on_set_end)

        seperator1 = ttk.Separator(self, orient=tk.HORIZONTAL)
        self._list_choice = ListChoice(self)
        self._list_choice.signal_select.connect(self._on_select)

        self.button_fit_signal = Signal()
        self.button_save_signal = Signal()
        self.button_reset_signal = Signal()
        self._button_add = ttk.Button(self, text='Add Fit', command=self._on_add)
        self._button_fit = ttk.Button(self, text='Do Fit', command=self.button_fit_signal)
        seperator2 = ttk.Separator(self, orient=tk.HORIZONTAL)
        self._button_save = ttk.Button(self, text='Save', command=self.button_save_signal)
        self._button_reset = ttk.Button(self, text='Reset', command=self._on_reset)

        fit_settings_label.pack()
        start_label.pack()
        start_spinbox.pack(pady=(0, 10))
        end_label.pack()
        end_spinbox.pack(pady=(0, 5))
        self._button_fit.pack(pady=(0, 3))
        seperator1.pack(fill=tk.X, padx=5, pady=3)
        self._list_choice.pack()
        self._button_add.pack(pady=3)
        seperator2.pack(fill=tk.X, padx=5, pady=3)
        self._button_save.pack(pady=3)
        self._button_reset.pack(pady=(3, 10))

        for fit in fit_list:
            self._list_choice.append(fit)
        if len(self._list_choice):
            self._list_choice.set_selection(0)
        else:
            self._on_add()

    def set_fit_list(self, fit_list):
        self._fit_list = fit_list

    def _on_add(self):
        limit = FitLimit()
        self._fit_list.append(limit)
        self._list_choice.append(limit)
        self._list_choice.set_selection(-1)

    def _on_reset(self):
        self.button_reset_signal()
        self._list_choice.clear()
        for fit in self._fit_list:
            self._list_choice.append(fit)
        if len(self._list_choice):
            self._list_choice.set_selection(-1)

    def _on_set_start(self, name, ind, op):
        ind = self._list_choice.get_selection()
        if ind is not None:
            try:
                self._fit_list[ind].fit_start = self.start_var.get()
                self._list_choice.update_line(ind, self._list_choice[ind])
            except tk.TclError:
                pass

    def _on_set_end(self, name, ind, op):
        ind = self._list_choice.get_selection()
        if ind is not None:
            try:
                self._fit_list[ind].fit_end = self.end_var.get()
                self._list_choice.update_line(ind, self._list_choice[ind])
            except tk.TclError:
                pass

    def _on_select(self, ind):
        if ind is not None:
            self.start_var.set(f'{round(self._fit_list[ind].fit_start, 1):.02f}')
            self.end_var.set(f'{round(self._fit_list[ind].fit_end, 1):.02f}')


class PartitionViewer(ttk.Frame):
    def __init__(self, parent, partition, file_name):
        ttk.Frame.__init__(self, parent)
        self._selecting = False
        self._partition = partition
        self._original_fit_list = FitList.from_bytes(partition.fit_list.to_bytes())[0]
        self._file_name = file_name
        self._make_data()
        self._make_subplots()
        self._last_fits = []
        self._sidebar = Sidebar(parent, self._event_magnitudes[0], self._event_magnitudes[-1], partition.fit_list)
        self._figure = TkFigure(self, self._subplots, title=f'{partition.run_info.rows}x{partition.run_info.cols}')
        self._figure.signal_mouse_press.connect(self._on_mouse_press)
        self._figure.signal_mouse_release.connect(self._on_mouse_release)
        self._figure.draw()
        self._sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        self._figure.pack(expand=tk.YES, fill=tk.BOTH)

        self._sidebar.button_fit_signal.connect(self.on_fit)
        self._sidebar.button_save_signal.connect(self.on_save)
        self._sidebar.button_reset_signal.connect(self.on_reset)

        self.on_fit()

    def _on_mouse_press(self, event):
        if event.key == 'control' and event.xdata is not None and event.ydata is not None:
            self._sidebar.start_var.set(round(event.xdata, 2))
            self._selecting = True

    def _on_mouse_release(self, event):
        self._figure._canvas.get_tk_widget().focus_set()
        if self._selecting and event.key == 'control' and event.xdata is not None and event.ydata is not None:
            self._sidebar.end_var.set(round(event.xdata, 2))
            self._selecting = False

    def _make_data(self):
        magnitudes = []
        num_blocks = []
        for slip_event in self._partition.slip_events:
            is_edge = any(sse.col == 0 or sse.col == self._partition.run_info.cols - 1 for sse in slip_event)
            if is_edge:
                continue
            distance = sum(single_slip_event.distance for single_slip_event in slip_event)
            if distance > 0 and len(slip_event) < (self._partition.run_info.rows * self._partition.run_info.cols):
                magnitudes.append(np.log(distance))
                num_blocks.append(len(slip_event))

        self._events = np.array(magnitudes)
        self._num_blocks = np.array(num_blocks)
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
        graph = Graph(self._events, self._num_blocks, plot_size=2)

        linear_subplot = SubPlot(linear_graph, x_label='M (Magnitude)', y_label='N', **subplot_options)
        log_subplot = SubPlot(logarithmic_graph, x_label='M (Magnitude)', y_label='ln(N)',
                              **subplot_options)
        subplot = SubPlot(graph, x_label='Event Magnitude', y_label='Number of Blocks')
        self._subplots = [[linear_subplot, log_subplot, subplot]]

    def on_save(self):
        write_data(self._file_name, self._partition)

    def on_reset(self):
        self._partition.fit_list = self._original_fit_list
        self._sidebar.set_fit_list(self._partition.fit_list)
        self._original_fit_list = FitList.from_bytes(self._partition.fit_list.to_bytes())[0]
        self.on_fit()

    def on_fit(self):
        options = {'line_width': 2, 'plot_type': '-'}
        for fit in self._last_fits:
            fit.remove()
        self._last_fits.clear()
        for fit in self._partition.fit_list:
            start_ind = bisect.bisect_left(self._magnitude_range, fit.fit_start)
            end_ind = bisect.bisect_right(self._magnitude_range, fit.fit_end)
            fit_range = slice(start_ind, end_ind)
            try:
                linear_values, _ = utilities.fit_func(gutenburg_richter_law, self._magnitude_range,
                                                      self._events_of_at_least_magnitude, limits=fit_range)
                log_values, _ = utilities.fit_func(gutenburg_richter_law_logarthimic, self._magnitude_range,
                                                   self._log_events_of_at_least_magnitude, limits=fit_range)
                gutenburg_x = self._magnitude_range[fit_range]
                gutenburg_y_linear = gutenburg_richter_law(gutenburg_x, *linear_values)
                gutenburg_y_log = gutenburg_richter_law_logarthimic(gutenburg_x, *log_values)
                label = 'a={:.1f} b={:.3f}'

                linear_graph = Graph(gutenburg_x, gutenburg_y_linear, legend_label=label.format(*log_values), **options)
                log_graph = Graph(gutenburg_x, gutenburg_y_log, legend_label=label.format(*log_values), **options)
                handle1 = self._subplots[0][0].add_graph(linear_graph)
                handle2 = self._subplots[0][1].add_graph(log_graph)
                handle3 = self._subplots[0][2].add_graph(Line(fit.fit_start, color='black'))
                handle4 = self._subplots[0][2].add_graph(Line(fit.fit_end, color='black'))
                self._last_fits.extend([handle1, handle2, handle3, handle4])
                self._figure.update_plot()
            except TypeError:
                continue


def view_partition(data, file_name):
    root = tk.Tk()
    root.wm_title('Partition Viewer')
    configure_styles()
    viewer = PartitionViewer(root, data, file_name)
    viewer.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
