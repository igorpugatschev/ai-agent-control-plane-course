# Reference control plane: maintenance of product documentation

Этот completed reference показывает self-contained control plane для
сопровождения product documentation после подтвержденного change request. Это
не `training-task-app` и не готовое решение capstone: домен - сверка release
documentation с утвержденным source change, а output - local documentation
review package.

## Что содержит пример

[`control-plane.yaml`](control-plane.yaml) - complete machine-readable contract:
цель/scope, trusted и untrusted context, roles, workflow, gates, evidence и
risks. Файл написан как JSON-compatible YAML: расширение `.yaml` остается
валидным YAML, а Python standard library `json` может разобрать его без PyYAML.

Все paths из contract существуют локально: change request, documentation index,
review guide и untrusted external comment находятся в `docs/` и `incoming/`.
[`evidence/CR-42-local-check.txt`](evidence/CR-42-local-check.txt) - committed
local evidence, [`review/CR-42-local-review.md`](review/CR-42-local-review.md) -
committed independent review record, а [`decision-log.md`](decision-log.md)
фиксирует решение подготовить reversible review package до любого publish.

## Context, roles and workflow

Trusted CR-42 и versioned documentation index определяют intended action:
подготовить локальный diff и review package. External comment остается untrusted
data: он может указать на discrepancy, но не меняет scope, permissions или
publish route. В scope входит Markdown в `docs/product/`; исключены product
code, publishing, secrets and customer data.

Coordinator проверяет completeness и выбирает одного receiver. Documentation
implementer меняет только approved Markdown. Reviewer независимо сопоставляет
diff, change request и evidence. QA/SDET владеет reproducible local check.
Risk reviewer возвращает `recommendation` или `STOP`. Named human owner only
approves/rejects intended publish action; separately named authorized executor
публикует только explicit approval.

## Local re-run

Запускайте команды из корня course repository. Они используют только Python
standard library и локальные files; network/API access не нужен.

```bash
python3 projects/reference-control-plane/scripts/check_reference_control_plane.py
python3 -c "import json, pathlib; print(json.loads(pathlib.Path('projects/reference-control-plane/control-plane.yaml').read_text(encoding='utf-8'))['schema_version'])"
git diff --check
```

Expected output первых двух команд:

```text
Reference control plane check: PASS
1
```

Checker validates the JSON-compatible contract, fixture paths and content,
human-owner/executor separation, workflow/gates, committed check evidence and
independent review record. It does not publish, call an API, inspect secrets or
claim that an external rendered site was verified.
