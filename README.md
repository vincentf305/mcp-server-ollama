# MCP Server for Ollama

A Model Control Protocol server that allows Claude Desktop to communicate with Ollama LLM server.

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and configure as needed
3. Install dependencies: `pip install -r requirements.txt`
4. Run server: `python -m src.mcp_server.server`

## Docker

### Building and Running

```bash
docker build -t mcp-server-ollama .
```

### Using with Claude Desktop

Edit the `claude_desktop_config.json` file with the following content:

```json
{
  "mcpServers": {
    "ollama-server": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp-server-ollama"]
    }
  }
}
```
