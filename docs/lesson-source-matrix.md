# Lesson source matrix

Матрица показывает traceability обязательной теории. Каждая строка содержит
только URL, который указан в `## Официальные источники` соответствующего урока:
ровно один primary Tier 1 URL. Supporting source указывается только при таком же
буквальном присутствии URL в том же уроке; `—` означает отсутствие фактически
использованного Tier 2/3 material. Все источники ниже checked **2026-07-13**.

| Урок | Primary Tier 1 | Поддерживающий Tier 2/3 | Проверено | Точная поддерживаемая тема | Ограничение вендора |
| --- | --- | --- | --- | --- | --- |
| 1 | [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents) (Tier 1) | — | 2026-07-13 | Различие model, tools и управляемого agent workflow | OpenAI workflow не определяет local authority, approval или control plane |
| 2 | [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents) (Tier 1) | — | 2026-07-13 | Instructions, tools и управляющий workflow как границы задачи | Guide не назначает permission конкретной задачи или human owner |
| 3 | [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents) (Tier 1) | — | 2026-07-13 | Agent workflows, tools и blueprint components | OpenAI mechanisms являются частной реализацией, не обязательным стеком |
| 4 | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (Tier 1) | — | 2026-07-13 | Formal API contract в source hierarchy | OAS не разрешает local conflict и не подтверждает freshness локальных docs |
| 5 | [Model Context Protocol documentation](https://modelcontextprotocol.io/docs/getting-started/intro) (Tier 1) | — | 2026-07-13 | Ограниченный context packet и внешние tools | Context integration не подменяет permission или human owner |
| 6 | [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents) (Tier 1) | — | 2026-07-13 | Ограничения и checks в управляемых agent actions | Guide не задает local source hierarchy или owner decision |
| 7 | [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents) (Tier 1) | — | 2026-07-13 | Roles, tools и управляемый workflow в role contract | Guide не определяет local prohibitions и separation of duties |
| 8 | [OpenAI Agents SDK for Python](https://openai.github.io/openai-agents-python/) (Tier 1) | — | 2026-07-13 | Tools, handoffs и guardrails как пример реализации | SDK не предоставляет permission вместо local control plane |
| 9 | [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents) (Tier 1) | — | 2026-07-13 | Orchestration и handoff patterns для coordinator routing | Guide не назначает receiver, authority owner или approval process |
| 10 | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (Tier 1) | — | 2026-07-13 | API contract для intake и acceptance impact | OAS не определяет product priority, exclusions или owner |
| 11 | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (Tier 1) | — | 2026-07-13 | Contract-aware controlled code change | OAS не заменяет focused tests и independent review |
| 12 | [Git documentation](https://git-scm.com/docs) (Tier 1) | — | 2026-07-13 | Commit и diff evidence в engineering gates | Git не выдает approval и не определяет routing |
| 13 | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (Tier 1) | — | 2026-07-13 | HTTP contract как source для testable conditions | API description не подтверждает behavior без observed output |
| 14 | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (Tier 1) | — | 2026-07-13 | Paths, operations, responses и schemas для API checks | OAS не делает unit test HTTP evidence и не требует UI scope |
| 15 | [pytest documentation](https://docs.pytest.org/) (Tier 1) | — | 2026-07-13 | Collection и report output для regression evidence | pytest output не является release approval и не объясняет flaky cause |
| 16 | [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) (Tier 1) | — | 2026-07-13 | Direct/indirect injection, untrusted input и least privilege | OWASP не назначает local owner или STOP record |
| 17 | [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) (Tier 1) | — | 2026-07-13 | Govern, Map, Measure и Manage для gates и authority | Core не задает конкретную role matrix или executor |
| 18 | [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai) (Tier 1) | — | 2026-07-13 | GenAI trace conventions и attributes для evaluation evidence | Conventions не определяют redaction policy или permission log payload |
| 19 | [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) (Tier 1) | — | 2026-07-13 | Risk ownership при сборке capstone control plane | Core не заменяет local contracts, gates и evidence index |
| 20 | [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/) (Tier 1) | — | 2026-07-13 | Measured failure, correction и re-run | Playbook не заменяет local N-01/F-01/F-02/F-03 evidence |
| 21 | [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai) (Tier 1) | — | 2026-07-13 | Trace terminology для audit и observability | Telemetry standard не определяет rubric, remediation или roadmap |

## Catalog boundary

`docs/source-catalog.md` также хранит verified catalog extensions, включая
DeepSeek, Qwen, A2A, GitHub Actions и ADK. Они не присваиваются строкам этой
матрицы без actual lesson use: catalog extensions не доказывают dependency
урока. JSON Schema остается Tier 1 reference для schema validation, но также
не является обязательным source уроков 1-21.
