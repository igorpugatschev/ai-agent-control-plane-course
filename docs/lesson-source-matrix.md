# Lesson source matrix

Матрица показывает traceability обязательной теории. `—` означает, что в уроке
не использован Tier 2/3 material: искусственно добавить его означало бы создать
ложную зависимость. Все источники ниже checked **2026-07-13**.

| Урок | Primary Tier 1 | Поддерживающий Tier 2/3 | Проверено | Точная поддерживаемая тема | Ограничение вендора |
| --- | --- | --- | --- | --- | --- |
| 1 | [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents) (Tier 1); comparative [DeepSeek API](https://api-docs.deepseek.com/) и [Qwen docs](https://qwen.readthedocs.io/en/stable/getting_started/quickstart.html) (Tier 1) | — | 2026-07-13 | model/agent/tools и provider runtime | Provider API не определяет local authority, approval или control plane |
| 2 | [MCP specification](https://modelcontextprotocol.io/specification/latest) (Tier 1) | — | 2026-07-13 | Capability и security boundaries для context/tools | MCP не выдает task permission и не заменяет owner decision |
| 3 | [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents) (Tier 1) | — | 2026-07-13 | Agents, handoffs, guardrails и workflow в blueprint | OpenAI mechanisms - частная реализация, не обязательный стек |
| 4 | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (Tier 1) | — | 2026-07-13 | Formal API contract для comparison requirements/tests | OAS не решает product conflict и freshness local docs |
| 5 | [MCP specification](https://modelcontextprotocol.io/specification/latest) (Tier 1) | — | 2026-07-13 | Ограниченный context packet, resources и tool boundaries | Capability не оправдывает передачу всего repo |
| 6 | [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents) (Tier 1) | — | 2026-07-13 | Evidence gate в controlled workflow | Guide не задает local source hierarchy/owners |
| 7 | [MCP specification](https://modelcontextprotocol.io/specification/latest) (Tier 1) | — | 2026-07-13 | Consent и tool safety для role contract | MCP не задает reviewer/human owner обязанности |
| 8 | [MCP specification](https://modelcontextprotocol.io/specification/latest) (Tier 1) | — | 2026-07-13 | Prompts/resources/tools как разные primitives | Primitive не равен permission; local contract обязателен |
| 9 | [A2A Protocol specification](https://a2a-protocol.org/latest/specification/) (Tier 1) | — | 2026-07-13 | Task/message/artifact exchange как контекст handoff | A2A не назначает local receiver, authority или approval |
| 10 | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (Tier 1) | — | 2026-07-13 | Operations и contract impact в intake/acceptance | Spec не определяет product priority, exclusions или owner |
| 11 | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (Tier 1) | — | 2026-07-13 | Contract sync для controlled service/API change | OAS не заменяет focused tests и independent review |
| 12 | [GitHub Actions documentation](https://docs.github.com/en/actions/reference) (Tier 1) | — | 2026-07-13 | CI workflow/job/step vocabulary для repeatable gates | CI verdict не product approval; GitHub не обязателен локально |
| 13 | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (Tier 1) | — | 2026-07-13 | API requirements в testable conditions/traceability | API description не подтверждает behavior без output |
| 14 | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (Tier 1) | — | 2026-07-13 | Schema-level API expectations, separate from UI evidence | OAS не требует UI scope и не делает unit test HTTP evidence |
| 15 | [GitHub Actions documentation](https://docs.github.com/en/actions/reference) (Tier 1) | — | 2026-07-13 | CI boundaries для regression/release evidence | Platform не определяет release authority, rollback или flaky cause |
| 16 | [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) (Tier 1) | — | 2026-07-13 | Direct/indirect injection, untrusted input и least privilege | OWASP не назначает local owner/STOP record |
| 17 | [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) (Tier 1) | — | 2026-07-13 | Governance/risk management для STOP/review/approval separation | RMF не задает конкретную role matrix/executor |
| 18 | [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai) (Tier 1) | — | 2026-07-13 | GenAI trace attributes для evaluation/tracing | Conventions не задают redaction policy/permission log payload |
| 19 | [Google Agent Development Kit documentation](https://adk.dev/) (Tier 1) | — | 2026-07-13 | Graph/multi-agent workflows, tools, evaluation и observability | ADK/cloud/model adapters не обязательны для capstone |
| 20 | [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) (Tier 1) | — | 2026-07-13 | Measured failure, correction и re-run | RMF не заменяет local N-01/F-01/F-02/F-03 evidence |
| 21 | [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai) (Tier 1) | — | 2026-07-13 | Trace terminology для audit/observability | Telemetry standard не определяет rubric/remediation/roadmap |

## Catalog boundary

`docs/source-catalog.md` содержит [JSON Schema](https://json-schema.org/specification)
как Tier 1 reference для schema validation. Он не является обязательным source
уроков 1-21, поэтому намеренно не присвоен строке без actual lesson use.
