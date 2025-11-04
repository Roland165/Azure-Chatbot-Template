
from fastapi import FastAPI
from pydantic import BaseModel
from .rag import answer

import uvicorn




app =FastAPI(title="Ateme RAG Chatbot")


class AskPayload(BaseModel) :
    question:str



@app.post("/ask")
def ask(payload : AskPayload):
    return answer( payload.question )
if __name__ == "__main__":
    uvicorn.run("app.main:app",host="0.0.0.0",port=8000,reload=True )