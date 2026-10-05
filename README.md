# AI API Testing

A lightweight Python test framework for validating large language model (LLM) APIs against contract, reliability, safety, and error-handling expectations.

This project uses pytest, httpx, Pydantic, and JSON Schema to exercise a Groq OpenAI-compatible chat completions endpoint and verify that responses are valid, stable, and safe under real-world adversarial prompts.

## Why this framework exists

LLM APIs are often treated as black boxes, but they still need robust validation. This framework helps answer questions such as:

- Does the API return the expected OpenAI-compatible response structure?
- Are error responses correctly shaped when inputs are invalid?
- Does the model refuse harmful or malicious prompts?
- Are outputs reliable across repeated runs?
- Does the system behave predictably under temperature and prompt variation?

## Core features

- Contract validation for chat completion responses
- JSON Schema and Pydantic model validation
- Live API testing against a Groq-hosted OpenAI-compatible endpoint
- Negative testing for invalid inputs and malformed requests
- Prompt injection and safety checks
- Non-determinism and accuracy checks for quality benchmarking
- Allure reporting for test output and CI publishing
- GitHub Actions-based automation for repeatable test execution

## Project structure

```text
.
├── .env.example                 # Example environment variables
├── .github/
│   └── workflows/
│       └── ci.yml               # CI pipeline for running tests and publishing Allure
├── src/
│   └── ai_api_testing/
│       ├── __init__.py          # Package entry point
│       ├── config.py            # Environment settings
│       └── schemas.py           # Pydantic models for API contract validation
├── tests/
│   ├── conftest.py             # Shared pytest fixtures and HTTP client setup
│   ├── test_contract.py        # Response shape and schema validation
│   ├── test_errors.py          # Error response validation
│   ├── test_negative.py        # Prompt injection and refusal checks
│   ├── test_nondeterminism.py  # Reliability/accuracy and temperature checks
│   ├── test_smoke.py          # Basic smoke test
│   └── ...
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

## Framework behavior

The framework centers around a reusable HTTP client fixture defined in `tests/conftest.py`:

- Uses `httpx.Client` with a configured base URL
- Injects the API key from environment settings
- Sends requests to `/chat/completions`
- Validates responses using `ChatCompletion` and `ErrorResponse` models
- Skips tests safely when the provider returns rate-limit errors (HTTP 429)

The configuration layer in `src/ai_api_testing/config.py` reads values from `.env` and exposes:

- `GROQ_API_KEY`
- `MODEL_NAME` (defaults to `openai/gpt-oss-120b`)
- `BASE_URL` (defaults to Groq's OpenAI-compatible endpoint)
- `TIMEOUT_SECONDS`

## Test categories

The suite is organized around pytest markers:

- `live`: calls the real API; slower and may consume quota
- `negative`: tests invalid or adversarial inputs
- `slow`: exercises large or expensive prompts

Examples:

- `test_contract.py`: checks status code, content type, response schema, token accounting, and model mapping
- `test_errors.py`: verifies 400/401 handling and validation failures
- `test_negative.py`: attempts prompt injection, harmful behavior, and ambiguity handling
- `test_nondeterminism.py`: evaluates output consistency and creative variance under different temperatures
- `test_smoke.py`: basic end-to-end health check

## Setup

This project uses Python 3.14 and `uv` for dependency management.

1. Clone the repository.
2. Install dependencies:

```bash
uv sync --group dev
```

3. Copy the example environment file:

```bash
cp .env.example .env
```

4. Add your Groq API key:

```dotenv
GROQ_API_KEY=your_key_here
MODEL_NAME=openai/gpt-oss-120b
```

## Running tests

Run the full suite:

```bash
uv run pytest tests/ -v --tb=short
```

Run only non-slow tests:

```bash
uv run pytest tests/ -v --tb=short -m "not slow"
```

Run a single test file:

```bash
uv run pytest tests/test_contract.py -q
```

Run only live tests:

```bash
uv run pytest tests/ -m live -v
```

## Allure reporting

The project is configured to generate Allure results automatically via pytest:

```bash
uv run pytest tests/ -v --tb=short --alluredir=allure-results
```

Generate a local HTML report:

```bash
allure generate allure-results --clean -o allure-report
```

Open the report:

```bash
allure open allure-report
```

## CI/CD

The repository includes a GitHub Actions workflow in `.github/workflows/ci.yml` that:

- checks out the repo
- installs dependencies with `uv`
- executes the pytest suite
- uploads raw Allure results as artifacts
- generates an HTML report
- publishes the report to GitHub Pages from the `gh-pages` branch

This makes the framework suitable for automated regression checks on pushes and pull requests to `main`.

## Dependencies

Core dependencies:

- `httpx`
- `jsonschema`
- `pydantic`
- `pydantic-settings`
- `python-dotenv`
- `tenacity`

Development dependencies:

- `pytest`
- `pytest-timeout`
- `respx`
- `ruff`
- `allure-pytest`

## Notes

- Keep your real API key in `.env` and do not commit it to source control.
- Some tests are intentionally live and may consume API quota or be rate-limited.
- The suite is useful for validating provider behavior, but it should be adapted to the specific model and API contract you are testing.

## License

This project does not currently declare a license in `pyproject.toml`, so verify repository policy before publishing or redistributing it externally.

## Summary

This repository is a practical, production-style test harness for checking whether an LLM API behaves as expected under contract, error, security, and reliability conditions. It is especially useful when integrating third-party or provider-backed chat models into real applications where correctness and safety matter.
