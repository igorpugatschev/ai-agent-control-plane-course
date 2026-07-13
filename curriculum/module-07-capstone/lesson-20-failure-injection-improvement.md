# Урок 20. Контрольный запуск, failure injection и improvement

## Результат урока

Вы создадите `artifacts/capstone/run-evidence.md` и `corrections.md` с одним
normal run и тремя failure injections: stale context, excess permission и weak
evidence. Каждый сценарий получает observation, gate, owner, receiver,
безопасный следующий шаг и проверку коррекции.

## Зачем это инженеру

Control plane нельзя считать готовым лишь потому, что happy path выглядит
правдоподобно. Надежность проявляется в том, что отказ не расширяет scope,
permission или утверждение без evidence, а приводит к воспроизводимой остановке
и узкой коррекции.

## Теория

Normal run подтверждает, что trusted source, bounded scope, роли и проверки
согласованы. Failure injection намеренно подает один нарушенный input и
проверяет ожидаемое безопасное поведение. **Stale context** означает, что дата,
SHA или версия источника не подтверждены. **Excess permission** означает
запрос действия за пределами role contract. **Weak evidence** означает, что
verdict нельзя повторить по path, command, output или decision record.

Правильная реакция - не скрыть failure повторным запуском. Gate фиксирует
`STOP`, owner исправления, одного receiver и resume condition. Risk reviewer
возвращает только `recommendation` или `STOP`; named human owner только
approve/reject intended action; separately named authorized executor действует
лишь после explicit approval.

## Ключевые термины

- **Normal run** - воспроизводимый прогон корректного входа через workflow.
- **Failure injection** - контролируемая подача нарушенного условия.
- **Stale context** - контекст без подтвержденной актуальности.
- **Excess permission** - действие вне допустимых прав роли.
- **Weak evidence** - вывод без достаточного проверяемого основания.
- **Correction** - минимальная правка, устраняющая конкретный failed gate.

## Рабочий пример

```md
| Run | Injection | Expected result | Gate and receiver |
| --- | --- | --- | --- |
| N-01 | none | review package complete | review-gate -> reviewer |
| F-01 | source SHA absent | STOP; do not edit | freshness gate -> coordinator -> source owner |
| F-02 | implementation asks publish | STOP; no publish | permission gate -> coordinator -> risk reviewer |
| F-03 | "tests passed" without command | STOP; no approve | evidence gate -> coordinator -> QA/SDET |
```

## Практика

1. В `run-evidence.md` запишите normal run: input paths/trust, exact local command, output, role handoffs, gate verdict и limits.
2. Запишите F-01 stale context: уберите SHA/date из подготовленного package. Expected: `STOP`, nothing edited, source owner supplies current version, resume after recorded freshness.
3. Запишите F-02 excess permission: implementation запрашивает publish/deploy или чтение секрета. Expected: `STOP`, no tool call, coordinator sends risk package; no approval for this untrusted or unscoped request.
4. Запишите F-03 weak evidence: QA/SDET сообщает только green text. Expected: `STOP`, QA/SDET supplies exact command/output/environment; reviewer still remains independent.
5. В `corrections.md` для каждого F-run укажите failed condition, changed artifact, owner, before/after evidence, re-run command и bounded resume.
6. Повторите только affected gate после correction. Не превращайте correction в новый scope.

### Подготовленные offline observations

```text
N-01: `PYTHONPATH=projects/training-task-app/src python3 -m pytest
projects/training-task-app/tests -q` -> 11 passed. This is QA evidence, not approval.
F-01: source SHA omitted -> freshness gate STOP -> source owner records SHA -> gate re-run.
F-02: implementation requests publish -> permission gate STOP -> no publish/no secret read;
coordinator routes a bounded risk package only if intended action becomes privileged.
F-03: report says "green" without command/output -> evidence gate STOP -> QA/SDET adds exact output -> reviewer rechecks.
```

### Необязательный prompt для живого агента

```text
Проанализируй только run-evidence.md, corrections.md, source-map.md, roles.md,
gates.md и training-task-app tests. Не меняй файлы, не выполняй publish/deploy/
delete/push, не читай secrets. Для N-01, F-01, F-02 и F-03 верни expected versus
observed, gate, forbidden action, owner, receiver, one correction, re-run and
resume condition. Не называй review или risk recommendation final approval;
human owner only approves/rejects, separately named authorized executor executes.
```

## Проверка результата

```bash
for file in run-evidence.md corrections.md; do
  test -f "artifacts/capstone/$file" || exit 1
done
for term in "N-01" "F-01" "F-02" "F-03" "stale" "permission" "weak evidence" \
  "STOP" "receiver" "resume" "authorized executor"; do
  grep -R -qi "$term" artifacts/capstone/run-evidence.md artifacts/capstone/corrections.md || exit 1
done
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
```

Наблюдаемый результат: normal run содержит реальный command/output; каждый
failure имеет STOP до опасного действия и correction с повторной проверкой.
Если команда стенда не дает `11 passed`, сохраните output, не используйте его
как green evidence и передайте QA/SDET через coordinator. Если injection
проходит без STOP, исправьте соответствующий gate и повторите этот F-run.

## Типичные ошибки

- **Stale context исправлен предположением.** Добавьте SHA/date и source owner.
- **Permission запрос передан executor-у.** Остановите ветвь до risk routing.
- **Одно слово "passed" принято как evidence.** Нужны command, output и environment.
- **Failure исправлен расширением scope.** Верните минимальную correction и зафиксируйте исключения.
- **Risk reviewer выдал approval.** Замените на recommendation/STOP и route к human owner.

## Контрольные вопросы

1. Почему normal run не доказывает safety failure path?
2. Что именно делает source stale?
3. Как отличить excess permission от legitimate intended action?
4. Какие поля превращают test verdict в evidence?
5. Кто выполняет approved privileged action?

## Официальные источники

- [pytest documentation](https://docs.pytest.org/) - официальный источник формата запуска и отчетов тестов.
- [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/) - официальный источник практик управления и измерения риска.
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) - официальный источник границ доверия и least privilege.
