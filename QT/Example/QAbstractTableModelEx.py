from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QVBoxLayout,
    QWidget,
    QPushButton,
)

import sys
from typing import Any


class PersonModel(QAbstractTableModel):

    def __init__(self, data: list[list[str]]):
        super().__init__()
        self.people_data = data


    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.people_data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 2


    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None

        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:
            return self.people_data[row][column]

        return None


    def addPerson(self, person: list[str]) -> None:
        max_row = self.rowCount(None)
        self.beginInsertRows(QModelIndex(), max_row, max_row)
        self.people_data.append(person)
        self.endInsertRows()

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.buttonAdd=QPushButton("Add")
        central_widget=QWidget()
        self.setCentralWidget(central_widget)
        layout=QVBoxLayout(central_widget)

        self.list_view=QTableView()
        self.model=PersonModel([["John", "Doe"], ["Jane", "Smith"]])
        self.list_view.setModel(self.model)

        layout.addWidget(self.list_view)
        layout.addWidget(self.buttonAdd)

        self.buttonAdd.clicked.connect(self.onAdd)

    def onAdd(self):
        self.model.addPerson(["New", "Person"])

app = QApplication(sys.argv)
window = MainWindow()
window.resize(320, 240)
window.show()
app.exec()
