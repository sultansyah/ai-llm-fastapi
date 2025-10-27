from fastapi import FastAPI, Request
import os
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from chat import ChatService
from vector import VectorStoreService
from short_memory import ShortMemoryService

load_dotenv()

MODEL = os.getenv("MODEL")
CSV_PATH = os.getenv("CSV_PATH")
DB_PATH = os.getenv("DB_PATH")
MODEL_EMBEDDING = os.getenv("MODEL_EMBEDDING")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
SEARCH_TYPE = os.getenv("SEARCH_TYPE")
SEARCH_KWARGS_K = os.getenv("SEARCH_KWARGS_K")
MAX_MEMORY = int(os.getenv("MAX_MEMORY"))

app = FastAPI()

templates = Jinja2Templates(directory="templates")

vector_service = VectorStoreService(
    csv_path=CSV_PATH,
    db_path=DB_PATH,
    model_embedding_name=MODEL_EMBEDDING,
    collection_name=COLLECTION_NAME,
    search_type=SEARCH_TYPE,
    search_kwargs={"k": int(SEARCH_KWARGS_K)},
)
chat_service = ChatService(model_name=MODEL)
short_memory = ShortMemoryService(max_memory=MAX_MEMORY)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})

def save_to_memory(content: str):
    print("save_to_memory = ", content)
    short_memory.append("assistant", content)

@app.get("/chat")
async def chat(prompt: str):
    short_memory.append("user", prompt)
    
    final_prompt = short_memory.build_prompt(MAX_MEMORY)
    
    print("final_prompt = ", final_prompt)
    
    reviews = vector_service.query(prompt)
    return StreamingResponse(chat_service.streaming(reviews, final_prompt, save_to_memory), media_type="text/event-stream")
