# Reference control plane: maintenance of product documentation

Этот completed reference показывает control plane для сопровождения product
documentation после подтвержденного change request. Это не `training-task-app`
и не готовое решение capstone: домен - сверка release documentation с
утвержденным source change, а output - local documentation review package.

## Что показывает пример

[`control-plane.yaml`](control-plane.yaml) содержит complete machine-readable
контракт: цель/scope, trusted и untrusted context, roles, workflow, gates,
evidence и risks. [`decision-log.md`](decision-log.md) фиксирует выбор
reversible local review вместо автоматической публикации. YAML использует
только maps, lists и quoted strings, поэтому валиден для стандартного YAML
parser; Markdown ниже объясняет, почему каждое поле нужно control plane.

## Context and scope

Trusted change request и versioned documentation index определяют intended
action: подготовить локальный diff и review package. Feedback from an external
comment form остается untrusted data: он может указать на ошибку, но не меняет
scope, permissions или publish route. В scope входит Markdown в `docs/product/`;
исключены product code, release publishing, secrets and customer data.

## Roles and workflow

Coordinator проверяет completeness и выбирает одного receiver. Documentation
implementer меняет только approved Markdown. Reviewer независимо сопоставляет
diff и change request. QA/SDET запускает link/structure checks и передает raw
evidence. Risk reviewer возвращает `recommendation` или `STOP` для privileged
route. Named human owner only approves/rejects an intended publish action;
separately named authorized executor publishes only an explicit approval.

Workflow: intake -> source freshness -> local edit -> QA evidence -> review ->
coordinator. При publish request добавляется risk analysis -> human decision ->
authorized execution. При stale source, excess permission or weak evidence
workflow останавливается, фиксирует receiver и resume condition.

## Gates and evidence

Freshness gate требует source revision; permission gate запрещает publish и
secret access implementer-у; evidence gate требует exact command/output and
independent review. Reference evidence is a stable local example, not a claim
that these paths exist in every student repository. Student substitutes own
paths and commands, not copy-pastes verdicts.

## Local inspection

```bash
python3 -c "import yaml, pathlib; print(yaml.safe_load(pathlib.Path('projects/reference-control-plane/control-plane.yaml').read_text(encoding='utf-8'))['schema_version'])"
git diff --check
```

If PyYAML is unavailable, parse in a local environment with a YAML parser; do
not replace the contract with ad hoc string parsing. The reference itself has
no paid service or live-agent prerequisite.
