# Module 02 checkpoint assessment guide

## Артефакты

- `artifacts/module-02/source-register.md`.
- `artifacts/module-02/context-packet.md`.
- `artifacts/module-02/context-map-evidence-gate.md`.

## Критерии оценки

| Критерий | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Иерархия источников | Конфликт решен догадкой | Источники без authority | Trust, Source owner/unknown, Authority owner и conflict rule различены |
| Свежесть и факт | Нет date/SHA/confidence | Categories смешаны | Fact, assumption и live state разделены, metadata воспроизводимы |
| Минимальный packet | Передан весь repo/нет citations | Лишние inputs без причины | Один вопрос, trusted/untrusted inputs, exclusions и citations достаточны |
| Evidence gate и STOP | Implementation разрешена | STOP без owner/re-run | Command/output, owners, correction и resume condition связаны |

## Наблюдаемое evidence

Reviewer повторяет pytest command, находит repo-relative sources и видит, что
stale documentation не становится instruction к реализации.

## Критические дефекты

- Нет Source owner либо documented `unknown` с эскалацией, отдельного Authority owner или check date.
- Нет SHA/command/output, либо service/API меняется до owner decision.

## Маршрут исправления

Исправьте поля во всех трех artifacts, верните conflict к Authority owner,
удалите unsupported implementation и повторите walkthrough.

## Повторная команда

```bash
test -f artifacts/module-02/source-register.md
```
