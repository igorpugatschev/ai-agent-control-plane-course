# Урок 15. Regression, defect/flaky triage и release gate

## Результат урока

Вы создадите `artifacts/module-05/triage-and-release-gate.md`: пакет defect/flaky triage, обоснованный regression scope и release gate, который останавливает выпуск без traceability.

## Зачем это инженеру

Не каждый failed run - продуктовый дефект, и не каждый green run - основание для выпуска. Defect fixture описывает детерминированное неправильное поведение в дефектной версии. Flaky log показывает разные результаты одной команды при неизмененных inputs и требует расследования, а не автоматического retry. Смешение этих состояний приводит либо к игнорированию регрессии, либо к ложной блокировке релиза.

Release gate соединяет traceability, test evidence, known defects, instability, риск и назначенного decision owner. QA/SDET дает quality evidence; coordinator проверяет полноту и routing; risk reviewer принимает отдельное approval/reject/STOP для высокорискового выпуска, а human owner остается владельцем final product acceptance. Без матрицы нельзя узнать, какие условия покрыты, поэтому выпуск должен остановиться.

## Теория

### Reproduction и regression scope

Defect report воспроизводим, когда заданы версия/условия, шаги, expected и actual result, минимальный check и evidence. В `scenarios/defect-report.md` проблема: дефектная версия считает `done`-задачу active и отклоняет повторное название. Current stable suite уже содержит guard `test_title_can_be_reused_after_task_is_done` и сейчас дает `11 passed`; значит fixture классифицируется как документированный historical functional defect с текущим passing regression guard, а не как наблюдаемый failure текущего стенда.

Regression scope выбирается по измененному правилу и соседним инвариантам. Для duplicate/status change обязательны: active duplicate rejection, `done` title reuse, status transition, ID sequence и list order. Можно начать focused tests для диагностики, но release evidence для стенда использует полный stable suite. Если scope неизвестен, matrix должна показать gap и gate возвращает STOP.

### Flaky classification

`scenarios/flaky-run.log` содержит три неизмененных запуска исторического набора из пяти tests: `5 passed`, затем `4 passed, 1 failed` с `id=2` вместо `id=1`, затем `5 passed`. Это flaky evidence: outcome меняется при той же command/source. Точная причина не доказана; гипотеза - shared `TaskService` state или ID counter. Правильный triage сохраняет все runs, повторяет command без изменения inputs, проверяет isolation test и поиск global state, а затем назначает owner. Retry не превращает flaky в pass.

### Severity, priority и release decision

Severity описывает влияние при наличии дефекта: для stale active duplicate пользователь не может создать допустимую новую задачу, но может выбрать другое название, поэтому допустима предварительная оценка `medium`; она должна быть пересмотрена по продуктовым последствиям. Priority - порядок исправления и определяется owner-ом с учетом release, клиентов и срока, поэтому не выводится только из severity. Release gate не «складывает» числа: он требует traceability, deterministic evidence, known-defect decision, flaky status, risk/rollback и named approver. Отсутствие любого обязательного поля означает `STOP`.

## Ключевые термины

- **Defect** - подтвержденное отклонение actual result от согласованного expected result.
- **Reproduction** - минимальные повторяемые шаги, показывающие дефект.
- **Regression scope** - набор checks для измененного поведения и его инвариантов.
- **Flaky test** - test/run с нестабильным outcome при неизмененных relevant inputs.
- **Severity** - техническое или пользовательское влияние дефекта.
- **Priority** - согласованный порядок исправления; не равен severity.
- **Release gate** - проверяемое правило `go`/`STOP` перед выпуском.
- **Rollback** - план безопасного возврата при неуспешном выпуске.

## Рабочий пример

```md
# Release gate: TaskService

## Traceability
- Есть `traceability-matrix.md`; все high-risk conditions имеют source, check и observed evidence.

## Defect triage
- `defect-report.md`: historical functional defect; current guard
  `test_title_can_be_reused_after_task_is_done` green in 11-test suite.
- Severity: preliminary medium; Priority: Product owner decision, unknown now.

## Flaky triage
- `flaky-run.log`: flaky, 1 failure of 3 unchanged historical runs; root cause unknown.
- Owner: QA/SDET for isolation evidence, implementation through coordinator for confirmed correction.

## Decision
- STOP: release traceability absent, flaky impact unclassified, or risk/rollback/approver missing.
- Candidate go: QA/SDET evidence complete -> coordinator completeness check ->
  risk reviewer decision for release risk -> human owner final acceptance.
```

### Подготовленный ответ агента без API-ключа

```text
Verdict: STOP, not ready for release decision.
Причина: defect fixture классифицирован, но отсутствует traceability matrix с
source-to-check evidence; flaky log показывает instability и не подтверждает
root cause. QA/SDET передает три raw run и stable 11-test result coordinator-у.
Coordinator запрашивает bounded isolation triage. Risk reviewer не получает
approval request до evidence, impact, rollback и human owner. Нельзя заменить
этот STOP повторным green run.
```

Это prepared verdict. Текущий локальный run нужно выполнить и зафиксировать отдельно; fixture не является live failure этого стенда.

## Практика

1. Создайте `artifacts/module-05/triage-and-release-gate.md` по `templates/review-gate.md` и дополните release criteria.
2. Внесите defect reproduction из `scenarios/defect-report.md`: conditions, steps, expected, actual, separate test snippet и classification `historical functional defect`.
3. Укажите, что `test_title_can_be_reused_after_task_is_done` - current regression guard, а baseline full suite ожидает `11 passed`.
4. Внесите три exact outcomes из `scenarios/flaky-run.log`, classification `flaky`, unknown root cause и hypothesis about shared state; не называйте гипотезу фактом.
5. Сформируйте regression scope для duplicate/status change: active duplicate, done reuse, status, ID sequence, list order и unknown ID. Обоснуйте каждый risk.
6. Отделите severity (предварительное влияние) от priority (решение Product owner). Добавьте known defect disposition, rollback limits, human owner и approval route.
7. Сделайте release rule: без traceability matrix, real command/output, defect/flaky disposition, impact/rollback и decision owner - только `STOP`.

### Необязательный prompt для живого агента

```text
Прочитай только defect-report.md, flaky-run.log, requirements.md,
tests/test_service.py, agents/qa-sdet.md и agents/risk-reviewer.md. Не меняй
стенд, не retry ради green, не release/deploy/commit/push. Верни defect/flaky
classification, regression scope, severity отдельно от priority, evidence gaps,
owner/receiver и release gate. Release без traceability matrix должен быть STOP.
```

## Проверка результата

```bash
test -f artifacts/module-05/triage-and-release-gate.md
for term in "defect-report.md" "flaky-run.log" "historical functional defect" \
  "flaky" "root cause unknown" "severity" "priority" "regression scope" \
  "traceability" "rollback" "risk reviewer" "human owner" "STOP"; do
  grep -qi "$term" artifacts/module-05/triage-and-release-gate.md || exit 1
done
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
# Текущее ожидаемое наблюдение неизмененного стенда: 11 passed.
```

Наблюдаемые критерии: fixture defect и flaky не смешаны; root cause flaky помечен unknown; regression scope связан с риском; severity не выдается за priority; release без traceability получает STOP. При несовпадении stable command и `11 passed` сохраните output, укажите failed node, не разрешайте release и передайте QA/SDET package coordinator-у.

Локальный маршрут исправления: если defect не содержит expected/actual/steps, вернитесь только к `defect-report.md` и дополните пакет. Если flaky записан как confirmed defect, замените verdict на `flaky`, сохраните runs и назначьте isolation check. Если priority придумана, оставьте `unknown` и запросите Product owner. Если release gate не находит matrix, добавьте STOP и receiver вместо условного `go`.

## Типичные ошибки

- **Исторический defect fixture выдан за current failure.** Исправление: назовите current guard и реальный output stable suite.
- **Flaky устраняется повторным запуском.** Исправление: храните все outcomes и расследуйте изоляцию.
- **Severity автоматически задает priority.** Исправление: сохраните отдельное owner decision.
- **Full suite заменен только focused test.** Исправление: для release повторите stable full command.
- **Release объявлен при отсутствующей traceability.** Исправление: verdict только STOP с missing evidence и receiver.

## Контрольные вопросы

1. Почему defect fixture не доказывает current regression сам по себе?
2. Какие три факта в flaky log делают его flaky evidence?
3. Почему hypothesis shared state нельзя назвать root cause?
4. Чем severity отличается от priority?
5. Какие условия release gate обязательны до decision о выпуске?

## Официальные источники

- [pytest documentation](https://docs.pytest.org/) - официальный источник запуска, collection и report tests; конкретные fixtures и expected count локальны.
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) - официальный источник API-contract terminology; release criteria курса сформулированы внутри репозитория.
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) - официальный источник risk-management context; конкретные роли и routing определены contracts курса.
