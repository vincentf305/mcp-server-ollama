import asyncio
import click
import httpx
import logging
import sys

import mcp
import mcp.types as types

from mcp.server import Server
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions

from .config import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def serve() -> Server:
    server = Server("ollama-server")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="ask-ollama",
                description="Ask models running in Ollama a question",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Ask assistant"},
                        "model": {"type": "string", "default": "llama3", "enum": ["llama3","llama3.2"]},
                        "temperature": {"type": "number", "default": 0.7, "minimum": 0, "maximum": 2},
                        "max_tokens": {"type": "integer", "default": 500, "minimum": 1, "maximum": 4000}
                    },
                    "required": ["query"]
                }
            )
        ]

    @server.call_tool()
    async def handle_tool_call(name: str, arguments: dict | None) -> list[types.TextContent]:
        try:
            if not arguments:
                raise ValueError("No arguments provided")

            if name == "ask-ollama":
                logger.info(f"Calling tool: {name} with arguments: {arguments}")
                query=arguments["query"]
                model=arguments.get("model", settings.model_name)
                temperature=arguments.get("temperature", 0.7)
                max_tokens=arguments.get("max_tokens", 500)

                async with httpx.AsyncClient(verify=False) as client:
                    ollama_request =  {
                        "model": model,
                        "messages":  [{"role": "user","content": query}],
                        "stream": False,
                        "temperature": temperature,
                        "max_tokens": max_tokens    
                    }
                    logger.debug(f"Ollama request: {ollama_request}")
                    response = await client.post(
                        f"{settings.ollama_base_url}/api/chat",
                        json=ollama_request,
                        timeout=30.0
                    )
                response.raise_for_status()
                data = response.json()
                logger.info(f"Ollama response: {data}")
                chat_response = data["message"]["content"]
                
                return [types.TextContent(type="text", text=f"Ollama Response:\n{chat_response}")]

            raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            logger.error(f"Tool call failed: {str(e)}")
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    return server

@click.command()
def main():
    try:
        async def _run():
            async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
                server = serve()
                await server.run(
                    read_stream, write_stream,
                    InitializationOptions(
                        server_name="ollama-server",
                        server_version="0.1.0",
                        capabilities=server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={}
                        )
                    )
                )
        asyncio.run(_run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.exception("Server failed")
        sys.exit(1)

if __name__ == "__main__":
    main()