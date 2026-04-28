from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QVBoxLayout, QWidget
import sys

class TodoModel(QAbstractListModel):
    def __init__(self, todos=None):
        super().__init__()
        self._todos = todos if todos is not None else []

    def rowCount(self, parent=QModelIndex()):
        return len(self._todos)

    def data(self, index, role):
        if not index.isValid() or index.row() >= len(self._todos):
            return None

        item = self._todos[index.row()]
        if role == Qt.DisplayRole:
            return item["name"]
        elif role == Qt.CheckStateRole:
            return Qt.Checked if item["done"] else Qt.Unchecked
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or index.row() >= len(self._todos):
            return False

        if role == Qt.CheckStateRole:
            # Chuyển đổi value sang bool một cách rõ ràng
            new_state = value == Qt.Checked.value  # hoặc so sánh trực tiếp
            if self._todos[index.row()]["done"] == new_state:
                return False  # Không thay đổi, không cần emit

            self._todos[index.row()]["done"] = new_state
            # Phát tín hiệu cho cả CheckStateRole (và có thể cả DisplayRole nếu muốn)
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            return True

        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        # Bảo đảm đầy đủ cờ
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo List - Fixed Checkbox")

        todos = [
            {"name": "Mua sữa", "done": False},
            {"name": "Đi tập gym", "done": True},
            {"name": "Đọc sách", "done": False}
        ]

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.list_view = QListView()
        self.model = TodoModel(todos)
        self.list_view.setModel(self.model)

        layout.addWidget(self.list_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())