from graphing.graphing import *
import numpy as np


def test(solver):
    exponential = lambda t, values: values
    ode = solver(exponential, step_size=.01)
    ode.set_initial_values([1])
    times = []
    values = []
    while ode.t < 4:
        values.append(ode.step())
        times.append(ode.t)
    ts = np.linspace(0, 4, 1000)
    ys = np.e**ts
    graph = Graph(times, values, plot_type='-', legend_label='solver')
    graph2 = Graph(ts, ys, plot_type='-', legend_label='exact')
    draw(SubPlot(graph, graph2))