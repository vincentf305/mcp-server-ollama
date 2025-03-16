# MCP Server for Ollama

A Model Control Protocol server that allows Claude Desktop to communicate with Ollama LLM server.

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and configure as needed
3. Install dependencies: `pip install -r requirements.txt`

### Using with Claude Desktop

Edit the `claude_desktop_config.json` file with the following content, change path-to-mcp-server to the path of this repo:

```json
{
  "mcpServers": {
    "ollama-server": {
      "command": "python",
      "args": ["-m", "src.mcp_server.server"],
      "env": {
        "PYTHONPATH": "path-to-mcp-server"
      }
    }
  }
}
```
