from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtWidgets import (
    QApplication,
    QListView,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
)
import sys



class ListViewModel(QAbstractListModel):
    def __init__(self, names):
        super().__init__()
        self.names = names

    def rowCount(self, parent):
        return len(self.names)

    def data(self, index: QModelIndex, role):
        if role == Qt.DisplayRole:
            return self.names[index.row()]

    def addList(self, name : str):
        max_row = self.rowCount(None)
        self.beginInsertRows(QModelIndex(), max_row, max_row)
        self.names.append(name)
        self.endInsertRows()

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.buttonAdd=QPushButton("Add")
        central_widget=QWidget()
        self.setCentralWidget(central_widget)
        layout=QVBoxLayout(central_widget)

        self.list_view=QListView()
        self.model=ListViewModel(["Apple","Banana","Orange"])
        self.list_view.setModel(self.model)

        layout.addWidget(self.list_view)
        layout.addWidget(self.buttonAdd)

        self.buttonAdd.clicked.connect(self.onAdd)

    def onAdd(self):
        self.model.addList("New Task")



app = QApplication(sys.argv)

window = MainWindow()
window.resize(320, 240)
window.show()

sys.exit(app.exec())
