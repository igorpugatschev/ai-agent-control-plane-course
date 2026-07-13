# Урок 7. Контракт роли агента

## Результат урока

Вы превратите общие названия ролей в проверяемые контракты. Результат - `artifacts/module-03/role-contracts.md` с contract для coordinator, implementation, reviewer, QA/SDET и risk reviewer.

## Зачем это инженеру

Фраза «попросим агента сделать задачу» не сообщает, кто вправе менять файл, кто проверяет доказательства и кто несет риск решения. Без контракта один исполнитель может расширить scope, сам себя одобрить и скрыть, что внешнее действие не было разрешено. Уверенный текст модели это не исправляет.

Роль делает ответственность наблюдаемой до запуска. Другой инженер видит допустимые входы, ожидаемый output, границу tools, момент STOP и следующего владельца. Поэтому ошибку можно вернуть к конкретному contract, а не спорить о том, что «агент обычно так делает».

## Теория

### Роль - это контракт ответственности

Контракт роли содержит восемь обязательных полей: цель, принятые входы, обязательный выход, разрешенные tools, запрещенные действия, stop conditions, критерии качества и получатель handoff. Цель описывает результат, а не занятость: «дать независимый verdict review» проверяемо, «помочь с кодом» - нет.

Входы ограничивают, на чем роль вправе основывать вывод. Reviewer принимает согласованную границу, diff и evidence, но не заменяет их предположением. Output имеет формат: findings с путем и наблюдением либо явный verdict. Тогда receiver может действовать без повторного исследования.

### Разделение конфликтующих полномочий

Один человек или runtime может последовательно исполнять несколько ролей, но не должен совмещать конфликтующие решения в одном шаге. Implementation готовит изменение и evidence, но не утверждает собственный результат. Reviewer читает и запускает проверки, но не редактирует файл implementation: иначе finding и исправление смешиваются. Risk reviewer владеет risk analysis и approval-gate process для удаления данных, публикации или отправки в защищенную ветку; coordinator доставляет ему package, а recommendation или STOP - named human owner.

Final irreversible-action approval дает только named human owner.

### Least privilege и STOP

Роль получает минимальное permission, достаточное для ее цели. Разрешение `read` не дает права писать, а наличие клиента Git не дает права `push`. Если нужный вход отсутствует, scope конфликтует, evidence неполно или следующий запрос превышает контракт, роль фиксирует STOP. STOP включает blocked action, факт, риск, безопасный шаг, владельца решения и handoff.

## Ключевые термины

- **Role contract (контракт роли)** - проверяемое описание ответственности, входов, выходов, прав, запретов и передачи.
- **Least privilege (минимальные привилегии)** - выдача только действий, без которых роль не достигнет цели.
- **Permission (разрешение)** - право конкретной роли выполнить действие в определенном scope.
- **Separation of duties (разделение обязанностей)** - разнесение конфликтующих решений между независимыми ролями.
- **Stop condition (условие остановки)** - наблюдаемое обстоятельство, при котором роль не продолжает действие.
- **Quality criterion (критерий качества)** - наблюдаемый признак приемлемого output.
- **Handoff target (получатель handoff)** - роль или человек, который получает следующий пакет.

## Рабочий пример

Согласованный scope допускает изменение `TaskService` и тестов в отдельной ветке. Implementation получает запрос: «после тестов удали stale-сценарий и сделай push». Изменение кода может входить в scope, но удаление сценария и push являются отдельными рискованными действиями. Contract implementation требует STOP для них и передачу coordinator-у; coordinator передает пакет risk reviewer-у.

### Подготовленный ответ агента без API-ключа

```text
Роль: implementation.
Статус: PARTIAL STOP.
Принятый scope: изменить только согласованные файлы TaskService и его тесты.
Evidence: список файлов, git diff, точная pytest-команда и вывод.
Запрещено: удалить stale-сценарий и выполнить git push.
Причина: это не входит в permission implementation и может быть необратимо.
Безопасный шаг: handoff coordinator-у с requested action, risk, scope и evidence.
Результат не утвержден: нужен независимый reviewer.
```

Это корректный результат даже если локальные тесты прошли: passing test не превращает implementation в approver и не снимает permission boundary.

## Практика

Создайте один накопленный артефакт:

```bash
mkdir -p artifacts/module-03
printf '# Контракты ролей\n' > artifacts/module-03/role-contracts.md
```

1. Скопируйте структуру `templates/agent-role.md` пять раз и назовите contracts `coordinator`, `implementation`, `reviewer`, `QA/SDET`, `risk reviewer`.
2. У каждого contract заполните восемь полей: `Цель`, `Принятые входы`, `Обязательный выход`, `Разрешенные tools`, `Запрещенные действия`, `Stop conditions`, `Критерии качества`, `Получатель handoff`.
3. Для implementation разрешите лишь согласованное редактирование и локальные тесты; запретите self-approval, удаление, deploy и push без решения.
4. Для reviewer разрешите чтение, `git diff` и повторный запуск проверок; запретите редактирование author files.
5. Для risk reviewer укажите владельца risk analysis и approval-gate process. Его output - documented `recommendation` или `STOP`, а не выполнение действия или final approval.
6. У каждого STOP назовите evidence и receiver; не пишите «остановиться при проблеме» без наблюдаемого условия.

### Необязательный prompt для живого агента

```text
Подготовь только Markdown-черновик пяти role contracts для учебного TaskService.
Не меняй файлы, не запускай команды, не выполняй push, deploy или удаления.
У каждой роли верни: Цель, Принятые входы, Обязательный выход, Разрешенные tools,
Запрещенные действия, Stop conditions, Критерии качества, Получатель handoff.
Сохрани разделение: reviewer не редактирует автора, implementation не утверждает
себя, risk reviewer выполняет analysis и возвращает recommendation или STOP. При нехватке входа
или permission верни STOP и receiver.
```

Проверьте черновик по локальной практике. Агент не может создать себе permission, назвать тест заменой review или назначить себя владельцем approval.

## Проверка результата

```bash
test -f artifacts/module-03/role-contracts.md
for role in coordinator implementation reviewer "QA/SDET" "risk reviewer"; do
  grep -qi "$role" artifacts/module-03/role-contracts.md || exit 1
done
for field in "Цель" "Принятые входы" "Обязательный выход" "Разрешенные tools" \
  "Запрещенные действия" "Stop conditions" "Критерии качества" "Получатель handoff"; do
  grep -qi "$field" artifacts/module-03/role-contracts.md || exit 1
done
grep -qiE 'reviewer.*не.*редакт|не.*редакт.*reviewer' artifacts/module-03/role-contracts.md
grep -qiE 'implementation.*не.*утверж|не.*утверж.*implementation' artifacts/module-03/role-contracts.md
grep -qiE 'risk reviewer.*необратим|необратим.*risk reviewer' artifacts/module-03/role-contracts.md
```

Наблюдаемые критерии приемки:

- каждый role contract имеет все восемь полей и receiver;
- output reviewer-а отличен от output implementation;
- reviewer не имеет write permission на работу автора;
- implementation не имеет self-approval;
- risk reviewer владеет risk analysis и approval-gate process, а named human
  owner - final irreversible-action approval;
- каждый STOP указывает факт, risk, безопасный шаг и handoff.

Локальный маршрут исправления: если команда не находит поле, добавьте его к отсутствующему contract, не меняя другие роли. Если две роли могут принять один конфликтующий результат, оставьте решение у независимого reviewer или risk reviewer. Если STOP не дает продолжения, добавьте evidence, receiver и resume condition в `role-contracts.md`, затем повторите команду.

## Типичные ошибки

- **Роль названа, но не ограничена.** Исправление: добавьте входы, output и конкретные запреты.
- **Implementation сам поставил `approve`.** Исправление: замените на evidence и handoff reviewer-у.
- **Reviewer исправил найденный дефект.** Исправление: верните finding implementation; reviewer сохраняет независимость.
- **Risk reviewer получил право сделать push или final approval.** Исправление:
  оставьте ему analysis и recommendation/STOP, а final approval дает named human
  owner; действие выполняйте отдельной разрешенной ролью после approval.
- **STOP скрывает риск.** Исправление: запишите blocked action и возможный ущерб.

## Контрольные вопросы

1. Почему название роли без output и permission не является контрактом?
2. Какие решения нельзя объединять у implementation?
3. Почему reviewer не должен исправлять author file во время review?
4. Чем владелец approval отличается от исполнителя одобренного действия?
5. Когда наличие инструмента не дает права его применять?
6. Какие поля позволяют следующей роли продолжить после STOP?

## Официальные источники

- [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents) - официальный источник о ролях, tools и управляемых workflow; contract урока полностью изложен локально.
- [Model Context Protocol: security best practices](https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices) - официальный источник о границах доступа и подтверждениях; MCP не требуется для задания.
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) - официальный каталог control families, включая least privilege и separation of duties; читать его для практики необязательно.
