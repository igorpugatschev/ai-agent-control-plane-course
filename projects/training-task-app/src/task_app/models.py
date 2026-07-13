from dataclasses import dataclass
from enum import StrEnum


class TaskStatus(StrEnum):
    OPEN = "open"
    DONE = "done"


@dataclass(slots=True)
class Task:
    id: int
    title: str
    status: TaskStatus = TaskStatus.OPEN
