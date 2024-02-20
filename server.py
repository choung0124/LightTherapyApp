from fastapi import FastAPI, UploadFile, File, WebSocket, Request, Depends
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from pathlib import Path
from Inference import GetValue
from DailyPrompts import AgePrompt, Introduction, GenderPrompt

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/start_session/")

class Chat(BaseModel):
    text: str
    uid: str
    metric: str
    
@app.post("/chat/")
async def chat(chat: Chat):
    if chat.metric == "age":
        prompt = AgePrompt.format(Introduction=Introduction, Dialogue=chat.text)
    elif chat.metric == "gender":
        prompt = GenderPrompt.format(Introduction=Introduction, Dialogue=chat.text)
    else:
        return {"error": "Invalid metric"}

    response = GetValue(prompt)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)