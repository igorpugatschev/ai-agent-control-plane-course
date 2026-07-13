# Checkpoint 2. Контекст и evidence для stale-документации

## Что проверяется

Checkpoint проверяет, умеете ли вы заметить конфликт между локальными источниками, собрать минимальный контекст и остановить работу до неподтвержденной реализации. Ценность работы не в догадке о происхождении старой инструкции, а в воспроизводимом решении: что подтверждено, кто вправе решать дальше и какие действия запрещены.

Используйте накопленные артефакты:

```text
artifacts/module-02/source-register.md
artifacts/module-02/context-packet.md
artifacts/module-02/context-map-evidence-gate.md
```

## Входные данные

Работайте только с repo-relative материалами учебного стенда:

```text
projects/training-task-app/requirements.md
projects/training-task-app/api/openapi.yaml
projects/training-task-app/tests/test_service.py
projects/training-task-app/src/task_app/service.py
projects/training-task-app/scenarios/stale-documentation.md
templates/context-map.md
```

`scenarios/stale-documentation.md` содержит намеренный конфликт и не является инструкцией к использованию сервиса. Определения, формат артефактов и проверки находятся в уроках 4-6; официальные ссылки лишь подтверждают материал.

## Задание

Обновите только три артефакта так, чтобы reviewer мог воспроизвести вывод без устных пояснений.

1. Зафиксируйте конфликт: stale-инструкция требует название и `closed`, а требования, OpenAPI и тесты подтверждают `task_id` и `done`.
2. Для каждого источника укажите документированный `Source owner`; если он отсутствует в локальных данных, запишите `unknown`, явный пробел и эскалацию к `Authority owner`. Не выводите владельца источника из роли, которая принимает решение.
3. Назначьте отдельный `Authority owner`: Product owner принимает решение о судьбе старой инструкции и любой смене контракта.
4. Укажите check date, выполните `git rev-parse HEAD` и запишите фактическое неизменяемое значение SHA вместо `<git rev-parse HEAD output>` для основных источников.
5. Отделите факты, предположения, live state и открытые вопросы. Причина устаревания остается предположением, пока `Authority owner` не подтвердит ее.
6. Соберите минимальный packet: trusted instructions, untrusted stale-текст, exclusions, citations и оба owner.
7. Заполните карту по `templates/context-map.md` и evidence gate с `Source owner`/документированным `unknown` с эскалацией, `Authority owner`, воспроизводимым evidence, confidence и исходом.
8. Выполните `PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q` и запишите точную команду с наблюдением `11 passed`.
9. Завершите явным `STOP before unsupported implementation`: нельзя менять `TaskService`, OpenAPI или старую документацию до решения Product owner и документирования `Source owner` либо `unknown` с эскалацией.

Не создавайте код, не меняйте стенд, не выбирайте контракт голосованием источников, не придумывайте owner и не заменяйте решение `Authority owner` текстом агента.

## Обязательный режим без API-ключа

Используйте подготовленные ответы в уроках как материал для критики. Они показывают форму STOP, но не содержат готового checkpoint-ответа: вы записываете свои check date, SHA, citations, команду и условия gate. Не переносите ответ агента без сопоставления с локальными источниками.

## Необязательный режим с живым агентом

Можно попросить агента критически прочитать три Markdown-файла. Разрешите ему только читать перечисленные входы и артефакты, вернуть список пробелов и предложить Markdown-правки. Агенту запрещены изменение файлов, сетевые действия, решение вместо Product owner и утверждение, что реализация разрешена.

```text
Проверь три артефакта Module 2 на stale-документации. Не меняй файлы и не
разрешай реализацию. Ищи `Source owner` либо документированное `unknown` с
эскалацией, отдельный `Authority owner`, check date, confidence, repo-relative
citations, воспроизводимый pytest evidence, distinction between
fact/assumption/live state и STOP before unsupported implementation.
Верни только пробелы с путем артефакта и правилом проверки.
```

Каждый комментарий агента проверяйте по локальным файлам и rubric.

## Самопроверка

Запустите из корня репозитория:

```bash
for file in source-register.md context-packet.md context-map-evidence-gate.md; do
  test -f "artifacts/module-02/$file" || exit 1
done
for file in artifacts/module-02/*.md; do
  grep -qi "Source owner" "$file" || exit 1
  grep -qi "Authority owner" "$file" || exit 1
  grep -qiE 'unknown|Source owner:.+[^ ]' "$file" || exit 1
  grep -qiE 'эскалац|escalat' "$file" || exit 1
  grep -qiE 'Проверено|check date|202[0-9]-[0-9]{2}-[0-9]{2}' "$file" || exit 1
  grep -qi "Confidence" "$file" || exit 1
done
grep -qi "STOP" artifacts/module-02/source-register.md
grep -qi "Citations" artifacts/module-02/context-packet.md
grep -qi "Evidence gate" artifacts/module-02/context-map-evidence-gate.md
grep -qi "unsupported implementation" artifacts/module-02/context-map-evidence-gate.md
git rev-parse HEAD
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
# Ожидаемое наблюдение: 11 passed
```

Проведите два walkthrough:

1. **Подтверждение конфликта:** reviewer проходит от stale-сценария к требованиям, OpenAPI и тесту, повторяет команду и видит, почему evidence достаточно для STOP.
2. **Попытка реализации:** implementer предлагает изменить `TaskService` или OpenAPI. Карта показывает отсутствие owner approval, запрещает действие, возвращает к Product owner и называет артефакты для обновления после решения.

Walkthrough пройден, если на каждом переходе видны `Source owner` или документированное `unknown` с эскалацией, отдельный `Authority owner`, check date, фактический SHA, confidence, repo-relative evidence, точная pytest-команда с наблюдением `11 passed`, следующий допустимый шаг и stop-condition.

## Оценивание

Каждый критерий оценивается от 0 до 2.

| Критерий | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Иерархия и owner | Источники смешаны, owner нет | Source owner и Authority owner смешаны | Для каждого источника есть Source owner либо documented `unknown` с эскалацией; отдельный Authority owner решает конфликт |
| Факты и свежесть | Догадки выданы за факты | Не хватает даты, SHA или live state | Категории отделены, check date, фактический SHA и команда воспроизводимы |
| Минимальный packet | Нужен весь репозиторий | Лишние или необъясненные данные | Один вопрос, trusted/untrusted, exclusions и citations |
| Evidence gate | «Агент подтвердил» | Evidence или один из owner неполны | Команда/файлы, confidence, оба owner, pass/fail и correction route |
| STOP и handoff | Реализация разрешена по догадке | STOP без возобновления | STOP до unsupported implementation, owner-вопрос и путь возобновления |

Для зачета нужно не менее 8 из 10 и отсутствие критических дефектов.

## Критические дефекты

Checkpoint не пройден независимо от баллов, если есть хотя бы один дефект:

- **Missing source owner or documented unknown:** у существенного источника нет `Source owner`, либо нет явного `unknown`, пробела и эскалации к `Authority owner`.
- **Missing authority owner:** нет отдельного Product owner или уполномоченной роли, которая решает конфликт и смену контракта.
- **Missing check date or confidence:** существенный вывод не имеет даты проверки либо скрывает уверенность.
- **Unreproducible evidence:** нет repo-relative источника, команды/ожидаемого наблюдения или reviewer не может повторить проверку.
- **Unsupported implementation:** артефакты разрешают менять сервис, API или stale-документацию без решения owner.
- **Hidden conflict:** старая инструкция выдана за текущий контракт или не приводит к STOP.
- **External-reading dependency:** обязательное объяснение вынесено во внешний источник.

## Локальный маршрут исправления

- missing source owner or documented unknown -> добавьте документированного `Source owner` либо `unknown`, пробел и эскалацию к `Authority owner` во все три артефакта, затем повторите walkthrough;
- missing authority owner -> добавьте отдельного Product owner и полномочие в `source-register.md`, `context-packet.md` и gate, повторите walkthrough;
- missing check date/confidence -> исправьте метаданные реестра, перенесите их в packet и карту, повторите структурную команду;
- unreproducible evidence -> укажите repo-relative файл, `git rev-parse HEAD`, фактический SHA, точную pytest-команду и наблюдение `11 passed` в `context-map-evidence-gate.md`, затем запустите ее снова;
- hidden conflict -> сопоставьте требования, OpenAPI, тесты и stale-сценарий, восстановите отдельный STOP в трех артефактах;
- unsupported implementation -> удалите разрешение на изменение из packet и gate, верните шаг к Product owner, повторите walkthrough попытки реализации;
- лишний контекст -> удалите несвязанные файлы из packet и карты, объясните сохраненные источники одним вопросом, повторите проверку.

После коррекции повторяйте самопроверку с первого шага. Не ослабляйте evidence gate и не редактируйте учебный стенд ради зачета.

## Результат checkpoint

Сохраните три артефакта в `artifacts/module-02/`. В handoff следующему модулю укажите конфликт, `Source owner` или documented `unknown` с эскалацией, отдельный `Authority owner`, check date, фактический SHA, confidence, точную pytest-команду с наблюдением `11 passed`, действующий STOP и условие возобновления. Эти артефакты станут входом для ролей, skills и handoff Module 3.
