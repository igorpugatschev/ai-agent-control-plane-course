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


def validate_lesson(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = [f"{path}: нет раздела {section}" for section in REQUIRED_SECTIONS if section not in text]
    if "https://" not in text:
        errors.append("нет ссылки на официальный источник")
    if re.search(r"[А-Яа-яЁё]", text) is None:
        errors.append(f"{path}: нет русскоязычного объяснения")
    return errors


def validate_module(path: Path) -> list[str]:
    errors: list[str] = []
    lessons = sorted(path.glob("lesson-*.md"))
    if not (path / "README.md").is_file():
        errors.append(f"{path}: нет README.md")
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
