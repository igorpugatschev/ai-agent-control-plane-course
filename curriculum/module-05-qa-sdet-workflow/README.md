# Модуль 5. Workflow QA/SDET: проверяемость, triage и release gate

Модуль продолжает единый control plane на учебном `TaskService`. Вместо вывода «тесты прошли» студент связывает источник требования, проверяемое условие, тест, наблюдение, дефект и решение о выпуске. QA/SDET владеет воспроизводимым evidence, но не final acceptance и не approval выпуска.

К концу модуля вы создадите три связанных артефакта и пройдёте checkpoint:

1. [От требований к проверяемым условиям](lesson-13-requirements-to-checks.md) - `artifacts/module-05/traceability-matrix.md`.
2. [API/UI automation и тестовые агенты](lesson-14-api-ui-test-agents.md) - `artifacts/module-05/test-agent-workflow.md`.
3. [Регрессия, triage и release gate](lesson-15-regression-triage-release-gate.md) - `artifacts/module-05/triage-and-release-gate.md`.
4. [Checkpoint 5](checkpoint.md) - интеграция трассировки, defect/flaky evidence и решения о выпуске.

## Обязательный локальный маршрут

Сначала прочитайте локальные `requirements.md`, `api/openapi.yaml`, `tests/test_service.py`, `scenarios/defect-report.md` и `scenarios/flaky-run.log` внутри `projects/training-task-app/`. Затем используйте contracts [QA/SDET](../../agents/qa-sdet.md), [risk reviewer](../../agents/risk-reviewer.md), [workflow](../../templates/workflow.md), [review-gate](../../templates/review-gate.md) и [handoff](../../templates/handoff.md).

Обязательный маршрут полностью локальный и не требует API-ключа. В каждом уроке есть prepared output, точные пути, проверка и correction route. Live prompt допустим только после offline-практики: он создаёт черновик, а не evidence, permission, approval или release decision.

## Готовность модуля

Модуль завершен, если:

- каждое release-relevant условие связано с локальным источником, тестом и наблюдаемым результатом;
- API-contract и service checks различены, а UI automation осознанно оставлена необязательным расширением без HTTP/UI-стенда;
- defect отделен от flaky evidence, причина flaky не угадывается, regression scope обоснован риском;
- точная команда ниже повторена и зафиксирована с текущим наблюдением `11 passed`;
- QA/SDET передает evidence coordinator-у, а release без traceability получает `STOP`.

```bash
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
```
