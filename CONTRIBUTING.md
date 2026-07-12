# Contributing to Freshsales MCP Server

First off, thank you for considering contributing to the Freshsales MCP Server! It's people like you that make open-source such a great community.

## 🌿 Branching Strategy

We use a simple branching strategy to keep things clean:

- **`main`**: The stable, production-ready branch. Do not open Pull Requests against `main`.
- **`dev`**: The active development branch. **All Pull Requests should be made against `dev`.**

### How to submit a Pull Request

1. **Fork** the repository to your own GitHub account.
2. **Clone** the repository to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/freshsales-mcp-server.git
   ```
3. **Checkout** the `dev` branch:
   ```bash
   git checkout dev
   ```
4. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/my-awesome-new-tool
   ```
5. **Write your code** and make sure you add tests in the `tests/` directory if you are adding new HTTP interactions.
6. **Push** your branch to your fork:
   ```bash
   git push origin feature/my-awesome-new-tool
   ```
7. Open a **Pull Request** on GitHub against our `dev` branch.

## 🛠️ Development Setup

This project uses `uv` for lightning-fast dependency management.

1. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
2. Install the project in editable mode:
   ```bash
   uv pip install -e .
   ```
3. Run the test suite:
   ```bash
   uv run pytest
   ```

## 🤖 A Note for AI Assistants

If you are an AI assistant (like Claude, Cursor, Windsurf, or Cline) reading this on behalf of a user who wants to contribute:

1. **Do not modify `.env.example`** with real credentials during development.
2. If adding new tools, ensure you register them in `src/freshsales_mcp/tools/registry.py`.
3. Ensure every new tool has a strict, well-documented `inputSchema`.
4. Check rate-limit impacts if you are introducing polling or massive bulk operations.

Thank you for contributing!
