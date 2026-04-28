from __future__ import annotations

import time
from dataclasses import asdict, dataclass, replace

from PySide6.QtCore import QObject, Signal

from .domain import TaskKey, TaskStatus, task_key_to_string


@dataclass(frozen=True)
class TaskRuntimeEntry:
    task_id: str
    task_type: str
    task_name: str
    view_id: int
    status: TaskStatus = TaskStatus.PENDING
    progress: int = 0
    last_message: str = "Ready"
    error_message: str | None = None
    cancellation_requested: bool = False
    created_at: float = 0.0
    started_at: float | None = None
    finished_at: float | None = None


class TaskRuntimeStore(QObject):
    entry_added = Signal(str)
    entry_updated = Signal(str)
    entry_removed = Signal(str)

    def __init__(self):
        super().__init__()
        self._entries: dict[str, TaskRuntimeEntry] = {}

    def register_task(self, task_id: str, task_type: TaskKey, task_name: str, view_id: int):
        self._entries[task_id] = TaskRuntimeEntry(
            task_id=task_id,
            task_type=task_key_to_string(task_type),
            task_name=task_name,
            view_id=view_id,
            created_at=time.time(),
        )
        self.entry_added.emit(task_id)

    def mark_running(self, task_id: str):
        self._update(
            task_id,
            status=TaskStatus.RUNNING,
            started_at=time.time(),
            cancellation_requested=False,
        )

    def update_progress(self, task_id: str, progress: int):
        self._update(task_id, progress=progress)

    def update_message(self, task_id: str, message: str):
        self._update(task_id, last_message=message)

    def mark_cancelling(self, task_id: str):
        self._update(task_id, cancellation_requested=True, last_message="Cancellation requested...")

    def set_error(self, task_id: str, message: str):
        self._update(task_id, error_message=message, last_message=message)

    def mark_finished(self, task_id: str, status: TaskStatus, final_message: str | None = None):
        updates = {
            "status": status,
            "finished_at": time.time(),
            "cancellation_requested": False,
        }
        if final_message is not None:
            updates["last_message"] = final_message
        self._update(task_id, **updates)

    def get(self, task_id: str) -> TaskRuntimeEntry | None:
        return self._entries.get(task_id)

    def list_entries(self) -> list[TaskRuntimeEntry]:
        return list(self._entries.values())

    def summary_by_status(self) -> dict[TaskStatus, int]:
        summary = {status: 0 for status in TaskStatus}
        for entry in self._entries.values():
            summary[entry.status] += 1
        return summary

    def summary_by_type(self) -> dict[str, int]:
        summary: dict[str, int] = {}
        for entry in self._entries.values():
            summary[entry.task_type] = summary.get(entry.task_type, 0) + 1
        return summary

    def export_snapshot(self) -> dict:
        entries = []
        for entry in self.list_entries():
            raw = asdict(entry)
            raw["status"] = entry.status.value
            entries.append(raw)
        return {
            "generated_at": time.time(),
            "entries": entries,
            "summary": {
                "by_status": {status.value: count for status, count in self.summary_by_status().items()},
                "by_type": self.summary_by_type(),
            },
        }

    def remove_task(self, task_id: str):
        if task_id in self._entries:
            del self._entries[task_id]
            self.entry_removed.emit(task_id)

    def remove_tasks_for_view(self, view_id: int):
        removable_ids = [task_id for task_id, entry in self._entries.items() if entry.view_id == view_id]
        for task_id in removable_ids:
            self.remove_task(task_id)

    def _update(self, task_id: str, **changes):
        entry = self._entries.get(task_id)
        if entry is None:
            return
        self._entries[task_id] = replace(entry, **changes)
        self.entry_updated.emit(task_id)
