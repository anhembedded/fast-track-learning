from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias


class ProgressReporter(ABC):
    @abstractmethod
    def report_progress(self, percent: int):
        ...

    @abstractmethod
    def report_message(self, message: str):
        ...

    @abstractmethod
    def is_cancelled(self) -> bool:
        ...


class DomainTask(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, reporter: ProgressReporter):
        ...


class DownloadTask(DomainTask):
    def __init__(self, url: str, save_path: str = ""):
        super().__init__(name=f"Download {url}")
        self.url = url
        self.save_path = save_path

    def execute(self, reporter: ProgressReporter):
        for i in range(1, 101):
            if reporter.is_cancelled():
                reporter.report_message(f"{self.name} cancelled")
                return
            time.sleep(0.02)
            reporter.report_progress(i)
            reporter.report_message(f"{self.name}: {i}%")
        reporter.report_message(f"{self.name} completed")


class ProcessDataTask(DomainTask):
    def __init__(self, dataset_name: str, batch_count: int = 8):
        super().__init__(name=f"Process {dataset_name}")
        self.dataset_name = dataset_name
        self.batch_count = max(1, batch_count)

    def execute(self, reporter: ProgressReporter):
        reporter.report_message(f"Loading dataset {self.dataset_name}")
        total_steps = self.batch_count * 10
        for step in range(1, total_steps + 1):
            if reporter.is_cancelled():
                reporter.report_message(f"{self.name} cancelled")
                return
            time.sleep(0.03)
            percent = int(step * 100 / total_steps)
            batch_number = ((step - 1) // 10) + 1
            reporter.report_progress(percent)
            reporter.report_message(f"{self.name}: batch {batch_number}/{self.batch_count}")
        reporter.report_message(f"{self.name} completed")


class GenerateReportTask(DomainTask):
    def __init__(self, report_name: str, section_count: int = 6):
        super().__init__(name=f"Generate report {report_name}")
        self.report_name = report_name
        self.section_count = max(1, section_count)

    def execute(self, reporter: ProgressReporter):
        for section in range(1, self.section_count + 1):
            if reporter.is_cancelled():
                reporter.report_message(f"{self.name} cancelled")
                return
            reporter.report_message(f"{self.name}: composing section {section}/{self.section_count}")
            for chunk in range(1, 6):
                if reporter.is_cancelled():
                    reporter.report_message(f"{self.name} cancelled")
                    return
                time.sleep(0.04)
                completed_units = ((section - 1) * 5) + chunk
                total_units = self.section_count * 5
                reporter.report_progress(int(completed_units * 100 / total_units))
        reporter.report_message(f"{self.name} completed")


class FailingTask(DomainTask):
    def __init__(self, job_name: str, fail_at_percent: int = 55):
        super().__init__(name=f"Fragile job {job_name}")
        self.job_name = job_name
        self.fail_at_percent = fail_at_percent

    def execute(self, reporter: ProgressReporter):
        for i in range(1, 101):
            if reporter.is_cancelled():
                reporter.report_message(f"{self.name} cancelled")
                return
            time.sleep(0.02)
            reporter.report_progress(i)
            reporter.report_message(f"{self.name}: validating step {i}%")
            if i >= self.fail_at_percent:
                raise RuntimeError(f"{self.name} failed during validation at {i}%")


class TaskType(Enum):
    DOWNLOAD = "download"
    PROCESS_DATA = "process_data"
    GENERATE_REPORT = "generate_report"
    FAILING_JOB = "failing_job"


class TaskStatus(Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    FAILED = "Failed"


TaskKey: TypeAlias = str | TaskType


def task_key_to_string(task_key: TaskKey) -> str:
    if isinstance(task_key, TaskType):
        return task_key.value
    return str(task_key)


class TaskFactory(ABC):
    @abstractmethod
    def create_task(self) -> DomainTask:
        ...

    @abstractmethod
    def build_title(self) -> str:
        ...


class DownloadTaskFactory(TaskFactory):
    def __init__(self, url: str, save_path: str = ""):
        self.url = url
        self.save_path = save_path

    def create_task(self) -> DomainTask:
        return DownloadTask(self.url, self.save_path)

    def build_title(self) -> str:
        return f"Download Task: {self.url}"


class ProcessDataTaskFactory(TaskFactory):
    def __init__(self, dataset_name: str, batch_count: int = 8):
        self.dataset_name = dataset_name
        self.batch_count = batch_count

    def create_task(self) -> DomainTask:
        return ProcessDataTask(self.dataset_name, self.batch_count)

    def build_title(self) -> str:
        return f"Process Task: {self.dataset_name}"


class GenerateReportTaskFactory(TaskFactory):
    def __init__(self, report_name: str, section_count: int = 6):
        self.report_name = report_name
        self.section_count = section_count

    def create_task(self) -> DomainTask:
        return GenerateReportTask(self.report_name, self.section_count)

    def build_title(self) -> str:
        return f"Report Task: {self.report_name}"


class FailingTaskFactory(TaskFactory):
    def __init__(self, job_name: str, fail_at_percent: int = 55):
        self.job_name = job_name
        self.fail_at_percent = fail_at_percent

    def create_task(self) -> DomainTask:
        return FailingTask(self.job_name, self.fail_at_percent)

    def build_title(self) -> str:
        return f"Fragile Task: {self.job_name}"


@dataclass(frozen=True)
class TaskDefinition:
    factory_cls: type[TaskFactory]
    start_text: str = "Start"
    cancel_text: str = "Cancel"
