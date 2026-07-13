# Task 1: Implementer Report

## Status

DONE_WITH_CONCERNS

## Изменения

- Создан `scripts/validate_course.py` с интерфейсами `validate_lesson(path)`, `validate_module(path)` и `validate_course(root)`.
- Зафиксирован единый `REQUIRED_SECTIONS` из десяти обязательных разделов урока.
- Добавлены проверки официальной HTTPS-ссылки и русскоязычного объяснения в уроке.
- Добавлены структурные проверки README, checkpoint, трёх уроков в модуле, семи модулей и 21 урока в курсе.
- Создан `tests/test_course_structure.py` с контрактными тестами из brief.
- Создан `curriculum/README.md` с prerequisites, оценкой 50-70 часов, таблицей семи модулей, artifact-first потоком, offline/no-key и live-agent режимами, правилами checkpoint и ссылками на каждый модуль.
- В корневой `README.md` добавлен основной CTA на `curriculum/README.md`.

## TDD RED -> GREEN evidence

### RED

Команда:

```text
python3 -m pytest tests/test_course_structure.py -q
```

Результат: коллекция упала с ожидаемой причиной `ModuleNotFoundError: No module named 'scripts'`, так как `scripts.validate_course` ещё не существовал.

### GREEN

Focused-команда:

```text
python3 -m pytest tests/test_course_structure.py::test_required_sections_match_approved_lesson_format tests/test_course_structure.py::test_lesson_requires_official_https_source -q
```

Результат: `2 passed in 0.31s`.

## Verification

- `python3 -m pytest -q` -> `2 passed in 0.01s`.
- `python3 -m py_compile scripts/validate_course.py` -> exit code `0`.
- `git diff --check` -> exit code `0`.
- `python3 scripts/validate_course.py curriculum` -> exit code `1`, сообщает `7` ожидаемых модулей и `21` ожидаемый урок при фактических `0`; это ожидаемо до выполнения следующих задач контентного плана.

## Изменённые файлы

- `scripts/validate_course.py`
- `tests/test_course_structure.py`
- `curriculum/README.md`
- `README.md`
- `.superpowers/sdd/task-1-implementer-report.md`

## Self-review

- Scope проверен по `git status`: изменения находятся только в зоне задачи 1.
- `REQUIRED_SECTIONS` побайтно соответствует утверждённому формату из brief.
- Ошибка отсутствующей официальной ссылки содержит требуемую фразу `нет ссылки на официальный источник`.
- Валидатор использует UTF-8, типы `Path`, стандартную библиотеку и минимальную реализацию из brief.
- Curriculum entry page содержит все перечисленные в brief обязательные элементы и не делает live-agent режим обязательным.
- Root README сохраняет существующий текст и получает явный primary CTA.
- После изменений повторно выполнены focused и полный доступный pytest, синтаксическая проверка и `git diff --check`.

## Concerns

- `validate_course curriculum` пока закономерно завершается с ошибкой, потому что модули, уроки и checkpoints создаются последующими задачами.
- Ссылки на семь модулей в `curriculum/README.md` заранее направлены на пути, которые появятся в следующих задачах.
- Более глубокие проверки внутренних ссылок и placeholders предусмотрены спецификацией курса, но не входят в контракт Task 1 и требуют отдельного расширения в последующих задачах.

## Commit

Создан коммит с сообщением `feat: add course structure validator`.
