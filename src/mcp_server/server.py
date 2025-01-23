from fastapi import FastAPI, HTTPException
import httpx
from .models import ChatRequest, ChatResponse
from .config import settings

app = FastAPI()

async def format_ollama_request(chat_request: ChatRequest) -> dict:
    messages = [{
        "role": msg.role,
        "content": msg.content
    } for msg in chat_request.messages]

    return {
        "model": settings.model_name,
        "messages": messages,
        "stream": False,
        "temperature": chat_request.temperature
    }

@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    try:
        async with httpx.AsyncClient() as client:
            ollama_request = await format_ollama_request(request)
            response = await client.post(
                f"{settings.ollama_base_url}/api/chat",
                json=ollama_request,
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return ChatResponse(content=data["message"]["content"])
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))