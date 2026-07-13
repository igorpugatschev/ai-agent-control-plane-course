# Урок 12. Diff, documentation, review и commit evidence

## Результат урока

Вы соберете `artifacts/module-04/change-review-gate.md` по `templates/review-gate.md`: independent review priority change с diff, tests, documentation sync, verdict и commit handoff.

## Зачем это инженеру

Фраза «тесты прошли» не показывает, какие файлы изменены, совпадает ли API с требованиями и кто проверил автора. Commit без review превращает историю Git в утверждение без evidence. Reviewer не должен исправлять чужой diff, иначе независимость пропадает.

Gate связывает change brief с фактической работой. Implementation предоставляет evidence автора; reviewer повторно проверяет scope, diff и command; coordinator маршрутизирует verdict. Commit отдельный после `approve`, а не награда за green pytest. Push и final acceptance вне урока.

## Теория

### Evidence implementation

Implementation передает approved scope, changed и untouched paths, `git diff --check`, точную pytest command и output, документационную сверку, текущий SHA и ограничения. Для priority allowed paths: `models.py`, `service.py`, `test_service.py`, `requirements.md`, `README.md`, `api/openapi.yaml`. Untouched: `complete_task`, список, duplicate-title и endpoints.

### Independent review

Reviewer применяет `templates/review-gate.md`, читает change brief, сравнивает diff с acceptance, повторяет command и сверяет docs/OpenAPI. Verdict только `approve`, `changes requested` или `STOP`. Finding содержит путь, наблюдение, риск и receiver correction. Reviewer не редактирует diff; implementation не self-approves.

### Commit и routing

При `approve` coordinator готовит commit handoff с SHA, message и reviewer evidence. Учебное сообщение: `feat: add task priority`. При `changes requested` receiver только implementation, а revision ограничена finding. При неполном scope/evidence coordinator возвращает STOP. Commit evidence не разрешает push, release или final acceptance.

## Ключевые термины

- **Diff evidence** - проверяемый список фактических правок.
- **Documentation sync** - совпадение requirements, README и OpenAPI с поведением.
- **Review gate** - независимый переход с criteria, evidence и verdict.
- **Verdict** - `approve`, `changes requested` или `STOP`.
- **Commit evidence** - SHA, message и review evidence после commit.
- **Self-approval** - author принимает собственный результат; это запрещено.
- **Receiver correction** - роль, получающая только named исправление.

## Рабочий пример

```md
# Review-gate: priority change

## Объект review
- Diff только для models.py, service.py, test_service.py, requirements.md,
  README.md и api/openapi.yaml.

## Evidence автора
- `git diff --check` -> exit 0.
- `PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q` -> expected learner evidence after implementing priority and adding three tests: `14 passed`; this is not the observed baseline. Current baseline: `11 passed`.

## Проверки reviewer-а
- Повторить command; сверить diff, API schema и документы с change brief.

## Решение
- changes requested: api/openapi.yaml не описывает default normal.

## Findings
- Путь: `projects/training-task-app/api/openapi.yaml`; риск: клиент не видит default;
  receiver: implementation; bounded revision: описать только priority default.
```

### Подготовленный ответ агента без API-ключа

```text
Verdict: changes requested. Tests green, но OpenAPI содержит только enum и не
сообщает default normal. Implementation меняет только api/openapi.yaml, затем
повторяет pytest и diff check. Reviewer не редактирует YAML; implementation не
approve и не commit. Coordinator получает повторный package после revision.
```

Это prepared review, а не verdict для будущего diff: finding нужно проверить по локальным путям.

## Практика

1. Создайте `artifacts/module-04/change-review-gate.md` по `templates/review-gate.md`.
2. Внесите object, criteria и раздельные `Evidence автора`/`Проверки reviewer-а`.
3. Назовите шесть allowed paths и protected behavior: list order, `complete_task`, duplicate-title, отсутствие endpoints.
4. Добавьте `git diff --check`, pytest command, expected `14 passed`, SHA placeholder и planned message `feat: add task priority`.
5. Запишите finding из примера и bounded correction только для `api/openapi.yaml`; reviewer повторяет проверку.
6. Завершите handoff: reviewer -> coordinator при approve; coordinator -> implementation при correction. Запретите self-approval, push и final acceptance.

### Необязательный prompt для живого агента

```text
Проверь только change brief, controlled change plan и предполагаемый priority
diff. Не меняй файлы, не commit, не push и не утверждай результат. Верни gate:
scope comparison, evidence автора, независимые проверки, verdict, findings с
путем/риском/receiver и STOP при отсутствии diff или output. Проверь models.py,
service.py, test_service.py, requirements.md, README.md и api/openapi.yaml;
list_tasks, complete_task, duplicate-title и endpoints вне diff.
```

## Проверка результата

```bash
test -f artifacts/module-04/change-review-gate.md
for term in "Evidence автора" "Проверки reviewer-а" "git diff --check" "14 passed" \
  "changes requested" "api/openapi.yaml" "implementation" "self-approval"; do
  grep -qi "$term" artifacts/module-04/change-review-gate.md || exit 1
done
git diff --check
```

Наблюдаемые критерии: author evidence и reviewer checks разделены; finding имеет путь, риск и receiver; commit требует approve; push/final acceptance запрещены. При лишнем файле verdict - `changes requested` или STOP, затем bounded revision.

## Типичные ошибки

- **Green tests названы approve.** Оставьте их в evidence автора и выполните review.
- **Reviewer правит YAML.** Запишите finding и верните implementation.
- **README синхронен, OpenAPI нет.** Ограничьте correction схемой и повторите gate.
- **Commit смешан с push.** Назовите commit handoff отдельно; push требует другого approval.

## Контрольные вопросы

1. Какие evidence передает implementation?
2. Почему reviewer повторяет command автора?
3. Когда допустим changes requested при green tests?
4. Кто получает correction?
5. Почему commit SHA не final acceptance?

## Официальные источники

- [Git documentation](https://git-scm.com/docs) - официальный справочник commit и diff; approval/routing заданы в уроке.
- [pytest documentation](https://docs.pytest.org/) - официальный источник test command; expected output локален.
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) - официальный источник API schema; review сверяет локальный YAML с brief.
