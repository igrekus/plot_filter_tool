import pandas as pd

from PyQt5.QtCore import QObject, pyqtSignal
from scipy.signal import savgol_filter


class PlotModel(QObject):
    headersChanged = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._currentFile = ''
        self._df = None
        self._xLabel = ''
        self._yLabel = ''

        self._headers = list()
        self._xs = list()
        self._ys = list()
        self._filteredYs = list()

    def openExcel(self, file):
        print(f'load dataset{file}')
        self._currentFile = file
        self._df: pd.DataFrame = pd.read_excel(self._currentFile, sheet_name=0)
        self.headers = list(self._df.columns)

    def _clear(self):
        self._headers.clear()
        self._xs.clear()
        self._ys.clear()
        self._filteredYs.clear()

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value
        self.headersChanged.emit(value)

    @property
    def xLabel(self):
        return self._xLabel

    @xLabel.setter
    def xLabel(self, value):
        self._xLabel = value
        self._xs = list(self._df[self._xLabel])

    @property
    def yLabel(self):
        return self._yLabel

    @yLabel.setter
    def yLabel(self, value):
        self._yLabel = value
        self._ys = list(self._df[self._yLabel])
        self._updateFilter()

    def _updateFilter(self):
        self._filteredYs = savgol_filter(self._ys, 9, 3)

    @property
    def xs(self):
        return self._xs

    @property
    def ys(self):
        return self._ys

    @property
    def filteredYs(self):
        return self._filteredYs
