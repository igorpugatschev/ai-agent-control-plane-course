from pathlib import Path

from scripts.validate_course import REQUIRED_SECTIONS, validate_course, validate_lesson, validate_module


VALID_MODULE_ROUTE = """## Обязательный локальный маршрут

Прочитайте локальные Markdown-файлы, заполните артефакт и запустите pytest.
Платный API-ключ и облачная платформа для обязательного маршрута не требуются.
"""


def write_complete_module(path, readme_text: str = VALID_MODULE_ROUTE):
    path.mkdir()
    (path / "README.md").write_text(readme_text, encoding="utf-8")
    for number in range(1, 4):
        write_complete_lesson(path / f"lesson-{number:02d}-topic.md")
    (path / "checkpoint.md").write_text("# Checkpoint", encoding="utf-8")


def write_complete_curriculum(path, readme_text: str):
    path.mkdir()
    (path / "README.md").write_text(readme_text, encoding="utf-8")
    for number in range(1, 8):
        write_complete_module(path / f"module-{number:02d}-topic")


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


def test_lesson_does_not_count_an_artifact_before_its_outcome_section(tmp_path):
    lesson = tmp_path / "lesson.md"
    write_complete_lesson(lesson, result="Студент объяснит разницу между ролью и tool.")
    lesson.write_text(
        "`artifacts/preamble-only.md`\n\n" + lesson.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    assert any(
        "нет именованного артефакта в результате урока" in error
        for error in validate_lesson(lesson)
    )


def test_lesson_counts_an_artifact_inside_its_outcome_section(tmp_path):
    lesson = tmp_path / "lesson.md"
    write_complete_lesson(lesson)

    assert validate_lesson(lesson) == []


def test_lesson_does_not_count_a_source_before_its_sources_section(tmp_path):
    lesson = tmp_path / "lesson.md"
    write_complete_lesson(lesson)
    text = lesson.read_text(encoding="utf-8").replace(
        "## Официальные источники\n\nhttps://example.com/official",
        "## Официальные источники\n\nЛокальная теория достаточна.",
    )
    lesson.write_text("https://example.com/preamble\n\n" + text, encoding="utf-8")

    assert "нет ссылки на официальный источник" in validate_lesson(lesson)


def test_lesson_counts_a_source_inside_its_sources_section(tmp_path):
    lesson = tmp_path / "lesson.md"
    write_complete_lesson(lesson)

    assert validate_lesson(lesson) == []


def test_module_requires_an_explicit_local_no_key_route(tmp_path):
    module = tmp_path / "module-01-foundations"
    module.mkdir()
    (module / "README.md").write_text("Обязательный маршрут локальный.", encoding="utf-8")
    for number in range(1, 4):
        write_complete_lesson(module / f"lesson-0{number}-topic.md")
    (module / "checkpoint.md").write_text("# Checkpoint", encoding="utf-8")

    assert any("нет явного offline/no-key маршрута" in error for error in validate_module(module))


def test_module_keyword_claim_does_not_replace_local_route_heading(tmp_path):
    module = tmp_path / "module-01-foundations"
    module.mkdir()
    (module / "README.md").write_text(
        "Обязательный маршрут полностью локальный и не требует API-ключа.",
        encoding="utf-8",
    )
    for number in range(1, 4):
        write_complete_lesson(module / f"lesson-0{number}-topic.md")
    (module / "checkpoint.md").write_text("# Checkpoint", encoding="utf-8")

    assert any("нет явного offline/no-key маршрута" in error for error in validate_module(module))


def test_module_heading_without_actionable_local_route_is_rejected(tmp_path):
    module = tmp_path / "module-01-foundations"
    write_complete_module(module, "## Обязательный локальный маршрут")

    assert any("локальный маршрут не описан" in error for error in validate_module(module))


def test_module_rejects_a_paid_key_as_mandatory(tmp_path):
    module = tmp_path / "module-01-foundations"
    write_complete_module(
        module,
        """## Обязательный локальный маршрут

Прочитайте локальные Markdown-файлы и заполните артефакт по шаблону.
Для выполнения обязателен платный API-ключ.
""",
    )

    assert any("требует платный API-ключ/облако" in error for error in validate_module(module))


def test_module_accepts_a_paraphrased_local_no_paid_key_route(tmp_path):
    module = tmp_path / "module-01-foundations"
    write_complete_module(module)

    assert validate_module(module) == []


def test_curriculum_requires_self_contained_entry_policy(tmp_path):
    curriculum = tmp_path / "curriculum"
    curriculum.mkdir()
    (curriculum / "README.md").write_text("Курс на русском языке.", encoding="utf-8")
    for number in range(1, 8):
        module = curriculum / f"module-{number:02d}-topic"
        module.mkdir()
        (module / "README.md").write_text("## Обязательный локальный маршрут", encoding="utf-8")
        for lesson_number in range(1, 4):
            write_complete_lesson(module / f"lesson-{lesson_number:02d}-topic.md")
        (module / "checkpoint.md").write_text("# Checkpoint", encoding="utf-8")

    assert any("нет self-contained политики" in error for error in validate_course(curriculum))


def test_curriculum_keyword_claim_does_not_replace_self_contained_route_structure(tmp_path):
    curriculum = tmp_path / "curriculum"
    curriculum.mkdir()
    (curriculum / "README.md").write_text(
        "Курс самодостаточен, но обязательный маршрут не самодостаточен.",
        encoding="utf-8",
    )
    for number in range(1, 8):
        module = curriculum / f"module-{number:02d}-topic"
        module.mkdir()
        (module / "README.md").write_text("## Обязательный локальный маршрут", encoding="utf-8")
        for lesson_number in range(1, 4):
            write_complete_lesson(module / f"lesson-{lesson_number:02d}-topic.md")
        (module / "checkpoint.md").write_text("# Checkpoint", encoding="utf-8")

    assert any("нет self-contained политики" in error for error in validate_course(curriculum))


def test_curriculum_rejects_headings_without_an_actionable_local_route(tmp_path):
    curriculum = tmp_path / "curriculum"
    write_complete_curriculum(
        curriculum,
        """## Перед началом

Обязательный маршрут самодостаточен: теория, задания, критерии готовности и
маршруты исправления находятся локально в репозитории.

## Два режима выполнения

### Обязательный offline/no-key режим
""",
    )

    assert any("локальный offline/no-key маршрут не описан" in error for error in validate_course(curriculum))


def test_curriculum_rejects_cloud_access_as_mandatory(tmp_path):
    curriculum = tmp_path / "curriculum"
    write_complete_curriculum(
        curriculum,
        """## Перед началом

Обязательный маршрут самодостаточен: теория, задания, критерии готовности и
маршруты исправления находятся локально в репозитории.

## Два режима выполнения

### Обязательный offline/no-key режим

Прочитайте локальные материалы и выполните проверки через pytest.
Для прохождения нужен доступ к облаку.
""",
    )

    assert any("требует платный API-ключ/облако" in error for error in validate_course(curriculum))


def test_curriculum_rejects_a_paid_key_in_the_entry_policy(tmp_path):
    curriculum = tmp_path / "curriculum"
    write_complete_curriculum(
        curriculum,
        """## Перед началом

Обязательный маршрут самодостаточен и хранится локально в репозитории.
Для начала обязателен платный API-ключ.

## Два режима выполнения

### Обязательный offline/no-key режим

Прочитайте локальные файлы, заполните Markdown-артефакт и запустите pytest.
API-ключ и облачный аккаунт для этого пути не требуются.
""",
    )

    assert any("требует платный API-ключ/облако" in error for error in validate_course(curriculum))


def test_curriculum_accepts_a_paraphrased_self_contained_no_paid_key_route(tmp_path):
    curriculum = tmp_path / "curriculum"
    write_complete_curriculum(
        curriculum,
        """## Перед началом

Весь обязательный материал самодостаточен и хранится локально в этом репозитории.

## Два режима выполнения

### Обязательный offline/no-key режим

Пройдите задания по локальным файлам, сохраните Markdown-артефакты и запустите pytest.
Платный API-ключ и облачный аккаунт для этого пути не требуются.
""",
    )

    assert validate_course(curriculum) == []


def test_complete_course_has_no_structure_errors():
    assert validate_course(Path("curriculum")) == []
