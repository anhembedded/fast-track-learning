from PySide6.QtCore import QThread, QObject, Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QVBoxLayout, QWidget, QTextEdit

# Worker kế thừa QObject để có Signal
class Worker(QObject):
    progress = Signal(int)        # báo %
    message = Signal(str)         # báo text
    finished = Signal()           # hoàn thành

    def __init__(self, data):
        super().__init__()
        self.data = data

    @Slot()
    def do_work(self):
        """Hàm chạy trong luồng nền."""
        for i in range(1, 101):
            # Gửi progress
            self.progress.emit(i)
            self.message.emit(f"Processing {i}%")
            QThread.msleep(50)   # giả lập công việc
        self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None

        self.progress_bar = QProgressBar()
        self.log = QTextEdit()
        self.btn = QPushButton("Start")
        self.btn.clicked.connect(self.start_task)

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log)
        layout.addWidget(self.btn)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_task(self):
        # Tạo QThread và Worker
        self.thread = QThread()
        self.worker = Worker("some data")
        self.worker.moveToThread(self.thread)

        # Kết nối signals
        self.thread.started.connect(self.worker.do_work)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.message.connect(self.log.append)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # Start
        self.thread.start()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()