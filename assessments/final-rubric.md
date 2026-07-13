# Final capstone rubric

Оценивайте capstone по artifacts и воспроизводимым runs, не по объему prose.
Каждое направление получает 0-3. Зачет: **>= 11/15**, без нулей, passed safety checkpoint,
reproducible N-01 run и risk report `risk-report.md`. Critical defect означает
`requires remediation` независимо от суммы.

| Направление | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Архитектура control plane | Нет package | Документы разрознены | Scope, sources, roles и workflow связаны | Contracts, gates и evidence index дают audit trail |
| Контекст и evidence | Claims без sources | Sources без trust/freshness | Source map, SHA/date и commands видимы | Owners, outputs и decisions независимы проверяемы |
| Роли и workflow | Роли смешаны | Нет handoff/recovery | One receiver и branches есть | Separation, recovery и ownership доказаны runs |
| Gates, safety и observability | Рискованное действие продолжается | STOP без evidence/resume | F-01/F-02/F-03 остановлены и traced | STOP/review/recommendation/approval/execution раздельны, trace redacted |
| Воспроизводимость и документация | Нет local check | Только narrative | Prepared runs, corrections и report есть | Re-run, remediation, residual risk, theory и roadmap согласованы |

## Safety checkpoint

Проверьте: untrusted input не дает command/permission/approval; F-02 останавливается
до tool action; named human owner только approves/rejects intended action;
authorized executor отдельный и действует после explicit approval. Любой
отрицательный ответ - critical defect.

## Reproducible run и risk report

`run-evidence.md` содержит N-01 command, environment, output, verdict и
independent review. `risk-report.md` содержит source/trust, impact, control,
residual risk, owner, receiver и revisit condition. Слово `passed` без
command/output - не evidence.

## Critical defects

- execution from untrusted input, privilege expansion или action до gate;
- confusion review/recommendation/test verdict с human approval;
- merged human owner, risk reviewer и authorized executor;
- missing source/trust, evidence, owner/receiver или resume condition for failure;
- future extension представлена как remediation current core failure.
