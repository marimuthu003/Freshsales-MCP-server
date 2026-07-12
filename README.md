<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Freshworks_logo_2021.svg/512px-Freshworks_logo_2021.svg.png" alt="Freshworks Logo" width="200" height="auto">
  
  # Freshsales CRM — Model Context Protocol (MCP) Server

  *Connect your AI Assistants (Claude, Cursor, Windsurf) directly to your Freshsales CRM data.*
  
  <p align="center">
    <a href="https://modelcontextprotocol.io"><img src="https://img.shields.io/badge/MCP-Compatible-blue.svg?style=for-the-badge&logo=anthropic" alt="MCP Compatible"></a>
    <img src="https://img.shields.io/badge/Python-3.12+-green.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+">
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-purple.svg?style=for-the-badge" alt="License: MIT"></a>
  </p>
</div>

<br>

Welcome to the **Freshsales MCP Server**! This open-source server implements the official [Model Context Protocol](https://modelcontextprotocol.io), allowing any compatible AI agent to securely interact with your Freshsales CRM.

Instead of writing custom API scripts or manually exporting CSVs, you can now simply ask your AI:
> *"What deals are currently in the 'Negotiation' stage?"*<br>
> *"Create a new contact for Jane Doe at Acme Corp and add a note saying we met at the conference."*<br>
> *"Summarize all recent activity for the contact m.scott@dundermifflin.com."*

---

## ✨ Enterprise-Ready Features

- **Massive Tool Suite (75+ Tools)**: Full CRUD support for Contacts, Accounts, Deals, Tasks, Notes, Activities, Documents, and Products.
- **Dynamic AI Discovery**: Deep, strict `inputSchema` definitions ensure AI models instantly understand required fields, eliminating hallucinated API requests.
- **Smart Rate Limiting**: Built-in exponential backoff (via `tenacity`) handles HTTP 429 errors gracefully so your AI never crashes during bulk operations.
- **Context-Window Protection**: Automatic pagination caps prevent large CRM databases from overloading the AI's memory.
- **Multiple Transports**: 
  - `stdio`: Seamless integration with AI IDEs (Cursor, Windsurf, Cline) and Desktop Apps (Claude).
  - `streamable-http` & `sse`: Built-in Starlette/Uvicorn support for scalable web deployments and agentic frameworks.

---

## 🚀 Quickstart Guide

### For Claude Desktop Users

1. Open your Claude Desktop configuration file:
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Add the Freshsales server configuration:

```json
{
  "mcpServers": {
    "freshsales": {
      "command": "uv",
      "args": ["run", "python", "-m", "freshsales_mcp", "--transport", "stdio"],
      "env": {
        "FRESHSALES_API_KEY": "YOUR_FRESHSALES_API_KEY",
        "FRESHSALES_DOMAIN": "yourcompany" 
      },
      "cwd": "C:\\path\\to\\freshsales_mcp"
    }
  }
}
```
*Note: Your `FRESHSALES_DOMAIN` should only be your subdomain (e.g., use `acme` instead of `acme.myfreshworks.com`).*

3. Restart Claude Desktop. You will see the 🔌 plug icon indicating the tools are loaded!

---

## ⚙️ Developer Installation

If you want to run the server standalone, test it locally, or deploy it to the cloud:

**Prerequisites:** 
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Recommended for ultra-fast dependency management)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/freshsales-mcp-server.git
cd freshsales-mcp-server

# 2. Set up environment variables
cp .env.example .env
# Edit .env and add your FRESHSALES_API_KEY and FRESHSALES_DOMAIN

# 3. Install the package
uv pip install -e .

# 4. Start the server (defaults to stdio)
python -m freshsales_mcp
```

### 🧪 Testing with the MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is the official interactive developer tool that lets you test all 75+ tools visually in your browser before you hook them up to an AI.

To run the inspector:
```bash
npx @modelcontextprotocol/inspector uv run python -m freshsales_mcp
```

1. The command will output a local URL (e.g., `http://localhost:5173`).
2. Open that URL in your browser and click **Connect**.
3. Navigate to the **Tools** tab to see the entire Freshsales integration.
4. Try clicking `freshsales_get_selectors`, enter `deal_stages`, and click **Run** to see real CRM data flow back!

---

## 🚝 Transport Modes

This server implements all three official MCP transport modes. You can switch between them using the `--transport` flag.

### 1. `stdio` (Default)
**Best for:** Local AI IDEs (Cursor, Windsurf, Cline) and Desktop Apps (Claude Desktop).
**How it works:** The AI communicates with the server directly through standard input/output streams. It is incredibly fast and requires no networking.
```bash
python -m freshsales_mcp --transport stdio
```

### 2. `streamable-http` (Modern Web)
**Best for:** Cloud deployments, scalable architectures, and the OpenAI Agents SDK.
**How it works:** The modern standard for running MCP servers over the internet. It uses standard HTTP requests and avoids the timeout issues of long-lived SSE connections.
```bash
# Starts a Uvicorn server on http://0.0.0.0:8080
python -m freshsales_mcp --transport streamable-http
```
*Note: You can change the port by setting `PORT=9090` in your `.env` file.*

### 3. `sse` (Legacy Web)
**Best for:** Older frameworks that specifically require Server-Sent Events.
**How it works:** Establishes a persistent, one-way connection from the server to the client using the `/messages/` endpoint.
```bash
python -m freshsales_mcp --transport sse
```

---

## 🛠️ Tool Architecture

The server exposes modular toolsets. The AI will intelligently chain these tools together to accomplish complex tasks.

- **Contacts & Accounts**: Full lifecycle management, including bulk upserts, owner assignments, and timeline activity retrieval.
- **Deals (Opportunities)**: Pipeline management, deal stage transitions, and CPQ document tracking.
- **Intelligent Lookup**: The `freshsales_search` and `freshsales_list_filters` tools allow the AI to dynamically find internal View IDs and UUIDs without user intervention.
- **Files & Documents**: Supports native multipart/form-data, allowing the AI to decode base64 strings and upload binary files/attachments directly to CRM records.

---

## 🤝 Contributing

We welcome community contributions! Whether you're fixing a bug, adding a new Freshsales endpoint, or optimizing the tool schemas for better AI reasoning, your help is appreciated.

Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to set up your environment, our branching strategy (`dev` vs `main`), and how to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
