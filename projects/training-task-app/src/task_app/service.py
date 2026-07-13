from .models import Task, TaskStatus


class TaskService:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def create_task(self, title: str) -> Task:
        normalized = title.strip()
        if not normalized:
            raise ValueError("Название задачи не может быть пустым")
        if any(
            task.status is TaskStatus.OPEN and task.title.casefold() == normalized.casefold()
            for task in self._tasks.values()
        ):
            raise ValueError("Активная задача с таким названием уже существует")
        task = Task(id=self._next_id, title=normalized)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def list_tasks(self) -> list[Task]:
        return [self._tasks[task_id] for task_id in sorted(self._tasks)]

    def complete_task(self, task_id: int) -> Task:
        if type(task_id) is not int or task_id not in self._tasks:
            raise KeyError(f"Задача {task_id} не найдена")
        self._tasks[task_id].status = TaskStatus.DONE
        return self._tasks[task_id]
