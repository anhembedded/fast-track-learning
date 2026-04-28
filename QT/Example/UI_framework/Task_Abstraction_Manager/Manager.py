from enum import Enum
from PySide6.QtCore import QObject, QRunnable, Signal, Slot, QThreadPool, QMutex, QMutexLocker
from PySide6.QtWidgets import QApplication, QProgressBar, QPushButton, QVBoxLayout, QWidget
import uuid
import time

class utils:
    @staticmethod
    def get_uuid():
        return str(uuid.uuid4())[:8]

class TaskStatus(Enum):
    PENDING = 0
    RUNNING = 1
    COMPLETED = 2
    CANCELLED = 3
    FAILED = 4

class TaskSignals(QObject):
    progress = Signal(int)
    message = Signal(str)
    finished = Signal()
    error = Signal(str)

class BaseTask(QRunnable):
    def __init__(self):
        super().__init__()
        self.id = utils.get_uuid()
        self.status = TaskStatus.PENDING
        self.signals = TaskSignals()
        self._is_cancelled = False
        self._mutex = QMutex()

    def get_task_id(self):
        return self.id

    def cancel(self):
        with QMutexLocker(self._mutex):
            self._is_cancelled = True

    def is_cancelled(self):
        with QMutexLocker(self._mutex):
            return self._is_cancelled

    def run(self):
        self.status = TaskStatus.RUNNING
        try:
            self._execute()
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.signals.error.emit(str(e))
        else:
            self.status = TaskStatus.COMPLETED
        finally:
            self.signals.finished.emit()

    def _execute(self):
        raise NotImplementedError

class DownloadTask(BaseTask):
    def __init__(self, url, dest):
        super().__init__()
        self.url = url
        self.dest = dest

    def _execute(self):
        # giả lập tải file
        for i in range(1, 101):
            if self.is_cancelled():
                self.signals.message.emit("Download cancelled")
                return  # dừng sớm, run() sẽ vẫn emit finished
            time.sleep(0.05)
            self.signals.progress.emit(i)
            self.signals.message.emit(f"Downloading {self.url} to {self.dest}... {i}%")

class TaskManager(QObject):
    task_added = Signal(BaseTask)
    task_removed = Signal(str)  # truyền task_id

    def __init__(self, max_concurrent=4):
        super().__init__()
        self.pool = QThreadPool.globalInstance()
        self.pool.setMaxThreadCount(max_concurrent)
        self._tasks : dict[str, BaseTask] = {}  # task_id -> BaseTask

    def submit(self, task: BaseTask):
        self._tasks[task.id] = task
        # Dọn dẹp khi task kết thúc
        task.signals.finished.connect(lambda tid=task.id: self._on_finished(tid))
        self.task_added.emit(task)
        self.pool.start(task)

    def cancel(self, task_id: str):
        task = self._tasks.get(task_id)
        if task:
            task.cancel()

    def _on_finished(self, task_id):
        if task_id in self._tasks:
            del self._tasks[task_id]
            self.task_removed.emit(task_id)

class MainWindow(QObject):
    def __init__(self):
        super().__init__()
        self.manager = TaskManager()
        self.manager.task_added.connect(self.on_task_added)
        self.manager.task_removed.connect(self.on_task_removed)

        self.buttonDownload_1 = QPushButton("Download File 1")
        self.buttonDownload_2 = QPushButton("Download File 2")

        self.progessDownloadBar_1 = QProgressBar()
        self.progessDownloadBar_2 = QProgressBar()

        self.buttonDownload_1.clicked.connect(self.buttonDownload_1_clicked)
        self.buttonDownload_2.clicked.connect(self.buttonDownload_2_clicked)

        container = QVBoxLayout()
        container.addWidget(self.buttonDownload_1)
        container.addWidget(self.progessDownloadBar_1)
        container.addWidget(self.buttonDownload_2)
        container.addWidget(self.progessDownloadBar_2)
        self.window = QWidget()
        self.window.setLayout(container)

    def buttonDownload_1_clicked(self):
        task = DownloadTask("http://example.com/file1.zip", "/path/to/file1.zip")
        task.signals.progress.connect(self.progessDownloadBar_1.setValue)
        self.manager.submit(task)

    def buttonDownload_2_clicked(self):
        task = DownloadTask("http://example.com/file2.zip", "/path/to/file2.zip")
        task.signals.progress.connect(self.progessDownloadBar_2.setValue)
        self.manager.submit(task)

    @Slot(BaseTask)
    def on_task_added(self, task : BaseTask):
        print(f"Task added: {task.get_task_id()}")

    @Slot(str)
    def on_task_removed(self, task_id : str):
        print(f"Task removed: {task_id}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.window.show()
    app.exec()