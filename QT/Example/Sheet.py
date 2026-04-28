from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem , QTableView
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from datetime import datetime
from PySide6 import QtGui
import sys


class SheetModel(QAbstractTableModel):
    def __init__(self, data : list[list[None | str]]):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0]) if self._data != [] else 0

    def data(self, index : QModelIndex, role : int):
        if role == Qt.DisplayRole:
            # Get the raw value
            value = self._data[index.row()][index.column()]

            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%Y-%m-%d")

            if isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value

            if isinstance(value, str):
                # Render strings with quotes
                return '"%s"' % value
            # Default (anything not captured above: e.g. int)
            return str(value)

        elif role == Qt.EditRole:
            return self._data[index.row()][index.column()]
        elif role == Qt.BackgroundRole and index.column() == 2:
            return QtGui.QColor('blue')
        elif role == Qt.TextAlignmentRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, int) or isinstance(value, float):
                # Align right, vertical middle.
                return Qt.AlignVCenter + Qt.AlignRight
        elif role == Qt.ForegroundRole:
            value = self._data[index.row()][index.column()]

            if (
                (isinstance(value, int) or isinstance(value, float))
                and value < 0
            ):
                return QtGui.QColor('red')
        elif role == Qt.DecorationRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, datetime):
                return QtGui.QIcon('C:\\Users\\hoang\\Desktop\\fast-track-learning\\QT\\Example\\icons\\calendar.png')


    def setData(self, index : QModelIndex, value, role : int):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [Qt.DisplayRole])
            return True
        return False

    def flags(self, index : QModelIndex):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

class SheetView(QTableView):
    def __init__(self, data : list[list[None | str]]):
        super().__init__()
        self.setModel(SheetModel(data))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sheet Example")

        # Create a QTableWidget
        self.sheet_widget =  SheetView([
            ["Alice", -30, datetime(2017,10,1)],
            ["Bob", 25, datetime(2018,5,15)],
            ["Charlie", 35, datetime(2019,12,10)],
            ["David", 28, datetime(2020,8,20)],
            ["Eve", 22, datetime(2021,3,25)]
        ])

        self.setCentralWidget(self.sheet_widget)

        # Set headers for the columns
        self.sheet_widget.model().setHeaderData(0, Qt.Horizontal, "Name")
        self.sheet_widget.model().setHeaderData(1, Qt.Horizontal, "Age")
        self.sheet_widget.model().setHeaderData(2, Qt.Horizontal, "Date of Birth")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())