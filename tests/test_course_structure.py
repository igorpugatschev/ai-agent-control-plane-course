from pathlib import Path

from scripts.validate_course import REQUIRED_SECTIONS, validate_course, validate_lesson


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


def test_complete_course_has_no_structure_errors():
    assert validate_course(Path("curriculum")) == []
