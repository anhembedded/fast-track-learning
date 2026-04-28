import sys
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListView, QLabel
)

# -----------------------------
# Model/View side
# -----------------------------
class NameModel(QAbstractListModel):
    def __init__(self, names):
        super().__init__()
        self.names = names

    def rowCount(self, parent):
        print("[Model] rowCount called")
        return len(self.names)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            print(f"[Model] data called for row {row}")
            return self.names[row]

    def add_item(self, name):
        row = self.rowCount(None)

        print(f"[Model] begin insert at row {row}")

        self.beginInsertRows(
            QModelIndex(),
            row,
            row
        )

        self.names.append(name)

        self.endInsertRows()

        print("[Model] end insert")


# -----------------------------
# Main Window
# -----------------------------
class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.counter = 1

        self.setWindowTitle("Built-in Widget vs Model/View")

        root = QVBoxLayout(self)

        compare_layout = QHBoxLayout()

        # -----------------
        # LEFT: QListWidget
        # -----------------
        left_layout = QVBoxLayout()

        left_layout.addWidget(
            QLabel("Built-in Data Widget\n(QListWidget)")
        )

        self.list_widget = QListWidget()

        self.list_widget.addItem("Apple")
        self.list_widget.addItem("Banana")
        self.list_widget.addItem("Orange")

        left_layout.addWidget(
            self.list_widget
        )

        compare_layout.addLayout(
            left_layout
        )


        # -----------------
        # RIGHT: QListView + Model
        # -----------------
        right_layout = QVBoxLayout()

        right_layout.addWidget(
            QLabel("Model/View\n(QListView + QAbstractListModel)")
        )

        self.model = NameModel(
            [
                "Apple",
                "Banana",
                "Orange"
            ]
        )

        self.list_view = QListView()

        self.list_view.setModel(
            self.model
        )

        right_layout.addWidget(
            self.list_view
        )

        # Add button for left side
        left_button = QPushButton("Add Item")
        left_button.clicked.connect(self.add_to_list_widget)
        left_layout.addWidget(left_button)

        # Add button for right side
        right_button = QPushButton("Add Item")
        right_button.clicked.connect(self.add_to_model)
        right_layout.addWidget(right_button)

        compare_layout.addLayout(
            right_layout
        )

        root.addLayout(
            compare_layout
        )

    def add_to_list_widget(self):
        self.counter += 1
        self.list_widget.addItem(f"Item {self.counter}")

    def add_to_model(self):
        self.counter += 1
        self.model.add_item(f"Item {self.counter}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec())