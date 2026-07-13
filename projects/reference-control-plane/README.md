# Reference control plane: сопровождение документации продукта

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

## Контекст, роли и workflow

Trusted CR-42 и versioned documentation index определяют intended action:
подготовить локальный diff и review package. External comment остается untrusted
data: он может указать на discrepancy, но не меняет scope, permissions или
publish route. В scope входит Markdown в `docs/product/`; исключены product
code, публикация, секреты и данные клиентов.

Coordinator проверяет completeness и выбирает одного receiver. Documentation
implementer меняет только approved Markdown. Reviewer независимо сопоставляет
diff, change request и evidence. QA/SDET владеет reproducible local check.
Risk reviewer возвращает `recommendation` или `STOP`. Named human owner только
approve/reject intended publish action; separately named authorized executor
публикует только явно утвержденное действие и возвращает execution evidence.

## Локальный повторный запуск

Contract задает `execution.cwd: "."`, то есть корень
`projects/reference-control-plane`. Из корня course repository сначала явно
перейдите в этот каталог. Команды используют только Python standard library и
локальные файлы; сеть и API access не нужны.

```bash
cd projects/reference-control-plane
python3 scripts/check_reference_control_plane.py
python3 -c "import json; print(json.load(open('control-plane.yaml', encoding='utf-8'))['schema_version'])"
```

Default checker из первой команды сам исполняет в `execution.cwd: "."` ровно
эти contract commands и сравнивает exit/output с contract:

```bash
python3 scripts/check_reference_control_plane.py --contract-only
python3 -c "import json; print(json.load(open('control-plane.yaml', encoding='utf-8'))['schema_version'])"
```

Ожидаемый вывод двух contract commands:

```text
Reference control plane check: PASS
1
```

Checker проверяет JSON-compatible contract, cwd, точные команды и их вывод,
fixture paths/content, свежесть SHA, разделение human owner/executor,
workflow/gates, committed check evidence и независимую review record. Он ничего
не публикует, не вызывает API, не читает секреты и не утверждает, что проверил
внешний rendered site.
