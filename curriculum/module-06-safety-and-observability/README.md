# Модуль 6. Безопасность, оценка и наблюдаемость

Этот модуль добавляет к control plane слой, который не дает агенту превратить
непроверенный текст в команду или скрыть плохое решение за словом "готово".
Сначала студент строит threat model, затем разделяет stop-gate, review-gate и
human approval, после чего измеряет поведение на cases и сохраняет trace с
решением.

К концу модуля вы создадите пять связанных артефактов:

1. [Threat model и недоверенный контекст](lesson-16-threat-model-prompt-injection.md) - `artifacts/module-06/threat-model.md`.
2. [Stop, review и approval gates](lesson-17-stop-review-approval-gates.md) - `artifacts/module-06/approval-matrix.md`.
3. [Оценка, трассировка и журнал решений](lesson-18-evaluation-tracing-decision-log.md) - `artifacts/module-06/evaluation-dataset.md`, `trace-record.md` и `decision-log.md`.
4. [Checkpoint 6](checkpoint.md) - проверка реакции на недоверенную инструкцию в документации.

## Как проходить модуль

Обязательный маршрут локальный: используйте prepared response из уроков,
`projects/training-task-app/` и contracts из `agents/` и `templates/`. Не нужны
сеть, API-ключ, внешний LLM или доступ к секретам. Внешние ссылки подтверждают
термины и подходы, но не заменяют теорию, checks или correction route внутри
модуля.

Сначала прочитайте [risk reviewer](../../agents/risk-reviewer.md),
[coordinator](../../agents/coordinator.md), [stop-gate](../../templates/stop-gate.md),
[review-gate](../../templates/review-gate.md) и
[журнал решений](../../templates/decision-log.md). Учебный `TaskService` не
меняйте: он служит только безопасным объектом intended action.

## Готовность модуля

Модуль завершен, если:

- threat model перечисляет assets, actors, trust boundaries, entry points и
  controls, а не только слово "prompt injection";
- внешний документ и output инструмента помечены как недоверенные данные и не
  могут расширить permission агента;
- необратимое или привилегированное действие останавливается до documented
  human approval; review качества не выдается за approval;
- evaluation dataset содержит нормальные, отказные и adversarial cases, outcome
  metrics и ожидаемую маршрутизацию;
- trace имеет run id, входы по ссылке/хэшу, tool observations, redaction,
  gate/decision и owner, а decision log объясняет основание и пересмотр;
- checkpoint фиксирует injection event, **никогда не исполняет вредоносную
  инструкцию** и запрашивает approval только для intended action.
