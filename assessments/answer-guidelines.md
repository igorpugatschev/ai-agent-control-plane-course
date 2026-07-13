# Answer guidance for reviewers

Это не answer key. Оценивайте путь рассуждения и проверяемость, а не длину
prose, точные слова или единственный допустимый owner.

## Quality patterns

- Claim привязан к source path, trust/freshness, command/output или decision record;
  student объясняет, что evidence подтверждает и чего не подтверждает.
- Scope содержит included/excluded work; assumption или conflict идет к authority
  owner, а не превращается в молчаливую реализацию.
- Role имеет ограниченные rights, prohibited actions, один receiver и observable
  handoff/resume condition.
- STOP блокирует конкретное действие до выполнения и оставляет безопасный
  reversible next step; correction называет artifact, owner и re-run.
- Test output, review verdict, risk recommendation, human approval и authorized
  execution не подменяют друг друга.
- Risk report отделяет residual risk, required remediation и optional extension.

## Frequent misconceptions

- Уверенный текст не заменяет evidence; короткий проверяемый ответ может быть сильнее.
- Tool, MCP server, A2A endpoint или framework не выдает permission и authority.
- Green test не равен product acceptance или approval необратимого действия.
- Source owner и Authority owner могут различаться; `unknown` требует эскалации.
- Safety не означает остановить все: допустим bounded reversible action в trusted scope.
- Critical safety defect нельзя компенсировать баллами или optional live-agent mode.

## Review posture

Просите показать artifact, command/output, blocked action, receiver и resume
condition. Не снижайте балл за иную структуру Markdown при эквивалентном,
проверяемом решении.
