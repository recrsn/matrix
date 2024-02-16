# Matrix

A cli-based prompt manager for LLMs. Supports OpenAI (GPT-3, ChatGPT, GPT-4 etc),
Anyscale Endpoints, vLLM and any other LLMs that support the OpenAI API.

## Features

- Provides a simple and easy to use interface for interacting with LLMs
- Manages and stores API tokens for multiple providers
- Supports multiple LLMs
- Manages and stores reusable prompts

## Quick Start

Register a LLM provider and run a prompt.

```
matrix providers register openai
Name (leave empty to use alias): OpenAI
URL: https://api.openai.com/v1
Token (leave empty if not required): <your-openai-api-token>
Registered provider OpenAI with alias openai

matrix prompts run --provider openai --model gpt-4-turbo-preview generic --stream
You: Who are you?
🤖 Assistant: I am an AI developed by OpenAI, designed to assist you with a wide range of queries and tasks. Whether you have questions, need information, or require help with something specific, I'm here to provide assistance. How can I help you today?
You: ^D
```

## Concepts

- **Provider**: A provider is a service that provides access to an LLM.
    For example, OpenAI, Anyscale,etc.
- **Prompt**: A system prompt that is used to start a conversation with an LLM.
- **Assistant**: A binding of a provider and an LLM to a prompt for a specific use case.

## Commands

- `matrix providers`: Manage providers
- `matrix assistants`: Manage assistants
- `matrix prompts`: Manage prompts

See `matrix --help` for more details.

## Configuration

Matrix stores its configuration as INI files in
    - `~/Applicaion Support/matrix/` on MacOS
    - `~/.config/matrix/` on Linux
    - `%APPDATA%\matrix\` on Windows

## License

BSD-2-Clause License

See [LICENSE](LICENSE) for more details.
