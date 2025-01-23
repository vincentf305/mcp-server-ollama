import uvicorn
from .config import settings

def main():
    uvicorn.run(
        "mcp_server.server:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )

if __name__ == "__main__":
    main()