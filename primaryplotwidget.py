import errno
import itertools
import os

from PyQt5.QtWidgets import QGridLayout, QWidget
from mytools.plotwidget import PlotWidget


class PrimaryPlotWidget(QWidget):

    def __init__(self, parent=None, model=None):
        super().__init__(parent)
        self._model = model

        self._plot = PlotWidget(parent=None, toolbar=True)

        self._grid = QGridLayout()
        self._grid.addWidget(self._plot, 0, 0)
        self.setLayout(self._grid)

        self._init()

    def _init(self):
        self._plot.subplots_adjust(bottom=0.150)
        self._plot.set_xlabel(self._model.xLabel)
        self._plot.set_ylabel(self._model.yLabel)
        self._plot.grid(b=True, which='major', color='0.5', linestyle='-')

    def clear(self):
        self._plot.clear()

    def plot(self):
        self.clear()
        self._init()

        self._plot.plot(self._model.xs, self._model.ys)
        self._plot.plot(self._model.xs, self._model.filteredYs)
