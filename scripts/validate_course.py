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
CURRICULUM_OFFLINE_NO_KEY_HEADING = "Обязательный offline/no-key режим"
SELF_CONTAINED_RE = re.compile(r"самодостаточ\w*", re.IGNORECASE)
LOCAL_CONTEXT_RE = re.compile(
    r"\b(?:локальн\w*|репозитори\w*|offline)\b",
    re.IGNORECASE,
)
LOCAL_ACTION_RE = re.compile(
    r"\b(?:использу\w*|прочита\w*|заполн\w*|созда\w*|провер\w*|запуст\w*|"
    r"выполн\w*|сохран\w*|работа(?:ет|ют|йте))\b",
    re.IGNORECASE,
)
LOCAL_RESOURCE_RE = re.compile(
    r"`[^`\n]+`|\[[^]\n]+\]\([^)\n]+\)|"
    r"\b(?:файл\w*|артефакт\w*|markdown|yaml|git|pytest|команд\w*|"
    r"prepared|подготовлен\w*)\b",
    re.IGNORECASE,
)
PAID_DEPENDENCY_TARGET_RE = re.compile(
    r"\b(?:api[- ]?ключ\w*|paid\s+api\s+key|платн\w*\s+(?:api[- ]?)?ключ\w*|"
    r"облак\w*|cloud(?:\s+(?:platform|account))?)\b",
    re.IGNORECASE,
)
DEPENDENCY_REQUIREMENT_RE = re.compile(
    r"\b(?:обязател(?:ен|ьна|ьно|ьны)|необходим\w*|нуж(?:ен|на|но|ны)|"
    r"требу(?:ется|ются|ет|ют)|required|must)\b",
    re.IGNORECASE,
)
NO_PAID_DEPENDENCY_RE = re.compile(
    r"\bбез\b.{0,80}\b(?:api[- ]?ключ\w*|платн\w*\s+(?:api[- ]?)?ключ\w*|"
    r"облак\w*|cloud(?:\s+(?:platform|account))?)\b|"
    r"\bне\s+(?:требу\w*|нуж\w*|необходим\w*|обязател\w*)\b.{0,80}"
    r"\b(?:api[- ]?ключ\w*|платн\w*\s+(?:api[- ]?)?ключ\w*|облачн\w*|cloud)\b|"
    r"\b(?:api[- ]?ключ\w*|платн\w*\s+(?:api[- ]?)?ключ\w*|облачн\w*|cloud)\b"
    r".{0,80}\bне\s+(?:требу\w*|нуж\w*|необходим\w*|обязател\w*)\b|"
    r"\bno-key\b",
    re.IGNORECASE,
)


def extract_markdown_section(text: str, heading: str, level: int) -> str | None:
    marker = "#" * level
    match = re.search(rf"^{marker} {re.escape(heading)}\s*$", text, re.MULTILINE)
    if match is None:
        return None
    next_heading = re.search(rf"^#{{1,{level}}} ", text[match.end() :], re.MULTILINE)
    end = len(text) if next_heading is None else match.end() + next_heading.start()
    return text[match.end() : end]


def extract_level_two_section(text: str, heading: str) -> str | None:
    return extract_markdown_section(text, heading, level=2)


def requires_paid_dependency(text: str) -> bool:
    statements = re.split(r"(?<=[.!?])\s+|\n+", text)
    return any(
        PAID_DEPENDENCY_TARGET_RE.search(statement)
        and DEPENDENCY_REQUIREMENT_RE.search(statement)
        and not NO_PAID_DEPENDENCY_RE.search(statement)
        for statement in statements
    )


def validate_local_route(
    section: str,
    path: Path,
    route_name: str,
    *,
    require_no_paid_dependency: bool = False,
) -> list[str]:
    errors: list[str] = []
    is_actionable = (
        LOCAL_CONTEXT_RE.search(section)
        and LOCAL_ACTION_RE.search(section)
        and LOCAL_RESOURCE_RE.search(section)
    )
    if not is_actionable:
        errors.append(f"{path}: {route_name} не описан")
    if requires_paid_dependency(section):
        errors.append(f"{path}: обязательный маршрут требует платный API-ключ/облако")
    if require_no_paid_dependency and not NO_PAID_DEPENDENCY_RE.search(section):
        errors.append(f"{path}: нет явного режима без платного API-ключа/облака")
    return errors


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
    else:
        local_route = extract_level_two_section(
            readme.read_text(encoding="utf-8"), MODULE_LOCAL_ROUTE_HEADING
        )
        if local_route is None:
            errors.append(f"{path}: нет явного offline/no-key маршрута")
        else:
            errors.extend(validate_local_route(local_route, path, "локальный маршрут"))
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
            and SELF_CONTAINED_RE.search(entry)
            and LOCAL_CONTEXT_RE.search(entry)
        )
        offline_no_key_route = extract_markdown_section(
            readme_text, CURRICULUM_OFFLINE_NO_KEY_HEADING, level=3
        )
        if not has_self_contained_route or offline_no_key_route is None:
            errors.append(f"{root}: нет self-contained политики")
        if entry is not None and requires_paid_dependency(entry):
            errors.append(f"{root}: обязательный маршрут требует платный API-ключ/облако")
        if offline_no_key_route is not None:
            errors.extend(
                validate_local_route(
                    offline_no_key_route,
                    root,
                    "локальный offline/no-key маршрут",
                    require_no_paid_dependency=True,
                )
            )
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
