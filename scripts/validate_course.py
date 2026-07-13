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
    r"\b(?:локальн\w*|репозитори\w*|offline)\b|"
    r"\bна\s+(?:своей|локальной)\s+машин\w*\b",
    re.IGNORECASE,
)
LOCAL_ACTION_PATTERN = (
    r"(?:использу\w*|прочита\w*|откро\w*|заполн\w*|созда\w*|провер\w*|"
    r"запуст\w*|выполн\w*|сохран\w*|работа(?:ет|ют|йте))"
)
LOCAL_ACTION_RE = re.compile(rf"\b{LOCAL_ACTION_PATTERN}\b", re.IGNORECASE)
NEGATED_LOCAL_ACTION_RE = re.compile(
    rf"\bне\s+{LOCAL_ACTION_PATTERN}\b", re.IGNORECASE
)
LOCAL_RESOURCE_RE = re.compile(
    r"`[^`\n]+`|\[[^]\n]+\]\([^)\n]+\)|"
    r"\b(?:файл\w*|артефакт\w*|markdown|yaml|git|pytest|команд\w*|"
    r"prepared|подготовлен\w*)\b",
    re.IGNORECASE,
)
PAID_ACCESS_RE = re.compile(
    r"\b(?:api[- ]?ключ\w*|paid\s+api\s+key|платн\w*\s+(?:api[- ]?)?ключ\w*|"
    r"платн\w*\s+(?:уч[её]тн\w*\s+запис\w*|аккаунт\w*|подписк\w*))\b",
    re.IGNORECASE,
)
CLOUD_ACCESS_RE = re.compile(
    r"\b(?:обла(?:к|ч)\w*|cloud(?:\s+(?:platform|account|service))?)\b",
    re.IGNORECASE,
)
DEPENDENCY_REQUIREMENT_RE = re.compile(
    r"\b(?:обязател\w*|необходим\w*|нуж\w*|понадоб\w*|требу\w*|required|must)\b",
    re.IGNORECASE,
)
DEPENDENCY_ABSENCE_RE = re.compile(
    r"\bбез\b|\bno-key\b|"
    r"\bне\s+(?:требу\w*|нуж\w*|понадоб\w*|необходим\w*|обязател\w*)\b|"
    r"\b(?:not\s+required|not\s+needed)\b",
    re.IGNORECASE,
)
CLAUSE_SPLIT_RE = re.compile(
    r"(?<=[.!?;:])\s+|\n[ \t]*\n+|,\s*(?:но|однако|а)\s+",
    re.IGNORECASE,
)
NO_KEY_RE = re.compile(r"\bno-key\b", re.IGNORECASE)
DEPENDENCIES = (
    (PAID_ACCESS_RE, NO_KEY_RE, "платный API-ключ", "платного API-ключа"),
    (CLOUD_ACCESS_RE, None, "облачную зависимость", "облачной зависимости"),
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


def dependency_evidence(
    text: str, target: re.Pattern[str], alias: re.Pattern[str] | None
) -> tuple[bool, bool]:
    absence = False
    required = False
    for clause in CLAUSE_SPLIT_RE.split(text):
        if target.search(clause) is None and (alias is None or alias.search(clause) is None):
            continue
        if DEPENDENCY_ABSENCE_RE.search(clause):
            absence = True
        elif DEPENDENCY_REQUIREMENT_RE.search(clause):
            required = True
    return absence, required


def validate_dependency_contract(
    text: str, path: Path, *, require_absence: bool
) -> list[str]:
    errors: list[str] = []
    for target, alias, required_label, absence_label in DEPENDENCIES:
        absence, required = dependency_evidence(text, target, alias)
        if required:
            errors.append(f"{path}: обязательный маршрут требует {required_label}")
        if require_absence and not absence:
            errors.append(
                f"{path}: нет явного подтверждения отсутствия {absence_label}"
            )
    return errors


def validate_local_route(
    section: str,
    path: Path,
    route_name: str,
    *,
    require_dependency_absence: bool = False,
) -> list[str]:
    errors: list[str] = []
    positive_action_text = NEGATED_LOCAL_ACTION_RE.sub("", section)
    is_actionable = (
        LOCAL_CONTEXT_RE.search(section)
        and LOCAL_ACTION_RE.search(positive_action_text)
        and LOCAL_RESOURCE_RE.search(section)
    )
    if not is_actionable:
        errors.append(f"{path}: {route_name} не описан")
    errors.extend(
        validate_dependency_contract(
            section, path, require_absence=require_dependency_absence
        )
    )
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
            errors.extend(
                validate_local_route(
                    local_route,
                    path,
                    "локальный маршрут",
                    require_dependency_absence=True,
                )
            )
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
        if entry is not None:
            errors.extend(
                validate_dependency_contract(entry, root, require_absence=False)
            )
        if offline_no_key_route is not None:
            errors.extend(
                validate_local_route(
                    offline_no_key_route,
                    root,
                    "локальный offline/no-key маршрут",
                    require_dependency_absence=True,
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
