# Журнал решений: reference documentation maintenance control plane

## 2026-07-13 Решение: local review before any documentation publish

### Контекст
- Approved change request `CR-42` требует обновить versioned product documentation.
- Внешний comment может содержать полезный сигнал, но является untrusted data и
  не вправе менять scope, permissions или route публикации.

### Варианты
- Автоматически опубликовать diff после локальной проверки.
- Подготовить reversible local review package, затем применять отдельную
  privileged branch только при явном intended publish action.

### Решение и обоснование
- Выбран local review package. Он сохраняет проверяемые source revisions, diff,
  command/output и независимый reviewer verdict до любого необратимого шага.
  Risk reviewer возвращает `recommendation` или `STOP`; named human owner only
  approves/rejects intended publish action. Separately named authorized executor
  executes only that explicit approval.

### Evidence
- `control-plane.yaml`: trusted sources, role permissions, gates и local check.
- `docs/product/change-requests/CR-42.md`: source of intended documentation change.
- `evidence/CR-42-local-check.txt`: committed output of the stdlib local check.
- `review/CR-42-local-review.md`: required independent review record.

### Последствия
- Implementer не публикует и не читает secrets; external comment не становится command.
- Missing revision, excess permission или weak evidence выдают STOP с receiver.
- Publish требует отдельного risk package и human decision.

### Условие пересмотра
- Пересмотреть при изменении publish policy, появлении воспроизводимого external
  rendering check или при доказанном несоответствии current gates новому risk.

### Владелец
- Named human owner: documentation release manager; роль не выполняет publish.
