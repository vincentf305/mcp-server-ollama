# MCP Server for Ollama

A Model Control Protocol server that allows Claude Desktop to communicate with Ollama LLM server.

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and configure as needed
3. Install dependencies: `pip install -r requirements.txt`
4. Run server: `python -m mcp_server`

## Docker

```bash
docker build -t mcp-server-ollama .
docker run -p 8000:8000 mcp-server-ollama
```

## Testing

```bash
pytest tests/
```