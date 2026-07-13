from pathlib import Path

from scripts.validate_course import REQUIRED_SECTIONS, validate_course, validate_lesson, validate_module


def write_complete_lesson(path, result: str = "Артефакт: `artifacts/module/output.md`."):
    sections = list(REQUIRED_SECTIONS)
    sections[0] = f"{sections[0]}\n\n{result}"
    sections[-1] = f"{sections[-1]}\n\nhttps://example.com/official"
    path.write_text("\n\n".join(sections), encoding="utf-8")


def test_required_sections_match_approved_lesson_format():
    assert REQUIRED_SECTIONS == (
        "## Результат урока",
        "## Зачем это инженеру",
        "## Теория",
        "## Ключевые термины",
        "## Рабочий пример",
        "## Практика",
        "## Проверка результата",
        "## Типичные ошибки",
        "## Контрольные вопросы",
        "## Официальные источники",
    )


def test_lesson_requires_official_https_source(tmp_path):
    lesson = tmp_path / "lesson.md"
    lesson.write_text("\n".join(REQUIRED_SECTIONS), encoding="utf-8")
    assert "нет ссылки на официальный источник" in validate_lesson(lesson)


def test_lesson_requires_named_artifact_in_its_outcome(tmp_path):
    lesson = tmp_path / "lesson.md"
    write_complete_lesson(lesson, result="Студент объяснит разницу между ролью и tool.")
    assert any(
        "нет именованного артефакта в результате урока" in error
        for error in validate_lesson(lesson)
    )


def test_module_requires_an_explicit_local_no_key_route(tmp_path):
    module = tmp_path / "module-01-foundations"
    module.mkdir()
    (module / "README.md").write_text("Обязательный маршрут локальный.", encoding="utf-8")
    for number in range(1, 4):
        write_complete_lesson(module / f"lesson-0{number}-topic.md")
    (module / "checkpoint.md").write_text("# Checkpoint", encoding="utf-8")

    assert any("нет явного offline/no-key маршрута" in error for error in validate_module(module))


def test_curriculum_requires_self_contained_entry_policy(tmp_path):
    curriculum = tmp_path / "curriculum"
    curriculum.mkdir()
    (curriculum / "README.md").write_text("Курс на русском языке.", encoding="utf-8")
    for number in range(1, 8):
        module = curriculum / f"module-{number:02d}-topic"
        module.mkdir()
        (module / "README.md").write_text(
            "Обязательный локальный маршрут не требует API-ключа.", encoding="utf-8"
        )
        for lesson_number in range(1, 4):
            write_complete_lesson(module / f"lesson-{lesson_number:02d}-topic.md")
        (module / "checkpoint.md").write_text("# Checkpoint", encoding="utf-8")

    assert any("нет self-contained политики" in error for error in validate_course(curriculum))


def test_complete_course_has_no_structure_errors():
    assert validate_course(Path("curriculum")) == []
