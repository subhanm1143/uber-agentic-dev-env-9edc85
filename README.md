# Uber | Agentic Developer Environment (AI Coding Assistant Platform)

An intermediate capstone that grows a real agentic developer platform from durable state up. You model projects/tasks/runs in Postgres behind repositories, expose an async orchestrator API, add a no-embeddings codebase retriever with Redis caching, wrap OpenAI/Claude behind a resilient provider abstraction, then build the LangGraph planner→codegen→executor loop with bounded iteration. You give agents a Docker sandbox to run commands safely, an atomic patch-apply layer to turn suggestions into real edits, a Redis-backed run worker so HTTP stays responsive, structured event/metrics observability, and finally a CLI and a React timeline UI to drive and watch runs.

Built step-by-step with [KhwajaLabs Build](https://khwajalabs.com).

## Stack
- Python
- LangGraph
- Postgres
- Redis
- Docker
- FastAPI
- OpenAI
- Claude
- TypeScript
- React
