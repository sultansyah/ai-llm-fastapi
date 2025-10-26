from fastapi import FastAPI, Depends, HTTPException, Header, Request
import ollama
import asyncio
import os
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from chat import ChatService
from vector import VectorStoreService

load_dotenv()

API_KEY_CREDITS = {os.getenv("API_KEY"): 5}

app = FastAPI()

templates = Jinja2Templates(directory="templates")

vector_service = VectorStoreService()
chat_service = ChatService()


def verify_api_key(x_api_key: str = Header(None)):
    credits = API_KEY_CREDITS.get(x_api_key, 0)
    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API key, or no credits")

    return x_api_key

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})

@app.post("/generate")
async def generate(prompt: str, x_api_key: str = Depends(verify_api_key)):
    API_KEY_CREDITS[x_api_key] -= 1

    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(
        None,
        ollama.chat,
        "gpt-oss:20b",  # model
        [{"role": "user", "content": prompt}]  # messages
    )

    return {"response": response["message"]["content"]}

@app.get("/chat")
async def chat(prompt: str):
    reviews = vector_service.query(prompt)
    return StreamingResponse(chat_service.streaming(reviews, prompt), media_type="text/event-stream")