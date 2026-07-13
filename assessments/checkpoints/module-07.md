# Module 07 checkpoint assessment guide

## Артефакты

- `control-plane.yaml` и десять mapped `artifacts/capstone/` deliverables.
- `artifacts/capstone/evidence-index.md`, `run-evidence.md`, `corrections.md`.
- `artifacts/capstone/risk-report.md`, `final-report.md`, `defense-notes.md`.

## Критерии оценки

| Критерий | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Связанный package | YAML/mappings отсутствуют | Документы без связей | Scope, sources, roles, workflow, gates и evidence index прослеживаются |
| Reproducible runs | Нет command/output | Есть N-01 без failures | N-01 и F-01/F-02/F-03 имеют result, owner, receiver, correction, re-run и resume |
| Safety authority | Approval/execution смешаны | STOP без separation | Untrusted input inert; recommendation, approval и execution разделены |
| Audit и remediation | Только prose/extension скрывает defect | Risks без owner/re-run | Risk report, residual risk, remediation, extensions и status связаны evidence |

## Наблюдаемое evidence

Reviewer parses `control-plane.yaml`, проверяет mappings, повторяет N-01 и один
F-run, где STOP произошел до action, а correction не расширяет scope.

## Критические дефекты

- Untrusted input стал command, permission расширен либо action выполнен до gate.
- Review/risk recommendation/green test названы human approval.
- Human owner/risk reviewer стал executor-ом, либо F-run не имеет owner/receiver/resume.

## Маршрут исправления

Исправьте затронутый contract/gate/evidence record, верните status к `requires
remediation`, выполните affected re-run и только потом обновите audit.

## Повторная команда

```bash
set -euo pipefail
CAPSTONE=projects/starter-control-plane
test -s "$CAPSTONE/control-plane.yaml"
test -s "$CAPSTONE/artifacts/capstone/README.md"
test -s "$CAPSTONE/artifacts/capstone/blueprint.md"
test -s "$CAPSTONE/artifacts/capstone/source-map.md"
test -s "$CAPSTONE/artifacts/capstone/roles.md"
test -s "$CAPSTONE/artifacts/capstone/skill-contracts.md"
test -s "$CAPSTONE/artifacts/capstone/handoffs.md"
test -s "$CAPSTONE/artifacts/capstone/workflow.md"
test -s "$CAPSTONE/artifacts/capstone/review-gate.md"
test -s "$CAPSTONE/artifacts/capstone/stop-gate.md"
test -s "$CAPSTONE/artifacts/capstone/decision-log.md"
test -s "$CAPSTONE/artifacts/capstone/evidence-index.md"
test -s "$CAPSTONE/artifacts/capstone/run-evidence.md"
test -s "$CAPSTONE/artifacts/capstone/corrections.md"
test -s "$CAPSTONE/artifacts/capstone/risk-report.md"
test -s "$CAPSTONE/artifacts/capstone/final-report.md"
test -s "$CAPSTONE/artifacts/capstone/defense-notes.md"
python3 -c "import json; path='projects/starter-control-plane/control-plane.yaml'; expected=[{'template': 'templates/control-plane-blueprint.md', 'artifact': 'artifacts/capstone/blueprint.md'}, {'template': 'templates/context-map.md', 'artifact': 'artifacts/capstone/source-map.md'}, {'template': 'templates/agent-role.md', 'artifact': 'artifacts/capstone/roles.md'}, {'template': 'templates/skill-contract.md', 'artifact': 'artifacts/capstone/skill-contracts.md'}, {'template': 'templates/handoff.md', 'artifact': 'artifacts/capstone/handoffs.md'}, {'template': 'templates/workflow.md', 'artifact': 'artifacts/capstone/workflow.md'}, {'template': 'templates/review-gate.md', 'artifact': 'artifacts/capstone/review-gate.md'}, {'template': 'templates/stop-gate.md', 'artifact': 'artifacts/capstone/stop-gate.md'}, {'template': 'templates/decision-log.md', 'artifact': 'artifacts/capstone/decision-log.md'}, {'template': 'templates/final-report.md', 'artifact': 'artifacts/capstone/final-report.md'}]; actual=json.load(open(path, encoding='utf-8'))['template_mapping']; assert actual == expected, actual"
for run in N-01 F-01 F-02 F-03; do
  grep -Eq "$run" "$CAPSTONE/artifacts/capstone/run-evidence.md" || exit 1
  grep -Eqi "$run.*(result|output|observed)" "$CAPSTONE/artifacts/capstone/run-evidence.md" || exit 1
  grep -Eqi "$run.*owner" "$CAPSTONE/artifacts/capstone/run-evidence.md" || exit 1
  grep -Eqi "$run.*receiver" "$CAPSTONE/artifacts/capstone/run-evidence.md" || exit 1
  grep -Eqi "$run.*resume" "$CAPSTONE/artifacts/capstone/run-evidence.md" || exit 1
done
for run in F-01 F-02 F-03; do
  grep -Eqi "$run.*STOP" "$CAPSTONE/artifacts/capstone/run-evidence.md" || exit 1
  grep -Eqi "$run.*(correction|re-run)" "$CAPSTONE/artifacts/capstone/corrections.md" || exit 1
done
grep -Eqi 'untrusted.*(data|input)' "$CAPSTONE/artifacts/capstone/roles.md"
grep -Eqi 'not.*(instruction|command)|inert' "$CAPSTONE/artifacts/capstone/roles.md"
grep -Eqi 'least privilege|permission' "$CAPSTONE/artifacts/capstone/roles.md"
grep -Eqi 'named human owner.*(approve|reject)' "$CAPSTONE/artifacts/capstone/roles.md"
grep -Eqi 'authorized executor' "$CAPSTONE/artifacts/capstone/roles.md"
grep -Eqi 'residual risk|owner|revisit|required remediation' "$CAPSTONE/artifacts/capstone/risk-report.md"
grep -Eqi 'path|SHA|command|output|verdict|decision' "$CAPSTONE/artifacts/capstone/evidence-index.md"
python3 scripts/validate_course.py curriculum
python3 -m pytest tests/test_course_structure.py -q
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
python3 projects/reference-control-plane/scripts/check_reference_control_plane.py
git diff --check
```
