from src.graphing.graphing import *


def view_energy(times, energies):
    graph = Graph(times, energies, plot_type='-')
    subplot = SubPlot(graph, x_label='Time', y_label='Energy')
    draw(subplot, title='Potential Energy')