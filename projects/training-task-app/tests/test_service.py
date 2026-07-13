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


@pytest.mark.parametrize(
    ("task_id", "message"),
    [
        (1.0, "Задача 1.0 не найдена"),
        (True, "Задача True не найдена"),
    ],
)
def test_complete_task_rejects_non_integer_ids(task_id, message):
    service = TaskService()
    task = service.create_task("Проверить контракт")

    with pytest.raises(KeyError) as error:
        service.complete_task(task_id)

    assert error.value.args == (message,)
    assert task.status is TaskStatus.OPEN


def test_complete_task_records_done_status():
    service = TaskService()
    task = service.create_task("Проверить контракт")
    completed = service.complete_task(task.id)
    assert completed.status is TaskStatus.DONE


def test_create_task_strips_title():
    task = TaskService().create_task("  Проверить контракт  ")
    assert task.title == "Проверить контракт"


def test_list_tasks_returns_tasks_in_id_order():
    service = TaskService()
    first = service.create_task("Первая задача")
    second = service.create_task("Вторая задача")
    service.complete_task(first.id)

    assert service.list_tasks() == [first, second]


def test_title_can_be_reused_after_task_is_done():
    service = TaskService()
    first = service.create_task("Проверить контракт")
    service.complete_task(first.id)

    second = service.create_task("проверить КОНТРАКТ")

    assert second.id == 2
    assert second.title == "проверить КОНТРАКТ"


def test_task_services_are_isolated():
    first_service = TaskService()
    second_service = TaskService()

    first = first_service.create_task("Одинаковое имя")
    second = second_service.create_task("Одинаковое имя")

    assert first.id == second.id == 1
    assert first_service.list_tasks() == [first]
    assert second_service.list_tasks() == [second]
