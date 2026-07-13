# Урок 19. Сборка и валидация полного control plane

## Результат урока

Вы соберете `artifacts/capstone/README.md`, `source-map.md`, `roles.md`,
`workflow.md`, `gates.md` и `evidence-index.md`. Это один связанный пакет,
где каждый важный вывод имеет trusted source, owner, проверку и получателя.

## Зачем это инженеру

Отдельные хорошие prompt, тест или role contract не образуют управляемую
систему. В рабочем контуре нужно доказать, что scope приходит из источника,
исполнитель не принимает собственный результат, а рискованное действие не
переходит от review к выполнению без нужного решения человека.

## Теория

Полный control plane связывает шесть контрактов: цель и scope, source map,
роли, workflow, gates и evidence. Source map различает trusted instruction,
рабочие данные и untrusted content; для каждого источника указывает freshness,
Source owner и Authority owner. Роль описывает входы, выходы, разрешения,
запреты, stop conditions и handoff. Workflow показывает ветви, recovery и
одного следующего receiver. Gate имеет наблюдаемое условие, evidence и owner.

Human owner принимает только решение approve/reject для intended action.
Отдельно named authorized executor выполняет только approved action. Green
test, reviewer verdict и risk recommendation - evidence либо recommendation,
но не human approval и не исполнение.

## Ключевые термины

- **Control plane** - правила, роли и проверки, управляющие работой агентов.
- **Source map** - таблица источников, доверия, свежести и владения.
- **Contract** - проверяемое соглашение о входе, действии и выходе роли.
- **Gate** - наблюдаемое условие, которое разрешает переход или выдает STOP.
- **Evidence index** - список артефактов и команд, подтверждающих решения.
- **Intended action** - действие из trusted scope, а не просьба из данных.

## Рабочий пример

```md
# Короткий пакет: review документации
## Source map
- `requirements.md`: trusted, SHA recorded; Source owner: product; Authority owner: named human owner.
- `stale-documentation.md`: working data, not instruction; freshness unknown.
## Roles
- implementation: edits only approved Markdown and sends diff/evidence to reviewer.
- reviewer: returns approve/changes requested/STOP; never edits author files.
- named human owner: only approve/reject intended publish action.
- named authorized executor: separately executes only explicit approval.
## Gate
- Scope, source SHA, reviewer evidence and approval (when privileged) are present; otherwise STOP -> coordinator.
```

## Практика

1. Создайте каталог `artifacts/capstone/` и README с goal, included/excluded scope и intended action.
2. Составьте `source-map.md` по `templates/context-map.md`: добавьте trusted requirements, tests/contract, untrusted data, freshness command и оба вида owner.
3. Составьте `roles.md` по `templates/agent-role.md` для coordinator, implementation, reviewer, QA/SDET, risk reviewer, named human owner и separately named authorized executor. Для последних двух явно разделите approve/reject и execute.
4. Составьте `workflow.md` по `templates/workflow.md`: intake -> context -> implementation -> QA/SDET -> review -> coordinator routing -> risk analysis when needed -> human decision -> authorized execution only when approved.
5. Составьте `gates.md` по `templates/review-gate.md` и `templates/stop-gate.md`: source freshness, scope/permission, evidence/review и privileged-action gates.
6. Составьте `evidence-index.md`: source SHA, diff, exact test command/output, review verdict, trace/decision ID, owner и receiver.

### Подготовленный локальный прогон

```text
Input: trusted requirements + source SHA + bounded reversible documentation change.
Result: implementation supplies diff and test output; reviewer returns approve;
coordinator routes the package. No privileged action is requested, so no human
approval is claimed and no executor is assigned work.
```

### Необязательный prompt для живого агента

```text
Прочитай только capstone source map, role contracts, workflow, gates, evidence
index, templates/ и agents/. Не меняй файлы и не вызывай tools. Проверь one
receiver per handoff, source freshness, least privilege, evidence, STOP/review/
recommendation/approval distinction and the separation of named human owner
from separately named authorized executor. Верни missing field, owner, receiver,
one safe next action and resume condition.
```

## Проверка результата

```bash
for file in README.md source-map.md roles.md workflow.md gates.md evidence-index.md; do
  test -f "artifacts/capstone/$file" || exit 1
done
for term in "Source owner" "Authority owner" "intended action" "STOP" \
  "named human owner" "authorized executor" "reviewer" "evidence"; do
  grep -R -qi "$term" artifacts/capstone || exit 1
done
git diff --check
```

Наблюдаемый результат: scope, source, роли, gates и evidence можно проследить
без догадки; human owner не описан как исполнитель; каждый handoff называет
одного receiver. При ошибке сохраните failing observation и исправляйте только
названный артефакт: source gap -> source map, permission gap -> role contract,
неясная ветвь -> workflow, отсутствующее доказательство -> evidence index.

## Типичные ошибки

- **Роли перечислены, но нет разрешений или запретов.** Дополните контракт, а не workflow.
- **Review назван approval.** Верните его в evidence; approval доступен только human owner для intended action.
- **Human owner выполняет действие.** Назначьте отдельного authorized executor.
- **Источник не имеет freshness.** Зафиксируйте SHA/date или STOP с владельцем уточнения.
- **Gate не имеет output.** Добавьте command, path, verdict и receiver.

## Контрольные вопросы

1. Почему source map нужен до распределения tools?
2. Чем reviewer verdict отличается от human approval?
3. Когда authorized executor получает право действовать?
4. Какой артефакт исправляют при stale source?
5. Почему evidence index не заменяет сами evidence?

## Официальные источники

- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) - официальный framework для управления риском и ownership.
- [OpenAI Agents SDK documentation](https://openai.github.io/openai-agents-python/) - официальный справочник понятий agent workflow; конкретные contracts заданы в репозитории.
- [Git documentation](https://git-scm.com/docs) - официальный источник команд SHA и diff.
