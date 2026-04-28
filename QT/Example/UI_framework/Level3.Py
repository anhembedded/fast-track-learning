from PySide6.QtCore import QRunnable, QObject, Signal, QMutex, QMutexLocker
import uuid
from enum import Enum

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
        self.id = str(uuid.uuid4())[:8]
        self.status = TaskStatus.PENDING
        self.signals = TaskSignals()
        self._is_cancelled = False
        self._mutex = QMutex()

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

class ExampleTask(BaseTask):
    def __init__(self, total_steps=100):
        super().__init__()
        self.total_steps = total_steps

    def _execute(self):
        for i in range(self.total_steps):
            if self.is_cancelled():
                self.signals.message.emit("Task cancelled")
                return
            # giả lập công việc
            import time
            time.sleep(0.05)
            percent = int((i+1)/self.total_steps*100)
            self.signals.progress.emit(percent)
            self.signals.message.emit(f"Step {i+1}/{self.total_steps}")

class TaskManager(QObject):
    """Quản lý các task với thread pool."""
    task_added = Signal(BaseTask)
    task_removed = Signal(str)

    def __init__(self, max_concurrent=4):
        super().__init__()
        self.pool = QThreadPool.globalInstance()
        self.pool.setMaxThreadCount(max_concurrent)
        self.tasks = {}   # id -> BaseTask

    def submit(self, task: BaseTask):
        self.tasks[task.id] = task
        task.signals.finished.connect(lambda: self._on_task_finished(task.id))
        self.task_added.emit(task)
        self.pool.start(task)

    def cancel(self, task_id: str):
        task = self.tasks.get(task_id)
        if task:
            task.cancel()

    def _on_task_finished(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.task_removed.emit(task_id)

