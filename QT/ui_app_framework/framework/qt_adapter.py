from __future__ import annotations

import uuid

from PySide6.QtCore import QObject, QMutex, QMutexLocker, QRunnable, Signal
from shiboken6 import isValid

from .domain import DomainTask, ProgressReporter, TaskStatus


def _safe_emit(signal_instance, *args):
    try:
        signal_instance.emit(*args)
    except RuntimeError:
        pass


class TaskSignals(QObject):
    progress = Signal(int)
    message = Signal(str)
    error = Signal(str)
    finished = Signal(str)


class QtProgressReporter(ProgressReporter):
    def __init__(self, signals: TaskSignals):
        self._signals = signals
        self._cancelled = False
        self._mutex = QMutex()

    def report_progress(self, percent: int):
        if isValid(self._signals):
            _safe_emit(self._signals.progress, percent)

    def report_message(self, message: str):
        if isValid(self._signals):
            _safe_emit(self._signals.message, message)

    def is_cancelled(self) -> bool:
        with QMutexLocker(self._mutex):
            return self._cancelled

    def cancel(self):
        with QMutexLocker(self._mutex):
            self._cancelled = True


class QtTaskRunner(QRunnable):
    def __init__(self, domain_task: DomainTask):
        super().__init__()
        self._signals = TaskSignals()
        self.domain_task = domain_task
        self.reporter = QtProgressReporter(self._signals)
        self._task_id = str(uuid.uuid4())[:8]
        self.status = TaskStatus.PENDING

    @property
    def task_id(self):
        return self._task_id

    @property
    def finished(self):
        return self._signals.finished

    @property
    def progress_signal(self):
        return self._signals.progress

    @property
    def message_signal(self):
        return self._signals.message

    @property
    def error_signal(self):
        return self._signals.error

    def run(self):
        self.status = TaskStatus.RUNNING
        try:
            self.domain_task.execute(self.reporter)
        except Exception as error:
            self.status = TaskStatus.FAILED
            if isValid(self._signals):
                _safe_emit(self._signals.error, str(error))
        else:
            self.status = TaskStatus.CANCELLED if self.reporter.is_cancelled() else TaskStatus.COMPLETED
        finally:
            if isValid(self._signals):
                _safe_emit(self._signals.finished, self.status.name)

    def cancel(self):
        self.reporter.cancel()
