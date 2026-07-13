from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_SECTIONS = (
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
OUTCOME_ARTIFACT_RE = re.compile(r"`artifacts/[^`\n]+`")
HTTPS_URL_RE = re.compile(r"https://[^\s)]+")
MODULE_LOCAL_ROUTE_HEADING = "Обязательный локальный маршрут"
CURRICULUM_ENTRY_HEADING = "Перед началом"
CURRICULUM_OFFLINE_NO_KEY_HEADING = "### Обязательный offline/no-key режим"
CURRICULUM_SELF_CONTAINED_STATEMENT = (
    "Обязательный маршрут самодостаточен: теория, задания, критерии готовности и "
    "маршруты исправления находятся локально в репозитории."
)


def extract_level_two_section(text: str, heading: str) -> str | None:
    match = re.search(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE)
    if match is None:
        return None
    next_heading = re.search(r"^## ", text[match.end() :], re.MULTILINE)
    end = len(text) if next_heading is None else match.end() + next_heading.start()
    return text[match.end() : end]


def validate_lesson(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = [f"{path}: нет раздела {section}" for section in REQUIRED_SECTIONS if section not in text]
    outcome = extract_level_two_section(text, "Результат урока")
    if outcome is None or not OUTCOME_ARTIFACT_RE.search(outcome):
        errors.append(f"{path}: нет именованного артефакта в результате урока")
    sources = extract_level_two_section(text, "Официальные источники")
    if sources is None or not HTTPS_URL_RE.search(sources):
        errors.append("нет ссылки на официальный источник")
    if re.search(r"[А-Яа-яЁё]", text) is None:
        errors.append(f"{path}: нет русскоязычного объяснения")
    return errors


def validate_module(path: Path) -> list[str]:
    errors: list[str] = []
    lessons = sorted(path.glob("lesson-*.md"))
    readme = path / "README.md"
    if not readme.is_file():
        errors.append(f"{path}: нет README.md")
    elif extract_level_two_section(
        readme.read_text(encoding="utf-8"), MODULE_LOCAL_ROUTE_HEADING
    ) is None:
        errors.append(f"{path}: нет явного offline/no-key маршрута")
    if not (path / "checkpoint.md").is_file():
        errors.append(f"{path}: нет checkpoint.md")
    if len(lessons) != 3:
        errors.append(f"{path}: ожидалось 3 урока, найдено {len(lessons)}")
    for lesson in lessons:
        errors.extend(validate_lesson(lesson))
    return errors


def validate_course(root: Path) -> list[str]:
    if root.name.startswith("module-"):
        return validate_module(root)
    modules = sorted(path for path in root.glob("module-*") if path.is_dir())
    errors: list[str] = []
    readme = root / "README.md"
    if not readme.is_file():
        errors.append(f"{root}: нет README.md")
    else:
        readme_text = readme.read_text(encoding="utf-8")
        entry = extract_level_two_section(readme_text, CURRICULUM_ENTRY_HEADING)
        has_self_contained_route = (
            entry is not None
            and CURRICULUM_SELF_CONTAINED_STATEMENT in " ".join(entry.split())
        )
        has_offline_no_key_route = (
            re.search(
                rf"^{re.escape(CURRICULUM_OFFLINE_NO_KEY_HEADING)}\s*$",
                readme_text,
                re.MULTILINE,
            )
            is not None
        )
        if not (has_self_contained_route and has_offline_no_key_route):
            errors.append(f"{root}: нет self-contained политики")
    if len(modules) != 7:
        errors.append(f"{root}: ожидалось 7 модулей, найдено {len(modules)}")
    for module in modules:
        errors.extend(validate_module(module))
    lesson_count = sum(len(list(module.glob("lesson-*.md"))) for module in modules)
    if lesson_count != 21:
        errors.append(f"{root}: ожидался 21 урок, найдено {lesson_count}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет структуру курса")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_course(args.path)
    if errors:
        print("\n".join(errors))
        return 1
    print("Курс проверен: ошибок нет")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
