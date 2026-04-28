from __future__ import annotations

from PySide6.QtCore import QObject, Slot

from .domain import TaskFactory, TaskKey, TaskStatus
from .qt_adapter import QtTaskRunner
from .views import EventLogView, RuntimeStoreView, TaskViewPort


class TaskPresenter(QObject):
    def __init__(self, view: TaskViewPort, task_type: TaskKey, factory: TaskFactory, manager: "TaskManager"):
        super().__init__(view)
        self.view = view
        self.task_type = task_type
        self.factory = factory
        self.manager = manager
        self.runner: QtTaskRunner | None = None
        self._last_error_message: str | None = None

        self.view.connect_start(self.on_start)
        self.view.connect_cancel(self.on_cancel)
        self.view.set_title(self.factory.build_title())
        self.view.reset_to_pending()

    def reconfigure(self, task_type: TaskKey, factory: TaskFactory):
        if self.runner is not None:
            raise RuntimeError("Cannot reconfigure a presenter while its task is running")
        self.task_type = task_type
        self.factory = factory
        self._last_error_message = None
        self.view.set_title(factory.build_title())
        self.view.reset_to_pending()

    def cancel_active_task(self):
        if self.runner is None:
            return
        self.runner.cancel()
        self.manager.runtime_store.mark_cancelling(self.runner.task_id)

    @Slot()
    def on_start(self):
        if self.runner is not None:
            return

        task = self.factory.create_task()
        self.runner = QtTaskRunner(task)
        self._last_error_message = None

        self.runner.progress_signal.connect(self.on_runner_progress)
        self.runner.message_signal.connect(self.on_runner_message)
        self.runner.error_signal.connect(self.on_runner_error)
        self.runner.finished.connect(self.on_runner_finished)

        self.manager.runtime_store.register_task(
            task_id=self.runner.task_id,
            task_type=self.task_type,
            task_name=task.name,
            view_id=id(self.view),
        )
        self.manager.runtime_store.mark_running(self.runner.task_id)
        self.view.set_running(self.runner.task_id)
        self.manager.submit_runner(self.runner)

    @Slot()
    def on_cancel(self):
        if self.runner is None:
            return
        self.runner.cancel()
        self.manager.runtime_store.mark_cancelling(self.runner.task_id)
        self.view.set_cancelling()

    @Slot(int)
    def on_runner_progress(self, value: int):
        if self.runner is None:
            return
        self.manager.runtime_store.update_progress(self.runner.task_id, value)
        self.view.set_progress(value)

    @Slot(str)
    def on_runner_message(self, message: str):
        if self.runner is None:
            return
        self.manager.runtime_store.update_message(self.runner.task_id, message)
        self.view.set_message(message)

    @Slot(str)
    def on_runner_error(self, message: str):
        if self.runner is None:
            return
        self._last_error_message = message
        self.manager.runtime_store.set_error(self.runner.task_id, message)
        self.view.set_message(message)

    @Slot(str)
    def on_runner_finished(self, status_name: str):
        if self.runner is None:
            return

        try:
            status = TaskStatus[status_name]
        except KeyError:
            status = TaskStatus.FAILED

        final_messages = {
            TaskStatus.COMPLETED: "Task completed successfully",
            TaskStatus.CANCELLED: "Task cancelled by user",
        }
        final_message = self._last_error_message if status == TaskStatus.FAILED else final_messages.get(status)

        self.manager.runtime_store.mark_finished(self.runner.task_id, status, final_message)
        self.view.set_final_state(status, None if status == TaskStatus.FAILED else final_message)

        self.runner = None
        self._last_error_message = None


class RuntimeStorePresenter(QObject):
    def __init__(self, runtime_store, runtime_view: RuntimeStoreView, event_log_view: EventLogView | None = None):
        super().__init__(runtime_view)
        self.runtime_store = runtime_store
        self.runtime_view = runtime_view
        self.event_log_view = event_log_view

        self.runtime_store.entry_added.connect(self.on_entry_added_or_updated)
        self.runtime_store.entry_updated.connect(self.on_entry_added_or_updated)
        self.runtime_store.entry_removed.connect(self.on_entry_removed)

    @Slot(str)
    def on_entry_added_or_updated(self, task_id: str):
        entry = self.runtime_store.get(task_id)
        if entry is None:
            return
        self.runtime_view.upsert_entry(entry)
        if self.event_log_view is not None:
            self.event_log_view.append_message(
                f"[{entry.task_id}] {entry.task_type} | {entry.status.value} | {entry.last_message}"
            )

    @Slot(str)
    def on_entry_removed(self, task_id: str):
        self.runtime_view.remove_entry(task_id)
        if self.event_log_view is not None:
            self.event_log_view.append_message(f"[{task_id}] removed from runtime store")
