# Урок 8. Tools, skills и permissions

## Результат урока

Вы соберете `artifacts/module-03/skill-and-permission-matrix.md`: матрицу, которая отделяет технически доступные tools, повторяемые skills и permissions конкретных ролей для учебного TaskService.

## Зачем это инженеру

Путаница «у агента есть Git, значит он может отправить ветку» открывает путь к несанкционированным действиям. В обратную сторону, «роль QA может тестировать» не объясняет, какой сценарий, с какими входами и каким evidence повторить. Tool, skill и permission решают разные задачи и не заменяют друг друга.

Матрица делает разницу проверяемой до запуска. Она показывает, что роль может технически вызвать, по какой процедуре она работает и какое действие ей разрешено в текущем scope. Coordinator поэтому выбирает безопасного исполнителя и объясняет отказ.

## Теория

### Нормативная privileged chain

- Risk reviewer выполняет только risk analysis и возвращает recommendation или STOP.
- Named human owner только approve/reject intended irreversible action.
- Separately named authorized executor, отличный от named human owner и risk reviewer, выполняет ровно approved action.
- Executor возвращает execution evidence: identity, approved scope, operation id, exit/output и resulting state.
- Недостаточное permission/evidence приводит к `STOP before execution`.

### Три разных уровня

**Tool** выполняет отдельное техническое действие: `git diff` показывает изменение, `pytest` запускает тест, редактор пишет файл. Tool сам не знает цель, порядок или владельца решения.

**Skill** - повторяемая процедура. Skill «проверить изменение TaskService» получает scope, требования, diff и тесты; читает контракт, запускает exact command, фиксирует output и возвращает findings. Его шаги, ограничения и evidence описываются в `templates/skill-contract.md`.

**Permission** отвечает на вопрос, имеет ли конкретная роль право использовать tool для конкретного действия в заданном scope. QA/SDET может запустить тест в локальном стенде, но не переписать требования после падения. Implementation может писать согласованный файл, но не публиковать результат.

### Матрица минимальных прав и schemas

Записывайте строку как `роль -> skill -> tool -> разрешенное действие -> scope -> evidence -> запрет`. Один tool допускает разные permissions: reviewer использует `git diff` только для inspection, implementation использует editor только для согласованных путей. `git push` может быть технически установлен, но у всех пяти roles нет permission выполнить его без отдельного human approval и назначения исполнителя.

Skill начинается с input schema: обязательные поля и недоверенные данные. Output schema задает поля handoff: `scope`, `sources`, `changed_files`, `command`, `exit_code`, `observed_result`, `findings`, `stop_status`, `receiver`. Если поле отсутствует, skill не достраивает его моделью, а возвращает STOP.

### Вендорные реализации вторичны

Vendor-neutral contract работает независимо от runtime. В OpenAI Agents SDK tool и handoff могут быть объектами SDK; в MCP tool может предоставлять server; в Copilot tool может быть доступен в agent environment. Во всех вариантах capability не заменяет permission, а provider API не меняет owner approval, schemas и stop conditions этого урока.

## Ключевые термины

- **Tool (инструмент)** - единичная техническая возможность, например поиск, редактор или test runner.
- **Skill (навык)** - воспроизводимая процедура с входами, шагами, ограничениями и evidence.
- **Permission (разрешение)** - право роли выполнить действие tool внутри scope.
- **Input schema (схема входа)** - обязательные поля входного пакета.
- **Output schema (схема выхода)** - обязательные поля, которые возвращает skill.
- **Capability (техническая возможность)** - то, что runtime способен сделать; не равно permission.
- **Least privilege (минимальные привилегии)** - отсутствие лишних actions даже при доступности tool.

## Рабочий пример

QA/SDET получает задачу проверить измененный `TaskService`. Его skill имеет input schema: подтвержденный scope, repo-relative пути, diff и команда. Разрешенные tools: `read`, `git diff`, `pytest`. Permission: запускать только `PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q` и описывать наблюдение. Он не меняет код, контракт или статус review.

### Подготовленный ответ агента без API-ключа

```text
Skill: локальная проверка TaskService.
Input schema: scope, requirements.md, api/openapi.yaml, changed_files, command.
Проверка входа: поле changed_files отсутствует.
Статус: STOP.
Tools не запускаются, потому что нельзя проверить scope результата.
Evidence: отсутствующее поле changed_files в handoff.
Handoff: coordinator; запросить у implementation список файлов и diff.
Запрещено: угадывать список файлов, редактировать сервис или ставить approve.
Privileged result: STOP before execution; tool call и executor отсутствуют.
```

STOP сохраняет достоверность: `pytest` может быть зеленым, но без scope QA/SDET не докажет, что проверял требуемое изменение.

## Практика

Создайте артефакт:

```bash
mkdir -p artifacts/module-03
printf '# Матрица skills и permissions\n' > artifacts/module-03/skill-and-permission-matrix.md
```

1. Используйте `templates/skill-contract.md` для skills `подготовка реализации`, `независимый review`, `локальная QA-проверка`, `risk analysis и approval-gate process` и `маршрутизация handoff`.
2. У каждого skill запишите input и output schema. Включите `scope`, `sources`, `evidence`, `stop_status`, `receiver`; для проверки добавьте command и observed result.
3. Создайте таблицу с колонками `Роль`, `Skill`, `Tool`, `Разрешенное действие`, `Scope`, `Evidence`, `Запрет`.
4. Внесите `read/search`, editor, `git diff`, `pytest`, `git commit`, `git push`, удаление файла. Отделите capability от permission.
5. Зафиксируйте: reviewer не использует editor для author files; implementation не использует approve; risk reviewer выполняет analysis и возвращает recommendation или STOP, но не выполняет необратимое действие и не дает final approval.
6. Добавьте STOP для отсутствующего input schema и correction route: receiver и поле, которое должен добавить sender.
7. В конце кратко сравните один provider-specific пример с vendor-neutral contract, не вводя обязательный SDK или ключ.

### Необязательный prompt для живого агента

```text
Не меняй файлы и не выполняй команды. Подготовь Markdown-черновик матрицы
tools, skills и permissions для пяти ролей TaskService. Сначала дай
vendor-neutral определения tool, skill и permission, затем таблицу
роль -> skill -> tool -> разрешенное действие -> scope -> evidence -> запрет.
У каждого skill задай input/output schema с scope, sources, evidence,
stop_status и receiver. Ограничения: reviewer не редактирует, implementation
не self-approves, risk reviewer владеет risk analysis и approval-gate process.
При отсутствующем schema верни structured STOP и handoff coordinator-у.
```

Проверьте, что черновик не превращает установленный tool в permission и не требует provider API для обязательной практики.

## Проверка результата

```bash
test -f artifacts/module-03/skill-and-permission-matrix.md
for term in "Input schema" "Output schema" scope sources evidence stop_status receiver Tool Skill Permission STOP; do
  grep -qi "$term" artifacts/module-03/skill-and-permission-matrix.md || exit 1
done
for tool in "git diff" pytest "git push"; do
  grep -qi "$tool" artifacts/module-03/skill-and-permission-matrix.md || exit 1
done
grep -qiE 'reviewer.*не.*редакт|не.*редакт.*reviewer' artifacts/module-03/skill-and-permission-matrix.md
grep -qiE 'implementation.*не.*утверж|не.*утверж.*implementation' artifacts/module-03/skill-and-permission-matrix.md
grep -qiE 'risk reviewer.*approval|approval.*risk reviewer' artifacts/module-03/skill-and-permission-matrix.md
for term in "risk analysis" recommendation STOP "approve/reject" \
  "authorized executor" "approved action" "execution evidence" identity \
  "approved scope" "operation id" "exit/output" "resulting state"; do
  grep -qi "$term" artifacts/module-03/skill-and-permission-matrix.md || exit 1
done
```

Наблюдаемые критерии приемки:

- definitions tool, skill и permission различимы на одном примере;
- каждый skill имеет input и output schema;
- матрица показывает scope и evidence, а не только tool name;
- `git push` и удаление имеют явный запрет без approval;
- отсутствие обязательного поля приводит к STOP и receiver;
- Final irreversible-action approval дает только named human owner.
- provider-specific пример вторичен и не нужен для no-key маршрута.

Локальный маршрут исправления: если нет поля schema, добавьте его в skill contract и повторите проверку. Если permission звучит как tool, перепишите строку глаголом и scope: не «pytest», а «запустить указанную локальную команду для согласованных файлов». Если provider пример стал обязательным, вынесите его в необязательную заметку и восстановите vendor-neutral procedure.

## Типичные ошибки

- **Tool назван skill.** Исправление: добавьте trigger, входы, шаги и evidence процедуры.
- **Skill выдан как permission.** Исправление: укажите роль и scope, где он разрешен.
- **Schema не содержит receiver.** Исправление: добавьте получателя любого STOP или result.
- **Green test считается approval.** Исправление: оставьте тест evidence QA, а approval передайте независимой роли.
- **SDK диктует workflow.** Исправление: сначала восстановите vendor-neutral contract, затем пометьте SDK как пример.

## Контрольные вопросы

1. Чем capability отличается от permission?
2. Почему один `git diff` имеет разные применения у reviewer и implementation?
3. Какие поля нужны, чтобы receiver мог воспроизвести проверку?
4. Почему skill останавливается при неполном input schema?
5. Может ли risk reviewer быть исполнителем необратимого действия по умолчанию?
6. Что остается неизменным при переходе от local workflow к provider SDK?

## Официальные источники

- [OpenAI Agents SDK for Python](https://openai.github.io/openai-agents-python/) - официальный пример tools, handoffs и guardrails как реализации, а не обязательного contract урока.
- [Model Context Protocol: Introduction](https://modelcontextprotocol.io/docs/getting-started/intro) - официальный источник о подключении tools; MCP не предоставляет permission вместо control plane.
- [Git documentation: git diff](https://git-scm.com/docs/git-diff) - официальное описание local inspection tool из примеров.
