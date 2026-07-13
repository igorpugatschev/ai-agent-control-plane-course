# Урок 21. Аудит, защита и roadmap развития

## Результат урока

Основной артефакт: `artifacts/capstone/final-report.md`.
При завершении урока вы также обновите связанные записи
`artifacts/capstone/risk-report.md` и `artifacts/capstone/defense-notes.md`.
Пакет объясняет архитектуру, evidence, четыре прогона, остаточные риски,
обязательные remediation и отдельные будущие extensions.

## Зачем это инженеру

Защита проверяет не красоту диаграммы, а способность владельца объяснить,
почему система действовала или остановилась. Audit делает ограничения видимыми:
что подтверждено локально, что еще не проверено, кто владеет решением и почему
план улучшения не маскирует незакрытый критический риск.

## Теория

Audit проходит по пяти направлениям финальной rubric: архитектура control
plane; контекст и evidence; роли и workflow; gates, безопасность и
observability; воспроизводимость и документация. Каждое направление получает
0-3 балла. Проход требует минимум 11/15, отсутствия нулей, safety checkpoint,
воспроизводимого run и risk report.

**Remediation** обязательна, когда current contract/gate/evidence не дает
выполнить базовое требование или оставляет критический риск. **Extension**
откладывается, когда core уже работает, а улучшение добавляет vendor-specific,
редкий или инфраструктурный сценарий. Extension не может закрыть current STOP.
Theory confirmation самодостаточна: студент объясняет термины и применение по
файлам репозитория, а official sources служат проверкой, а не скрытым условием.

## Ключевые термины

- **Audit** - независимая сверка claims, artifacts и evidence.
- **Defense** - устное или письменное объяснение решений и ограничений.
- **Rubric** - явные критерии и шкала оценки результата.
- **Residual risk** - риск, оставшийся после controls.
- **Remediation** - обязательное исправление failed базового требования.
- **Extension** - необязательное развитие после закрытия базовых gates.

## Рабочий пример

```md
## Risk report excerpt
| Risk | Evidence | Current control | Decision | Owner |
| --- | --- | --- | --- | --- |
| Stale requirement | F-01 STOP | freshness gate + SHA | remediation: require SHA | source owner |
| Publish outside scope | F-02 STOP | permission gate | closed for current run | coordinator |
| No live-agent evaluation | offline prepared runs | disclose limitation | extension: add sandbox evaluation | course owner |
```

## Практика

1. Проведите audit по пяти направлениям rubric и внесите score/3, path и evidence в `defense-notes.md`.
2. В `risk-report.md` укажите risk, source/trust, impact, control, residual risk, owner, receiver и revisit condition.
3. Разделите список на `Required remediation` и `Future extensions`. У remediation добавьте failed gate и re-run; у extension - rationale, но не выдавайте ее за закрытую работу.
4. Создайте `final-report.md` по шаблону: status, result, changed artifacts, commands/output, decision IDs, concerns и next owner.
5. Напишите self-contained theory confirmation: своими словами объясните control plane, trusted/untrusted context, least privilege, gate, evidence, STOP, review, recommendation, human approval и authorized execution; приведите один путь из своих artifacts.
6. Проведите защиту: покажите normal/F-01/F-02/F-03, объясните один STOP, один correction и почему human owner не исполняет действие.

### Template mapping audit acceptance

Audit принимает package только при parsed `control-plane.yaml` и каждом exact
mapping ниже; missing mapped file - remediation, не future extension.

| Mapping | Audit evidence |
| --- | --- |
| `templates/control-plane-blueprint.md` -> `artifacts/capstone/blueprint.md` | цель, scope, gates и evidence |
| `templates/context-map.md` -> `artifacts/capstone/source-map.md` | trust, freshness и owners |
| `templates/agent-role.md` -> `artifacts/capstone/roles.md` | responsibility, rights и separation |
| `templates/skill-contract.md` -> `artifacts/capstone/skill-contracts.md` | repeatable local check |
| `templates/handoff.md` -> `artifacts/capstone/handoffs.md` | one receiver и next action |
| `templates/workflow.md` -> `artifacts/capstone/workflow.md` | branch and recovery |
| `templates/review-gate.md` -> `artifacts/capstone/review-gate.md` | independent verdict |
| `templates/stop-gate.md` -> `artifacts/capstone/stop-gate.md` | STOP and resume condition |
| `templates/decision-log.md` -> `artifacts/capstone/decision-log.md` | owner and revisit condition |
| `templates/final-report.md` -> `artifacts/capstone/final-report.md` | honest status and concerns |

### Подготовленная offline защита

```text
Claim: F-02 did not publish anything. Evidence: run-evidence F-02 and permission
gate record STOP, forbidden tool action, coordinator as receiver and no executor
assignment. Decision: the named human owner was not asked to approve an
unscoped request. Residual risk: live-agent behavior was not measured; this is
an extension only after all offline gates are reproducible.
```

### Необязательный prompt для живого агента

```text
Прочитай только capstone artifacts, checkpoint rubric and templates/final-report.md.
Не меняй файлы и не вызывай tools. Проведи audit: для каждого rubric direction
назови score 0-3, path/evidence, gap, remediation or extension, owner and one
next action. Отдельно проверь, что named human owner only approves/rejects and
separately named authorized executor only executes explicit approval.
```

## Проверка результата

```bash
# Run from the capstone package root.
python3 -c "import json; json.load(open('control-plane.yaml', encoding='utf-8'))"
for file in risk-report.md final-report.md defense-notes.md; do
  test -f "artifacts/capstone/$file" || exit 1
done
for term in "architecture" "context" "roles" "gates" "reproducibility" \
  "Required remediation" "Future extensions" "residual risk" \
  "self-contained theory" "named human owner" "authorized executor"; do
  grep -R -qi "$term" artifacts/capstone || exit 1
done
git diff --check
```

Наблюдаемый результат: defense может показать evidence для каждого score;
обязательная correction имеет owner и re-run; extension не заменяет remediation.
При нулевом score или safety defect статус `requires remediation`: исправьте
указанный contract/gate/evidence, повторите затронутый run и только потом
обновите rubric. При неясном owner вернитесь к roles.md, а не назначайте
исполнителя задним числом.

## Типичные ошибки

- **Risk report повторяет список угроз без owner.** Добавьте impact, control, receiver и revisit condition.
- **Extension закрывает failed core gate.** Переместите ее в remediation с re-run.
- **Источники заменяют объяснение.** Напишите theory confirmation в репозитории.
- **Score не связан с path.** Добавьте artifact и exact command/output.
- **Human owner указан как executor.** Разделите решение и исполнение в contracts и defense.

## Контрольные вопросы

1. Какой дефект переводит capstone в requires remediation?
2. Почему live-agent test может быть extension, а не обязательным маршрутом?
3. Чем residual risk отличается от unaddressed critical risk?
4. Как доказать, что STOP действительно сработал?
5. Почему final report не заменяет decision log?

## Официальные источники

- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) - официальный источник структуры управления AI risks.
- [OWASP GenAI Security Project](https://genai.owasp.org/) - официальный источник security guidance для GenAI systems.
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai) - официальный источник terminology для наблюдаемости; redaction policy остается локальным contract.
