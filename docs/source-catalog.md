# Каталог достоверных источников

Этот каталог фиксирует источники, на которые автор курса опирается при создании русскоязычного самодостаточного курса **AI Agent Control Plane Engineering**.

Важно: источники в этом документе не являются обязательным внешним чтением для студента. Обязательная теория, задания, критерии готовности и разбор типичных ошибок должны быть изложены внутри репозитория на русском языке. Ссылки нужны автору курса для проверки фактов, обновления материалов и углубления.

Дата первичной проверки каталога: **2026-07-13**.

## Уровни доверия

### Tier 1: официальная документация и спецификации

Главные источники истины:

- официальная документация продукта, API, SDK, CLI или платформы;
- API reference;
- официальные спецификации протоколов;
- changelog, release notes, migration guides;
- официальные security, safety, governance и compliance-разделы.

Если курс объясняет поведение инструмента, формат конфигурации, ограничение API, модель безопасности или рекомендуемый workflow, это должно подтверждаться источником Tier 1.

### Tier 2: официальные курсы и учебные репозитории

Важные источники структуры и педагогики:

- курсы от разработчиков платформы или библиотеки;
- официальные учебные репозитории;
- лабораторные работы и notebooks от команды продукта.

Материалы Tier 2 можно использовать для выбора тем, последовательности уроков, упражнений и типичных учебных ошибок. Но если в них описано поведение API или инструмента, это поведение нужно сверить с Tier 1.

### Tier 3: официальные примеры, cookbook и templates

Практические источники:

- official cookbook;
- sample apps;
- starter packs;
- reference implementations;
- шаблоны инфраструктуры и CI/CD.

Материалы Tier 3 полезны для практики, но не являются нормативными сами по себе. Любой важный вывод из примера должен быть проверен по Tier 1.

### Неосновные источники

Личные блоги, видео, статьи, форумы, агрегаторы, "awesome"-списки, ответы моделей и неофициальные пересказы можно использовать только для разведки и альтернативных объяснений. Они не должны быть источником истины для обязательной программы.

## Правило для GitHub и GitLab

Официальный учебный репозиторий на GitHub или GitLab попадает в Tier 2 только если он размещен в организации, принадлежащей разработчику продукта, платформы или библиотеки, либо явно указан из официальной документации.

Первичная проверка на 2026-07-13 подтвердила несколько GitHub-репозиториев уровня Tier 2. Подтвержденных GitLab-репозиториев с официальными курсами по агентам или нейросетям на эту дату не добавлено. Если такой источник появится позже, его нужно добавлять только после проверки владельца, статуса поддержки и связи с Tier 1 документацией.

## Tier 1: официальная документация и спецификации

### OpenAI, ChatGPT, Codex, API и Agents SDK

Ссылки:

- [OpenAI / ChatGPT developer docs](https://learn.chatgpt.com/docs)
- [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents)
- [OpenAI Agents SDK for Python](https://openai.github.io/openai-agents-python/)

Использовать для:

- OpenAI API и agentic workflows;
- Responses API, инструменты, guardrails, evaluation, observability;
- Codex как инженерная среда: AGENTS.md, кастомизация, skills, MCP, hooks, subagents;
- проектирование review-gates и safety-gates вокруг агентных действий.

Разделы курса:

- база control plane;
- контекст и инструменты;
- роли агентов;
- workflow;
- gates, review и safety;
- capstone.

Ограничения:

- названия моделей, доступность функций, лимиты, цены и политики нужно перепроверять на дату обновления урока;
- OpenAI-специфичные механики нужно отделять от общих принципов agent control plane.

### NIST AI RMF Core

- Роль: vendor-neutral Tier 1 framework для управления AI risks.
- Scope: функции Govern, Map, Measure и Manage; распределение ответственности,
  оценка и управление рисками в Module 6.
- Canonical URL: [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- Checked: 2026-07-13.

Ограничения:

- Core задает framework outcomes, а локальные role contracts и safety gates
  определяют учебный workflow и permissions.

### OWASP LLM01:2025 Prompt Injection

- Роль: Tier 1 security guidance для угрозы prompt injection.
- Scope: direct и indirect prompt injection, untrusted inputs, least privilege
  и boundaries в Module 6.
- Canonical URL: [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- Checked: 2026-07-13.

Ограничения:

- OWASP описывает риск и controls; решение о named human owner и local STOP
  остается частью учебного control plane.

### OpenTelemetry GenAI semantic conventions

- Роль: Tier 1 specification для trace conventions и attributes GenAI telemetry.
- Scope: trace conventions и attributes для Module 6 trace record; не redaction
  policy и не разрешения на запись payload.
- Canonical URL: [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
- Checked: 2026-07-13.

Ограничения:

- Redaction, data minimization и protected evidence определяет локальная course
  safety policy, а не semantic conventions.

### DeepSeek API documentation

- Роль: Tier 1 vendor API documentation для provider-neutral runtime comparison.
- Scope: authentication, compatible API surface и model/runtime constraints в
  вводной части курса; не workflow authority.
- Canonical URL: [DeepSeek API documentation](https://api-docs.deepseek.com/)
- Checked: 2026-07-13.

Ограничения:

- модели, compatibility и availability меняются; DeepSeek API не задает общие
  permissions, product scope или acceptance rules.

### Qwen documentation

- Роль: Tier 1 vendor documentation для open-model/runtime comparison.
- Scope: Qwen inference/deployment context в provider-neutral вводной части;
  не обязательная лаборатория и не control-plane specification.
- Canonical URL: [Qwen documentation](https://qwen.readthedocs.io/en/stable/getting_started/quickstart.html)
- Checked: 2026-07-13.

Ограничения:

- hardware, model versions и serving stack зависят от окружения; Qwen docs не
  определяют local roles, gates или approval.

### A2A Protocol specification

- Роль: Tier 1 interoperability specification для agent-to-agent task exchange.
- Scope: tasks, messages, artifacts, Agent Cards, transports и authentication
  boundaries как внешний контекст Module 3 handoff patterns.
- Canonical URL: [A2A Protocol specification](https://a2a-protocol.org/latest/specification/)
- Checked: 2026-07-13.

Ограничения:

- protocol interoperability не назначает local receiver, authority owner,
  approval process или permission matrix.

### OpenAPI Specification

- Роль: Tier 1 normative specification для machine-readable HTTP API contracts.
- Scope: operations, request/response schema и contract impact для Modules 2,
  4 и 5.
- Canonical URL: [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- Checked: 2026-07-13.

Ограничения:

- OAS не принимает product decisions, не доказывает live behavior без checks и
  не заменяет local source hierarchy.

### JSON Schema specification

- Роль: Tier 1 normative specification для JSON structure and validation.
- Scope: reference при проверке schema vocabulary и interoperability; не
  обязательный lesson dependency без actual schema task.
- Canonical URL: [JSON Schema specification](https://json-schema.org/specification)
- Checked: 2026-07-13.

Ограничения:

- JSON Schema validates data shape, но не определяет API semantics, permissions
  или evidence/approval workflow.

### GitHub Actions documentation

- Роль: Tier 1 platform documentation для CI workflow vocabulary и execution.
- Scope: workflow, job, step и security reference как comparison для Modules 4
  and 5 repeatable gates.
- Canonical URL: [GitHub Actions documentation](https://docs.github.com/en/actions/reference)
- Checked: 2026-07-13.

Ограничения:

- GitHub-hosted behavior, runners и secrets are platform-specific; CI output не
  является product approval и не обязателен для offline course route.

### Anthropic Claude Platform

Ссылки:

- [Anthropic Claude Platform docs](https://platform.claude.com/docs/en/home)
- [Anthropic courses](https://github.com/anthropics/courses)

Использовать для:

- tool use, prompt engineering, prompt evaluation;
- Claude API, Messages API и managed agents;
- подходы к оценке, safety и production-ready использованию LLM.

Разделы курса:

- инструкции и промпты как часть control plane;
- tool use;
- evaluation;
- safety and review.

Ограничения:

- Claude-специфичные рекомендации нельзя переносить как универсальные без сверки с другими официальными источниками;
- материалы курсов Tier 2 должны быть адаптированы в русскоязычные самодостаточные уроки.

### Model Context Protocol specification

- Роль: Tier 1 protocol specification для external context и tool integrations.
- Scope: hosts, clients, servers, resources, prompts, tools, consent и transport
  boundaries для Modules 1-3.
- Canonical URL: [MCP specification](https://modelcontextprotocol.io/specification/latest)
- Checked: 2026-07-13.

Ссылки:

- [MCP official docs](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Model Context Protocol GitHub organization](https://github.com/modelcontextprotocol)

Использовать для:

- архитектуры MCP: hosts, clients, servers;
- локальных и удаленных MCP-серверов;
- SDK, debugging, inspector и example servers;
- security, authorization и versioning;
- подключения инструментов и внешнего контекста к агентам.

Разделы курса:

- контекст;
- инструменты;
- agent integrations;
- security gates;
- capstone.

Ограничения:

- версии протокола, transport и security-рекомендации должны сверяться с текущей официальной спецификацией;
- учебные упражнения должны объяснять MCP на русском без требования читать спецификацию целиком.

### Google Agent Development Kit documentation

- Роль: Tier 1 framework documentation для managed, graph и multi-agent workflows.
- Scope: tools, workflows, evaluation, tracing и safety examples для capstone
  comparison; не mandatory implementation path.
- Canonical URL: [Google Agent Development Kit documentation](https://adk.dev/)
- Checked: 2026-07-13.

Ссылки:

- [Gemini API docs](https://ai.google.dev/gemini-api/docs)
- [Google Agent Development Kit docs](https://adk.dev/)

Использовать для:

- Gemini API, function calling, tools, code execution, computer use;
- agent development kit и managed agent workflows;
- grounding, RAG, search, safety и release notes;
- сравнение cloud-agent подходов с локальными и repo-first workflow.

Разделы курса:

- LLM-интеграции;
- tools and actions;
- RAG и grounding;
- production patterns;
- safety.

Ограничения:

- Google Cloud-зависимые упражнения не должны становиться обязательными для основного маршрута, если курс не включает полный локальный или sandbox-путь;
- Google-специфичные термины нужно объяснять как частный вариант общего паттерна.

### Microsoft Foundry, Semantic Kernel и GitHub Copilot

Ссылки:

- [Microsoft Foundry docs](https://learn.microsoft.com/en-us/azure/foundry/)
- [Semantic Kernel docs](https://learn.microsoft.com/en-us/semantic-kernel/overview/)
- [GitHub Copilot docs](https://docs.github.com/en/copilot)

Использовать для:

- enterprise control plane для AI apps and agents;
- governance, observability, evaluation, content safety;
- plugin/function calling модель Semantic Kernel;
- Copilot agent workflows, hooks, skills, MCP servers и sandbox-подходы.

Разделы курса:

- enterprise agent workflow;
- roles and plugins;
- evaluation and observability;
- security and governance;
- code review agents.

Ограничения:

- Microsoft-продуктовые сценарии нужно отделять от общих инженерных принципов;
- cloud-specific и license-specific поведение должно быть помечено в уроках явно.

### Hugging Face, Transformers и smolagents

Ссылки:

- [Hugging Face documentation hub](https://huggingface.co/docs)
- [smolagents documentation](https://huggingface.co/docs/smolagents/index)

Использовать для:

- open-source model workflows;
- Transformers, datasets, tokenizers, evaluate, accelerate, TRL;
- lightweight agent framework smolagents;
- практики вокруг локальных и открытых моделей.

Разделы курса:

- основы моделей;
- локальные эксперименты;
- agent framework comparison;
- evaluation.

Ограничения:

- документация Hugging Face является источником истины для экосистемы Hugging Face, но не для всех agent architecture решений;
- deep learning-часть должна оставаться прикладной и не превращать курс в общий курс ML.

### LangGraph и LlamaIndex

Ссылки:

- [LangGraph documentation](https://docs.langchain.com/oss/python/langgraph/overview)
- [LlamaIndex documentation](https://developers.llamaindex.ai/python/framework/)

Использовать для:

- stateful agent workflows;
- graph-based orchestration;
- memory, human-in-the-loop, tools и streaming;
- RAG, indexing, retrieval, agents over data;
- tracing, debugging and evaluation.

Разделы курса:

- workflow orchestration;
- context and retrieval;
- multi-step agents;
- evaluation;
- capstone.

Ограничения:

- framework abstractions нужно переводить в общие понятия control plane;
- API-примеры проверяются по текущей документации перед включением в задания.

### Python, testing и QA-инструменты

Ссылки:

- [Python documentation](https://docs.python.org/3/)
- [pytest documentation](https://docs.pytest.org/)
- [Playwright for Python](https://playwright.dev/python/docs/intro)

Использовать для:

- базовой реализации учебных scripts и checks;
- тестирования agent workflow;
- browser-driven QA;
- формализации verification gates.

Разделы курса:

- практические задания;
- QA/SDET workflows;
- test gates;
- capstone project.

Ограничения:

- курс не должен превращаться в общий курс Python или test automation;
- объяснять нужно только тот минимум, который нужен для agent control plane.

### Базовые ML и neural network источники

Ссылки:

- [PyTorch documentation](https://pytorch.org/docs/stable/index.html)
- [TensorFlow API documentation](https://www.tensorflow.org/api_docs)
- [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html)

Использовать для:

- минимального объяснения моделей, inference, embeddings, evaluation;
- различения classic ML, deep learning и LLM-подходов;
- foundation-модулей для студентов без ML-бэкграунда.

Разделы курса:

- вводная теория;
- ограничения моделей;
- evaluation;
- терминология.

Ограничения:

- это вспомогательный слой, а не ядро курса;
- обязательная теория должна быть сжата до того, что нужно для понимания агентных систем.

### Локальные модели и serving

Ссылки:

- [Ollama documentation](https://docs.ollama.com/)
- [vLLM documentation](https://docs.vllm.ai/)
- [llama-cpp-python documentation](https://llama-cpp-python.readthedocs.io/)

Использовать для:

- локального запуска моделей;
- offline experiments;
- inference serving;
- сравнения cloud и local constraints.

Разделы курса:

- модели и runtime;
- локальные лабораторные работы;
- production constraints;
- capstone alternatives.

Ограничения:

- локальные runtime-задания должны быть optional, если для них нет стабильного минимального окружения;
- hardware-specific детали нужно явно отделять от общих принципов.

## Tier 2: официальные курсы и учебные репозитории

### Microsoft AI Agents for Beginners

Ссылка: [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners)

Использовать для:

- карты тем по agent design patterns;
- tool use, RAG, planning, multi-agent, metacognition;
- trustworthy agents, production, protocols, context engineering, memory and security.

Ограничения:

- не делать внешнее прохождение курса обязательным;
- Microsoft-specific материалы адаптировать в общие русскоязычные уроки.

### Hugging Face Agents Course

Ссылка: [huggingface/agents-course](https://github.com/huggingface/agents-course)

Использовать для:

- определения базовых понятий agent, tool, observation, action;
- сравнения smolagents, LangGraph и LlamaIndex;
- observability, evaluation, Agentic RAG и финального проекта.

Ограничения:

- курс является источником структуры и упражнений, но API-поведение нужно сверять с Tier 1;
- англоязычные объяснения адаптируются на русский.

### Microsoft MCP for Beginners

Ссылка: [microsoft/mcp-for-beginners](https://github.com/microsoft/mcp-for-beginners)

Использовать для:

- учебной декомпозиции MCP;
- cross-language examples;
- modular, scalable and secure AI workflows.

Ограничения:

- спецификация MCP из Tier 1 важнее учебного пересказа;
- примеры на разных языках использовать выборочно.

### LangChain Academy

Ссылка: [langchain-ai/langchain-academy](https://github.com/langchain-ai/langchain-academy)

Использовать для:

- учебной последовательности по LangGraph;
- notebooks and hands-on workflows;
- graph thinking для stateful agents.

Ограничения:

- LangGraph-специфичные паттерны нельзя подавать как единственный способ строить agent control plane;
- кодовые примеры проверяются по актуальной документации LangGraph.

### Anthropic courses

Ссылка: [anthropics/courses](https://github.com/anthropics/courses)

Использовать для:

- Claude API fundamentals;
- prompt engineering;
- real-world prompting;
- prompt evaluations;
- tool use.

Ограничения:

- использовать как official course source, но не как обязательный внешний учебник;
- устаревшие model-specific фрагменты перепроверять.

### Microsoft Generative AI for Beginners

Ссылка: [microsoft/generative-ai-for-beginners](https://github.com/microsoft/generative-ai-for-beginners)

Использовать для:

- фундамента generative AI applications;
- базовых упражнений и структуры beginner-friendly уроков;
- сравнения с agent-specific курсами.

Ограничения:

- брать только темы, поддерживающие agent control plane;
- не дублировать весь общий GenAI-курс.

### Microsoft AI for Beginners

Ссылка: [microsoft/AI-For-Beginners](https://github.com/microsoft/AI-For-Beginners)

Использовать для:

- базового объяснения AI, neural networks, deep learning and ethics;
- foundation-материалов для студентов без ML-базы.

Ограничения:

- использовать выборочно;
- обязательная теория должна быть короче и связана с агентными системами.

### Hugging Face Course

Ссылка: [huggingface/course](https://github.com/huggingface/course)

Использовать для:

- foundation по Transformers ecosystem;
- tokenizers, datasets, models and fine-tuning context;
- понимания open-source LLM tooling.

Ограничения:

- не превращать курс в курс по Transformers;
- включать только теорию, нужную для control-plane инженера.

### Microsoft ML for Beginners

Ссылка: [microsoft/ML-For-Beginners](https://github.com/microsoft/ML-For-Beginners)

Использовать для:

- минимального classic ML контекста;
- педагогической структуры: lesson, quiz, assignment, challenge;
- объяснения отличий classic ML от LLM/agentic workflows.

Ограничения:

- classic ML не является ядром курса;
- deep learning и agent tooling должны идти из профильных источников.

## Tier 3: официальные примеры, cookbook и templates

### OpenAI Cookbook

Ссылка: [openai/openai-cookbook](https://github.com/openai/openai-cookbook)

Использовать для:

- практических implementation examples;
- patterns around tools, retrieval, evaluation and structured outputs;
- идей для упражнений.

Ограничения:

- cookbook-пример не заменяет официальную документацию;
- перед включением кода в курс нужно сверить API с Tier 1.

### GoogleCloudPlatform generative-ai

Ссылка: [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai)

Использовать для:

- Gemini and Google Cloud notebooks;
- RAG, grounding, function calling and setup examples;
- sample applications.

Ограничения:

- cloud-specific настройки не должны быть обязательными без полного объяснения;
- демонстрационные notebooks нужно адаптировать в воспроизводимые русскоязычные задания.

### Google ADK Samples

Ссылка: [google/adk-samples](https://github.com/google/adk-samples)

Использовать для:

- examples of ADK agents;
- multi-agent and tool workflows;
- понимания практического применения ADK.

Ограничения:

- sample repo не является нормативной спецификацией;
- все production-выводы проверяются по ADK docs.

### Google Agent Starter Pack

Ссылка: [GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)

Использовать для:

- production-oriented templates;
- CI/CD, evaluation, observability and deployment ideas;
- infrastructure patterns for agent applications.

Ограничения:

- templates не должны задавать обязательный стек курса;
- production-практики нужно объяснять через общие принципы и подтверждать документацией.

### Anthropic prompt engineering tutorial

Ссылка: [anthropics/prompt-eng-interactive-tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)

Использовать для:

- prompt exercises;
- разделения инструкций и данных;
- работы с hallucinations, chaining, tools, search and retrieval.

Ограничения:

- model-specific рекомендации нужно перепроверять;
- prompt engineering должен быть встроен в control plane, а не подаваться как отдельная магия.

### Microsoft Copilot Camp

Ссылка: [microsoft/copilot-camp](https://github.com/microsoft/copilot-camp)

Использовать для:

- hands-on labs вокруг Microsoft 365 Copilot and custom engine agents;
- Microsoft-specific agent scenarios;
- примеров enterprise-интеграций.

Ограничения:

- это Microsoft-specific практикум, а не универсальная программа курса;
- использовать только как дополнительный источник примеров.

## Правила обновления каталога

1. Каждый новый обязательный урок должен указывать источники, на которые он опирается.
2. Для каждого важного источника нужно фиксировать дату проверки.
3. Если источник Tier 2 или Tier 3 описывает поведение API, рядом должен быть найден Tier 1 источник, подтверждающий это поведение.
4. Если источники конфликтуют, приоритет такой: текущая официальная документация и API reference, затем changelog/release notes, затем официальный курс, затем официальный пример.
5. Если официальный источник изменился, нужно обновить не только ссылку, но и русскоязычную теорию внутри курса.
6. Нельзя делать внешнюю ссылку обязательным условием прохождения основного маршрута.

## Чеклист добавления источника

Перед добавлением нового источника ответить:

- Это официальный источник?
- Это нормативная документация, учебный курс или пример?
- Какая часть курса от него зависит?
- Какой источник Tier 1 подтверждает ключевые утверждения?
- Не создает ли источник vendor lock-in для основного маршрута?
- Есть ли в курсе русскоязычное самодостаточное объяснение темы?
- Зафиксирована ли дата проверки?
