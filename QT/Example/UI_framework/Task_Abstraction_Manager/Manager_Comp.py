from enum import Enum
import time
import uuid

from PySide6.QtCore import QObject, QRunnable, QMutex, QMutexLocker, QThreadPool, Signal, Slot
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


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
        except Exception as error:
            self.status = TaskStatus.FAILED
            self.signals.error.emit(str(error))
        else:
            self.status = TaskStatus.CANCELLED if self.is_cancelled() else TaskStatus.COMPLETED
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
        for i in range(1, 101):
            if self.is_cancelled():
                self.signals.message.emit("Download cancelled")
                return
            time.sleep(0.05)
            self.signals.progress.emit(i)
            self.signals.message.emit(f"Downloading {self.url} to {self.dest}... {i}%")


class TaskManager(QObject):
    task_added = Signal(BaseTask)
    task_removed = Signal(str)
    task_finished = Signal(BaseTask)

    def __init__(self, max_concurrent=4):
        super().__init__()
        self.pool = QThreadPool.globalInstance()
        self.pool.setMaxThreadCount(max_concurrent)
        self._tasks: dict[str, BaseTask] = {}

    def submit(self, task: BaseTask):
        self._tasks[task.id] = task
        task.signals.finished.connect(lambda tid=task.id: self._on_finished(tid))
        self.task_added.emit(task)
        self.pool.start(task)

    def cancel(self, task_id: str):
        task = self._tasks.get(task_id)
        if task:
            task.cancel()

    def _on_finished(self, task_id):
        task = self._tasks.pop(task_id, None)
        if task is None:
            return
        self.task_finished.emit(task)
        self.task_removed.emit(task_id)


class TaskCard(QFrame):
    def __init__(self, title, start_text, cancel_text):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.title_label = QLabel(title)
        self.status_label = QLabel("Idle")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.message_label = QLabel("Ready")
        self.message_label.setWordWrap(True)
        self.task_id_label = QLabel("Task: -")
        self.start_button = QPushButton(start_text)
        self.cancel_button = QPushButton(cancel_text)
        self.cancel_button.setEnabled(False)

        header = QHBoxLayout()
        header.addWidget(self.title_label)
        header.addStretch()
        header.addWidget(self.status_label)

        actions = QHBoxLayout()
        actions.addWidget(self.start_button)
        actions.addWidget(self.cancel_button)

        layout = QVBoxLayout(self)
        layout.addLayout(header)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.message_label)
        layout.addWidget(self.task_id_label)
        layout.addLayout(actions)

    def prepare_running(self, task_id):
        self.progress_bar.setValue(0)
        self.status_label.setText("Running")
        self.message_label.setText("Task started")
        self.task_id_label.setText(f"Task: {task_id}")
        self.cancel_button.setEnabled(True)

    def set_status(self, text):
        self.status_label.setText(text)

    def set_message(self, text):
        self.message_label.setText(text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Abstraction Manager")
        self.resize(840, 520)

        self.manager = TaskManager()
        self.manager.task_added.connect(self.on_task_added)
        self.manager.task_removed.connect(self.on_task_removed)
        self.manager.task_finished.connect(self.on_task_finished)

        self._active_task_ids: dict[str, str] = {}
        self._task_cards: dict[str, TaskCard] = {}

        self.info_label = QLabel(
            "Two independent download slots managed by TaskManager. "
            "Each slot tracks progress, messages, cancellation, and final status."
        )
        self.info_label.setWordWrap(True)

        self.download_card_1 = TaskCard("Download Slot 1", "Download File 1", "Cancel Task 1")
        self.download_card_2 = TaskCard("Download Slot 2", "Download File 2", "Cancel Task 2")
        self._task_cards["download_1"] = self.download_card_1
        self._task_cards["download_2"] = self.download_card_2

        self.download_card_1.start_button.clicked.connect(self.buttonDownload_1_clicked)
        self.download_card_2.start_button.clicked.connect(self.buttonDownload_2_clicked)
        self.download_card_1.cancel_button.clicked.connect(lambda: self.cancel_task("download_1"))
        self.download_card_2.cancel_button.clicked.connect(lambda: self.cancel_task("download_2"))

        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setPlaceholderText("Task logs will appear here...")

        self.clear_log_button = QPushButton("Clear Log")
        self.clear_log_button.clicked.connect(self.log_view.clear)

        cards_layout = QGridLayout()
        cards_layout.addWidget(self.download_card_1, 0, 0)
        cards_layout.addWidget(self.download_card_2, 0, 1)

        log_header = QHBoxLayout()
        log_header.addWidget(QLabel("Task Event Log"))
        log_header.addStretch()
        log_header.addWidget(self.clear_log_button)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.info_label)
        layout.addLayout(cards_layout)
        layout.addLayout(log_header)
        layout.addWidget(self.log_view)
        self.setCentralWidget(container)

    def buttonDownload_1_clicked(self):
        self.start_download_task("download_1", "http://example.com/file1.zip", "/path/to/file1.zip")

    def buttonDownload_2_clicked(self):
        self.start_download_task("download_2", "http://example.com/file2.zip", "/path/to/file2.zip")

    def start_download_task(self, slot_name, url, dest):
        current_task_id = self._active_task_ids.get(slot_name)
        if current_task_id:
            self.append_log(f"[{slot_name}] Task {current_task_id} is still running")
            return

        task = DownloadTask(url, dest)
        card = self._task_cards[slot_name]
        self._active_task_ids[slot_name] = task.id
        card.prepare_running(task.id)
        self.bind_task_to_card(slot_name, task)
        self.manager.submit(task)

    def bind_task_to_card(self, slot_name, task):
        card = self._task_cards[slot_name]
        task.signals.progress.connect(card.progress_bar.setValue)
        task.signals.message.connect(card.set_message)
        task.signals.message.connect(lambda text, slot=slot_name: self.append_log(f"[{slot}] {text}"))
        task.signals.error.connect(lambda text, slot=slot_name: self.handle_task_error(slot, text))

    def cancel_task(self, slot_name):
        task_id = self._active_task_ids.get(slot_name)
        if not task_id:
            self.append_log(f"[{slot_name}] No running task to cancel")
            return

        card = self._task_cards[slot_name]
        card.set_status("Cancelling")
        card.set_message("Cancellation requested")
        self.manager.cancel(task_id)

    def append_log(self, message):
        self.log_view.appendPlainText(message)

    def update_card_from_status(self, slot_name, status):
        card = self._task_cards[slot_name]
        labels = {
            TaskStatus.PENDING: "Pending",
            TaskStatus.RUNNING: "Running",
            TaskStatus.COMPLETED: "Completed",
            TaskStatus.CANCELLED: "Cancelled",
            TaskStatus.FAILED: "Failed",
        }
        card.set_status(labels[status])
        if status != TaskStatus.RUNNING:
            card.cancel_button.setEnabled(False)

    def find_slot_name_by_task_id(self, task_id):
        for slot_name, current_task_id in self._active_task_ids.items():
            if current_task_id == task_id:
                return slot_name
        return None

    def handle_task_error(self, slot_name, error_message):
        card = self._task_cards[slot_name]
        card.set_message(error_message)
        self.update_card_from_status(slot_name, TaskStatus.FAILED)
        self.append_log(f"[{slot_name}] Error: {error_message}")

    @Slot(BaseTask)
    def on_task_added(self, task: BaseTask):
        self.append_log(f"Task added: {task.get_task_id()}")

    @Slot(str)
    def on_task_removed(self, task_id: str):
        self.append_log(f"Task removed: {task_id}")

    @Slot(BaseTask)
    def on_task_finished(self, task: BaseTask):
        slot_name = self.find_slot_name_by_task_id(task.id)
        if slot_name is None:
            self.append_log(f"Task finished but no slot mapping found: {task.id}")
            return

        card = self._task_cards[slot_name]
        self.update_card_from_status(slot_name, task.status)

        if task.status == TaskStatus.COMPLETED:
            card.set_message("Download completed successfully")
        elif task.status == TaskStatus.CANCELLED:
            card.set_message("Download cancelled by user")
        elif task.status == TaskStatus.FAILED:
            card.set_message("Download failed")

        self._active_task_ids.pop(slot_name, None)
        self.append_log(f"[{slot_name}] Finished with status: {task.status.name}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
