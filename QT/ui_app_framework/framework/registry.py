from __future__ import annotations

from .domain import TaskDefinition, TaskFactory, TaskKey, task_key_to_string


class TaskRegistry:
    def __init__(self):
        self._definitions: dict[str, TaskDefinition] = {}

    def register(self, task_type: TaskKey, definition: TaskDefinition):
        self._definitions[task_key_to_string(task_type)] = definition

    def get_definition(self, task_type: TaskKey) -> TaskDefinition:
        key = task_key_to_string(task_type)
        definition = self._definitions.get(key)
        if definition is None:
            raise ValueError(f"Unknown task type: {key}")
        return definition

    def create_factory(self, task_type: TaskKey, *args, **kwargs) -> TaskFactory:
        definition = self.get_definition(task_type)
        return definition.factory_cls(*args, **kwargs)
