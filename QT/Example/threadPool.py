from PySide6.QtCore import QRunnable, QThreadPool, QTimer, Slot
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
import time


class Domain():
    def __init__(self, name):
        self.name = name

    def task_1(self):
        print(f"Task 1 for {self.name}")

    def task_2(self):
        print(f"Task 2 for {self.name}")


class Worker(QRunnable):
    """Worker thread."""
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs  # ✅ Fixed: was 'kwarg' (typo)

    @Slot()
    def run(self):
        self.function(*self.args, **self.kwargs)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Thread Pool Example")

        self.threadpool = QThreadPool()
        self.domain = Domain("Example Domain")

        layout = QVBoxLayout()

        self.label = QLabel("Press the button to start tasks")
        layout.addWidget(self.label)

        self.button_1 = QPushButton("Start Task 1")
        self.button_2 = QPushButton("Start Task 2")

        self.button_1.clicked.connect(self.start_tasks_1)
        self.button_2.clicked.connect(self.start_tasks_2)

        layout.addWidget(self.button_1)
        layout.addWidget(self.button_2)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_tasks_1(self):
        worker = Worker(self.domain.task_1)
        self.threadpool.start(worker)

    def start_tasks_2(self):
        worker = Worker(self.domain.task_2)
        self.threadpool.start(worker)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()