import pytest

from task_app import TaskService, TaskStatus


def test_create_task_assigns_integer_id():
    task = TaskService().create_task("Проверить контракт")
    assert task.id == 1
    assert task.status is TaskStatus.OPEN


def test_empty_title_is_rejected():
    with pytest.raises(ValueError, match="Название задачи не может быть пустым"):
        TaskService().create_task("   ")


def test_duplicate_active_title_is_rejected():
    service = TaskService()
    service.create_task("Проверить контракт")
    with pytest.raises(ValueError, match="Активная задача с таким названием уже существует"):
        service.create_task("проверить КОНТРАКТ")


def test_unknown_task_cannot_be_completed():
    with pytest.raises(KeyError, match="Задача 99 не найдена"):
        TaskService().complete_task(99)


def test_complete_task_records_done_status():
    service = TaskService()
    task = service.create_task("Проверить контракт")
    completed = service.complete_task(task.id)
    assert completed.status is TaskStatus.DONE
