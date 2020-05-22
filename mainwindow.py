from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex, QStringListModel

from plotmodel import PlotModel
from primaryplotwidget import PrimaryPlotWidget



def is_even(value):
    return value % 2 == 0


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi('mainwindow.ui', self)

        self._plotModel = PlotModel()

        self._xsModel = QStringListModel(parent=self)
        self._ui.listXs.setModel(self._xsModel)

        self._ysModel = QStringListModel(parent=self)
        self._ui.listYs.setModel(self._ysModel)

        self._plotWidget = PrimaryPlotWidget(parent=self, model=self._plotModel)
        self._ui.tabWidget.insertTab(0, self._plotWidget, 'ГРАФОН')

        self._connectSignals()

    def _connectSignals(self):
        self._plotModel.headersChanged[list].connect(self.on_headers_changed)

    @pyqtSlot()
    def on_btnOpenFile_clicked(self):
        fn = self._getFileName()
        if fn:
            self._ui.editFileName.setText(fn)
            self._plotModel.openExcel(fn)

    def _getFileName(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self,
                                                  caption='Открыть книгу Excel...',
                                                  directory='.',
                                                  filter='Excel 2007+ Book (*.xlsx)')
        return filename

    @pyqtSlot(list)
    def on_headers_changed(self, headers):
        self._xsModel.setStringList(list(headers))
        self._ysModel.setStringList(list(headers))

    @pyqtSlot(QModelIndex)
    def on_listXs_clicked(self, _):
        self._plotModel.xLabel = self._ui.listXs.selectionModel().selectedIndexes()[0].data(role=Qt.DisplayRole)
        self._updatePlot()

    @pyqtSlot(QModelIndex)
    def on_listYs_clicked(self, _):
        self._plotModel.yLabel = self._ui.listYs.selectionModel().selectedIndexes()[0].data(role=Qt.DisplayRole)
        self._updatePlot()

    def _updatePlot(self):
        if not (self._ui.listXs.selectionModel().hasSelection() and self._ui.listYs.selectionModel().hasSelection()):
            return
        self._plotWidget.plot()

    @pyqtSlot(int)
    def on_spinWindow_valueChanged(self, value):
        if value % 2 == 0:
            self._ui.spinWindow.setValue(value + 1)
        self._updateFilter()

    @pyqtSlot(int)
    def on_spinPoly_valueChanged(self, _):
        self._updateFilter()

    @pyqtSlot(int)
    def on_spinDeriv_valueChanged(self, _):
        self._updateFilter()

    @pyqtSlot(float)
    def on_spinDelta_valueChanged(self, _):
        self._updateFilter()

    def _updateFilter(self):
        window = self._ui.spinWindow.value()
        poly = self._ui.spinPoly.value()
        deriv = self._ui.spinDeriv.value()
        delta = self._ui.spinDelta.value()

        self._updateWidgetLimits(window, poly, deriv, delta)

        self._plotModel._updateFilter(params={
            'window': window,
            'poly': poly,
            'deriv': deriv,
            'delta': delta
        })
        self._updatePlot()

    def _updateWidgetLimits(self, window, poly, deriv, delta):
        x_len = len(self._plotModel.xs)
        self._ui.spinWindow.setMinimum(poly + 1 if is_even(poly) else poly + 2)
        self._ui.spinWindow.setMaximum(x_len - 1 if is_even(x_len) else x_len - 2)

        self._ui.spinPoly.setMaximum(window - 1)

    @pyqtSlot()
    def on_btnSaveExcel_clicked(self):
        self._plotModel.exportExcel()
