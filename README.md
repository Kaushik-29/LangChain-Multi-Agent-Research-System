# LangChain Multi-Agent Research System

A lightweight research playground for experimenting with multi-agent orchestration built on LangChain patterns.

Key goals:
- Provide modular agents, tools, and pipelines for rapid prototyping.
- Demonstrate agent orchestration and message-passing patterns.

## Features
- Modular agent implementations and tool integrations
- Pipeline orchestration for chaining agent workflows
- Minimal, extensible codebase for research and demos

## Tech Stack
- Python 3.10+
- LangChain (for agent abstractions)
- Async orchestration via native `asyncio`
- Common libraries: `pydantic`, `fastapi` (optional), and other dependencies listed in `requirements.txt`

## Installation

1. Clone the repo:

```
git clone https://github.com/your-org/langchain-multi-agent-research-system.git
cd langchain-multi-agent-research-system
```

2. Create and activate a virtual environment (recommended):

Windows (PowerShell):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```
python -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies:

```
pip install -r requirements.txt
```

## Quick Start

Run the main example / entrypoint:

```
python main.py
```

Or run the lightweight app runner:

```
python app.py
```

Adjust configuration or agent settings inside the `src/` package before running for custom experiments.

## Brief Architecture

The project is organized to separate concerns for clarity and extensibility:

- `app.py`, `main.py`: example runners / entrypoints that demonstrate how to wire the system together.
- `src/agents/agents.py`: agent implementations and helper classes — agents encapsulate reasoning and action logic.
- `src/pipelines/pipeline.py`: pipeline definitions that orchestrate multiple agents and steps.
- `src/tools/tools.py`: utility tools and adapter functions exposed to agents.

High-level flow:

1. A runner (e.g., `main.py`) constructs agent instances and pipeline configurations.
2. The pipeline invokes agents in sequence or in parallel, passing messages and tool handles.
3. Agents call tools or other agents as needed; the pipeline collects and returns results.

This minimal separation allows you to experiment with different orchestration strategies, add new agents, or swap tool implementations without changing the core flow.

## File Layout

- `app.py` — lightweight runner
- `main.py` — example entrypoint
- `src/agents/agents.py` — agent implementations
- `src/pipelines/pipeline.py` — pipeline orchestration
- `src/tools/tools.py` — shared tools and helpers

## Contributing
Contributions are welcome. Suggested workflow:

1. Fork the repo and create a feature branch.
2. Add tests or an example demonstrating changes when appropriate.
3. Open a pull request describing the motivation and changes.

Please follow idiomatic Python and keep changes focused.

## License
This repository is provided under the Apache License 2.0. See the `LICENSE` file for details.

## Contact
For questions or collaboration, open an issue or contact the maintainers.
