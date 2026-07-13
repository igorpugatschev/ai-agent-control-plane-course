# Checkpoint 5. QA/SDET evidence, triage и release decision

## Что проверяется

Checkpoint проверяет путь `требование -> testable condition -> traceability -> deterministic evidence -> defect/flaky triage -> regression scope -> release gate`. Успех - обоснованный STOP или подготовленный decision package, а не формальное слово `passed`.

Используйте накопленные артефакты:

```text
artifacts/module-02/context-packet.md
artifacts/module-02/context-map-evidence-gate.md
artifacts/module-03/coordinator-handoff.md
artifacts/module-04/change-review-gate.md
artifacts/module-05/traceability-matrix.md
artifacts/module-05/test-agent-workflow.md
artifacts/module-05/triage-and-release-gate.md
```

## Входные данные

Работайте только с repo-relative источниками и contracts:

```text
projects/training-task-app/requirements.md
projects/training-task-app/api/openapi.yaml
projects/training-task-app/tests/test_service.py
projects/training-task-app/scenarios/defect-report.md
projects/training-task-app/scenarios/flaky-run.log
agents/qa-sdet.md
agents/risk-reviewer.md
templates/workflow.md
templates/review-gate.md
templates/handoff.md
```

Учебный стенд не меняйте. Его current stable baseline подтверждается только exact command и в неизмененном состоянии ожидается как `11 passed`.

## Задание

Создайте или исправьте только три Module 5 артефакта.

1. В `traceability-matrix.md` свяжите минимум шесть requirements/API conditions с named tests или schema review, риском и observed evidence. Обязательно разделите Python service checks и HTTP claims.
2. В `test-agent-workflow.md` опишите API schema review, stable command, evidence fields, failure routing, optional Playwright branch и `UI check: not applicable` для текущего стенда.
3. В `triage-and-release-gate.md` классифицируйте exact fixtures ниже, выберите regression scope и подготовьте release gate. Выпуск без traceability matrix обязан завершиться `STOP`.
4. Передайте QA/SDET package coordinator-у. QA/SDET не исправляет стенд, не выдает final acceptance и не делает release/deploy; risk reviewer принимает только документированное decision об approval/reject/STOP после complete risk package.

## Exact fixture classification

### Defect fixture

`projects/training-task-app/scenarios/defect-report.md` - **documentary historical case**, а не pinned defective revision или executable defect fixture. Он документирует утверждение, что после `complete_task` повторное создание того же названия в дефектной версии давало `ValueError`, хотя expected result - новая задача с ID `2`. В current стенде `test_title_can_be_reused_after_task_is_done` уже является regression guard; `11 passed` означает `not reproduced` в current checkout. Evidence package обязан записать `not reproduced`, missing pinned defective revision/fixture и `STOP` с запросом pinned artifact, прежде чем назвать defect reproducible. Не меняйте code или tests, чтобы создать failure; после получения pinned artifact учебные steps и minimal check сохраняют смысл defect reproduction.

### Flaky fixture

`projects/training-task-app/scenarios/flaky-run.log` описывает **flaky evidence**: один и тот же historical пяти-test command дал `5 passed`, затем `4 passed, 1 failed` (`id=2` вместо `id=1`), затем `5 passed`, без изменения command или source. Root cause **unknown**. Shared state/ID counter - гипотеза для isolation check, не доказанный defect. Owner первичного evidence - QA/SDET; confirmed correction получает implementation через coordinator.

## Prepared release input

```text
Release request: "pytest зеленый, выпускайте".
Evidence: только фраза автора, без traceability matrix, без полного command/output,
без defect disposition, без оценки flaky impact, rollback, human owner и approver.
```

Правильная реакция:

```text
Verdict: STOP.
Причина: release-relevant conditions не трассируются от sources к checks и
observed evidence; request не содержит disposition defect/flaky, impact,
rollback, human owner или documented approval route.
Receiver: coordinator.
Следующее действие: запросить у QA/SDET три Module 5 артефакта и actual test
report; после completeness check coordinator направляет risk package risk
reviewer-у, а final product acceptance остается human owner.
Resume condition: complete traceability, deterministic evidence, defect/flaky
decision, risk/rollback и named owners.
```

## Обязательный режим без API-ключа

Prepared input заменяет живую модель. Выполните анализ по локальным fixtures, contracts и templates. Внешняя документация подтверждает термины, но обязательная теория, условия, artifacts, checks и correction route уже находятся в модуле. Сеть, API-ключ и UI не нужны.

## Необязательный режим с живым агентом

```text
Проверь только Module 5 artifacts и локальные requirements, OpenAPI, tests,
defect-report, flaky-run, QA/SDET и risk reviewer contracts. Не меняй файлы,
не retry ради green, не release/deploy/commit/push и не выдавай final acceptance.
Верни source-to-check gaps, exact defect/flaky classification, regression scope,
severity отдельно от priority, release verdict, missing evidence, receiver,
next action и resume condition. Release без traceability обязан быть STOP.
```

## Самопроверка

```bash
for file in traceability-matrix.md test-agent-workflow.md triage-and-release-gate.md; do
  test -f "artifacts/module-05/$file" || exit 1
done
for path in requirements.md api/openapi.yaml tests/test_service.py defect-report.md flaky-run.log; do
  grep -R -q "$path" artifacts/module-05 || exit 1
done
for term in "given" "when" "then" "Observed evidence" "201" "400" "404" \
  "not applicable" "documentary historical case" "not reproduced" \
  "pinned" "root cause unknown" "severity" "priority" "regression scope" \
  "traceability" "STOP"; do
  grep -R -qi "$term" artifacts/module-05 || exit 1
done
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
# Текущее ожидаемое наблюдение неизмененного стенда: 11 passed.
git diff --check
```

Проведите два walkthrough. Нормальный путь: full traceability и deterministic evidence -> coordinator completeness check -> risk reviewer decision при release risk -> human owner final acceptance. Failure path: отсутствует matrix или flaky disposition -> `STOP -> coordinator -> QA/SDET` для bounded evidence package; не выполняйте release.

## Оценивание

Каждый критерий оценивается от 0 до 2.

| Критерий | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Testable conditions и traceability | Нет source/check связи | Есть tests без risk/observation | Условия, source, check, risk, evidence и gaps видимы |
| API/UI workflow | Layers смешаны | Есть command без полного evidence | Schema/service/UI branches и routing воспроизводимы |
| Defect/flaky triage | Fixtures перепутаны | Есть label без facts/owner | Exact classification, runs, unknown cause, scope и owner |
| Release gate | Green назван release | Есть checklist без traceability STOP | Matrix, output, disposition, risk/rollback, owners; missing data -> STOP |

Для зачета нужно не менее 8 из 10 и отсутствие критического дефекта.

## Критические дефекты

- **Release without traceability:** release/go выдан без source-to-check matrix и observed evidence.
- **Fixture confusion:** documentary historical case без pinned artifact назван reproducible/current defect, либо flaky назван confirmed root cause.
- **Unbounded flaky retry:** нестабильность скрыта повторным green run без сохраненных outcomes.
- **Layer confusion:** Python unit test выдан за HTTP endpoint или обязательный UI check выдуман без UI scope.
- **Role violation:** QA/SDET self-approves release, либо risk reviewer/deployer выполняет действие вместо documented decision.
- **Missing deterministic evidence:** нет exact command, environment/exit result или named receiver.

## Локальный маршрут исправления

- release without traceability -> добавьте source, condition, check и observed evidence в `traceability-matrix.md`; верните verdict к STOP и повторите command;
- fixture confusion -> для defect-report запишите documentary historical case, `not reproduced`, missing pinned revision/fixture и STOP/request for pinned artifact; сохраните defect steps или все flaky outcomes, root cause оставьте `unknown`;
- unbounded retry -> внесите неизмененные command/source, каждый run и isolation next action в `triage-and-release-gate.md`;
- layer confusion -> перенесите HTTP claim в schema review, UI в optional branch `not applicable`, пока нет approved scope;
- role violation -> передайте QA/SDET report coordinator-у, approval - risk reviewer-у, final acceptance - human owner;
- failed check -> сохраните output, failed node, source/diff state и failure owner, затем передайте coordinator-у.

## Результат checkpoint

Передайте coordinator три Module 5 артефакта и один verdict. Handoff содержит scope, source paths, exact command/output, schema/UI status, defect/flaky classification, `not reproduced` и missing pinned revision/fixture для documentary historical case, regression scope, release criteria, missing evidence, risk, receiver, одно следующее действие и resume condition. При отсутствующей traceability или pinned artifact итог - `STOP`, а не release.
