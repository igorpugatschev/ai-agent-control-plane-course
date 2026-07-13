# Task 10 implementer report

## Status

Completed: capstone projects are self-contained and re-runnable without network,
API, or PyYAML.

## Delivered

- Converted both `control-plane.yaml` files to JSON-compatible YAML so Python
  standard library `json` parses them.
- Added the reference documentation-maintenance fixtures, stdlib checker,
  committed local evidence, and independent review record.
- Added the exact ten-template mapping to lesson 19, starter, capstone,
  checkpoint, and audit acceptance; `control-plane.yaml` is required.
- Added placeholder-only starter artifacts for every mapped deliverable plus
  evidence, failure, risk, and defense records.
- Added regression tests for the reference local check and complete mapping.

## Final fixes

- Made the capstone verification cwd explicit in `projects/capstone.md` and
  Module 7 checkpoint 7: repository-root commands run from the course
  repository root, while student `control-plane.yaml` and `artifacts/capstone/`
  remain inside the starter/capstone directory.
- Defined one canonical ten-entry template-to-artifact mapping in
  `tests/test_course_assets.py` and asserted parsed starter
  `control-plane.yaml.template_mapping` equals it exactly.
- Added regression coverage for both root-cwd markers, all documented root
  commands, and their execution from the repository root.

## Verification

- `python3 projects/reference-control-plane/scripts/check_reference_control_plane.py`
  -> `Reference control plane check: PASS`
- `python3 scripts/validate_course.py curriculum` -> `Курс проверен: ошибок нет`
- `python3 -m pytest tests/test_course_assets.py -q` -> `7 passed`
- `python3 -m pytest tests/test_course_structure.py -q` -> `3 passed`
- `PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q`
  -> `11 passed`
- `PYTHONPATH=projects/training-task-app/src python3 -m pytest -q` -> `21 passed`
- Stdlib `json` parse for both `.yaml` files -> `JSON-compatible YAML: PASS`
- `git diff --check` -> clean.

## Concern

The repository-wide pytest command still needs
`PYTHONPATH=projects/training-task-app/src` for the nested training application;
the capstone and checkpoint now document that command from the course
repository root. No network/API dependency or unresolved Task10 blocker
remains.
