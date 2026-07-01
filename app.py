import json

from fastapi import FastAPI
from pydantic import BaseModel

from agent import Agent
from llm import LLM
from vector_db import vectordb


app = FastAPI()

agent = Agent(LLM())

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


class Recommendation(BaseModel):
    name: str
    url: str
    description: str

class Comparison(BaseModel):
    reply: str
    end_of_conversation: bool


class ChatResponse(BaseModel):
    reply: str
    recommendations: list[Recommendation] | None
    end_of_conversation: bool


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    
    history = [m.model_dump() for m in request.messages]
    reply = agent.run(history)
    if isinstance(reply, dict):
        return ChatResponse(
            reply=reply.get("reply", str(reply)),
            recommendations=None,
            end_of_conversation=False,
        )

    try:
        data = json.loads(reply)

        query = " ".join([
            data["role"],
            *data["competencies"],
            *data["job_level"],
            *data["test_type_keys"],
        ])

        results = vectordb.query(
            texts=[query],
            collection_name="catalog_collection",
            n_results=5,
        )

        recommendations = []

        for doc, meta in zip(
            results["documents"][0],
            results["metadatas"][0],
        ):
            recommendations.append(
                Recommendation(
                    name=meta["name"],
                    url=meta["link"],
                    description=doc,
                )
            )

        return ChatResponse(
            reply="Based on your requirements, here are the best assessments.",
            recommendations=recommendations,
            end_of_conversation=True,
        )

    except json.JSONDecodeError:

        return ChatResponse(
            reply=reply,
            recommendations=None,
            end_of_conversation=False,
        )