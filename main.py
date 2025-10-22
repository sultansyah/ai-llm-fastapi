from fastapi import FastAPI, Depends, HTTPException, Header
import ollama
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_CREDITS = {os.getenv("API_KEY"): 5}

app = FastAPI()

def verify_api_key(x_api_key: str = Header(None)):
    credits = API_KEY_CREDITS.get(x_api_key, 0)
    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API key, or no credits")

    return x_api_key

@app.post("/generate")
async def generate(prompt: str, x_api_key: str = Depends(verify_api_key)):
    print(x_api_key)
    API_KEY_CREDITS[x_api_key] -= 1

    print(prompt)
    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(
        None,
        ollama.chat,
        "gpt-oss:20b",  # model
        [{"role": "user", "content": prompt}]  # messages
    )

    return {"response": response["message"]["content"]}
