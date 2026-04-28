from __future__ import annotations

from dataclasses import dataclass

from framework.domain import TaskType


@dataclass(frozen=True)
class TaskBlueprint:
    task_type: TaskType
    title: str
    primary_value: str
    secondary_value: int


@dataclass(frozen=True)
class ScenarioDefinition:
    name: str
    description: str
    tasks: tuple[TaskBlueprint, ...]
