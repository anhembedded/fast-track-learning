from __future__ import annotations

from typing import Protocol

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .domain import TaskStatus


class TaskViewPort(Protocol):
    def connect_start(self, handler): ...
    def connect_cancel(self, handler): ...
    def set_title(self, title: str): ...
    def reset_to_pending(self, message: str = "Ready"): ...
    def set_progress(self, value: int): ...
    def set_running(self, task_id: str): ...
    def set_final_state(self, status: TaskStatus, message: str | None = None): ...
    def set_message(self, text: str): ...
    def set_cancelling(self): ...


class TaskView(QFrame):
    def __init__(self, title, start_text="Start", cancel_text="Cancel"):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.title_label = QLabel(title)
        self.status_label = QLabel(TaskStatus.PENDING.value)
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

    def connect_start(self, handler):
        self.start_button.clicked.connect(handler)

    def connect_cancel(self, handler):
        self.cancel_button.clicked.connect(handler)

    def set_title(self, title: str):
        self.title_label.setText(title)

    def reset_to_pending(self, message: str = "Ready"):
        self.status_label.setText(TaskStatus.PENDING.value)
        self.progress_bar.setValue(0)
        self.message_label.setText(message)
        self.task_id_label.setText("Task: -")
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

    def set_progress(self, value: int):
        self.progress_bar.setValue(value)

    def set_running(self, task_id: str):
        self.progress_bar.setValue(0)
        self.status_label.setText(TaskStatus.RUNNING.value)
        self.message_label.setText("Task started")
        self.task_id_label.setText(f"Task: {task_id}")
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

    def set_final_state(self, status: TaskStatus, message: str | None = None):
        self.status_label.setText(status.value)
        if message:
            self.message_label.setText(message)
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

    def set_message(self, text: str):
        self.message_label.setText(text)

    def set_cancelling(self):
        self.status_label.setText("Cancelling")
        self.message_label.setText("Cancellation requested...")
        self.cancel_button.setEnabled(False)


class RuntimeStoreView(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Task ID", "Type", "Status", "Progress", "Message", "Error"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Runtime Store"))
        layout.addWidget(self.table)

    def upsert_entry(self, entry):
        row = self._find_row(entry.task_id)
        if row is None:
            row = self.table.rowCount()
            self.table.insertRow(row)

        values = [
            entry.task_id,
            entry.task_type,
            entry.status.value,
            str(entry.progress),
            entry.last_message,
            entry.error_message or "",
        ]
        for column, value in enumerate(values):
            self.table.setItem(row, column, QTableWidgetItem(value))

    def remove_entry(self, task_id: str):
        row = self._find_row(task_id)
        if row is not None:
            self.table.removeRow(row)

    def _find_row(self, task_id: str):
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.text() == task_id:
                return row
        return None


class EventLogView(QWidget):
    def __init__(self):
        super().__init__()
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)

        self.clear_button = QPushButton("Clear Log")
        self.clear_button.clicked.connect(self.log.clear)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Framework Event Log"))
        layout.addWidget(self.log)
        layout.addWidget(self.clear_button)

    def append_message(self, message: str):
        self.log.appendPlainText(message)
