from __future__ import annotations

from PySide6.QtCore import QObject, QThreadPool
from shiboken6 import isValid

from .domain import (
    DownloadTaskFactory,
    FailingTaskFactory,
    GenerateReportTaskFactory,
    ProcessDataTaskFactory,
    TaskDefinition,
    TaskKey,
    TaskType,
)
from .presenter import TaskPresenter
from .registry import TaskRegistry
from .runtime_store import TaskRuntimeStore
from .views import TaskView


class TaskManager(QObject):
    def __init__(
        self,
        max_threads: int = 4,
        registry: TaskRegistry | None = None,
        runtime_store: TaskRuntimeStore | None = None,
    ):
        super().__init__()
        self.pool = QThreadPool.globalInstance()
        self.pool.setMaxThreadCount(max_threads)
        self.registry = registry or TaskRegistry()
        self.runtime_store = runtime_store or TaskRuntimeStore()
        if self.runtime_store.parent() is None:
            self.runtime_store.setParent(self)
        self._presenters_by_view_id: dict[int, TaskPresenter] = {}

        self._register_default_task_types()

    def register_task_type(self, task_type: TaskKey, definition: TaskDefinition):
        self.registry.register(task_type, definition)

    def create_task(self, task_type: TaskKey, *args, **kwargs) -> TaskView:
        factory = self.registry.create_factory(task_type, *args, **kwargs)
        definition = self.registry.get_definition(task_type)
        view = TaskView(
            factory.build_title(),
            start_text=definition.start_text,
            cancel_text=definition.cancel_text,
        )
        self.bind_task(view, task_type, *args, **kwargs)
        return view

    def bind_task(self, view: TaskView, task_type: TaskKey, *args, **kwargs) -> TaskPresenter:
        factory = self.registry.create_factory(task_type, *args, **kwargs)
        view_id = id(view)
        presenter = self._presenters_by_view_id.get(view_id)

        if presenter is None:
            presenter = TaskPresenter(view, task_type, factory, self)
            self._presenters_by_view_id[view_id] = presenter
            view.destroyed.connect(lambda _obj=None, dead_view_id=view_id: self._cleanup_view(dead_view_id))
            return presenter

        presenter.reconfigure(task_type, factory)
        return presenter

    def submit_runner(self, runner):
        self.pool.start(runner)

    def _cleanup_view(self, view_id: int):
        presenter = self._presenters_by_view_id.pop(view_id, None)
        if presenter is not None:
            presenter.cancel_active_task()
        if isValid(self.runtime_store):
            self.runtime_store.remove_tasks_for_view(view_id)

    def _register_default_task_types(self):
        defaults = {
            TaskType.DOWNLOAD: TaskDefinition(
                factory_cls=DownloadTaskFactory,
                start_text="Start Download",
                cancel_text="Cancel Download",
            ),
            TaskType.PROCESS_DATA: TaskDefinition(
                factory_cls=ProcessDataTaskFactory,
                start_text="Start Processing",
                cancel_text="Cancel Processing",
            ),
            TaskType.GENERATE_REPORT: TaskDefinition(
                factory_cls=GenerateReportTaskFactory,
                start_text="Start Report",
                cancel_text="Cancel Report",
            ),
            TaskType.FAILING_JOB: TaskDefinition(
                factory_cls=FailingTaskFactory,
                start_text="Run Fragile Job",
                cancel_text="Cancel Fragile Job",
            ),
        }
        for task_type, definition in defaults.items():
            self.register_task_type(task_type, definition)
