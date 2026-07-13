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
LOCAL_NO_KEY_ROUTE_RE = re.compile(
    r"API-ключ|no-key|обязательный путь полностью локальн", re.IGNORECASE
)
SELF_CONTAINED_RE = re.compile(r"самодостаточ", re.IGNORECASE)


def validate_lesson(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = [f"{path}: нет раздела {section}" for section in REQUIRED_SECTIONS if section not in text]
    outcome = text.split("## Зачем это инженеру", 1)[0]
    if not OUTCOME_ARTIFACT_RE.search(outcome):
        errors.append(f"{path}: нет именованного артефакта в результате урока")
    if "https://" not in text:
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
    elif not LOCAL_NO_KEY_ROUTE_RE.search(readme.read_text(encoding="utf-8")):
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
    elif not SELF_CONTAINED_RE.search(readme.read_text(encoding="utf-8")):
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
