from datetime import datetime

from fastapi import FastAPI, status
from pydantic import BaseModel, Field, ValidationError

app = FastAPI()


# 1.3 Enforce field constraint
class Message(BaseModel):
    sender: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    # description: str | None = Field(
    #     default=None, title="The description of the item", max_length=300
    # )


class Conversation(BaseModel):
    id: int
    title: str
    messages: list[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)


conversations: list[Conversation] = []


@app.get("/")
def main():
    return {"message": "Welcome home", "status": status.HTTP_200_OK}


def findConversation(id: int):
    if conversations:
        conversation = next(conv for conv in conversations if conv.id == id)  # type: ignore
        if conversation:
            return conversation
        else:
            return None
    return None


@app.get("/conversation/{id}")
def GetConversation(id: int):
    conversation = findConversation(id)
    if conversation:
        return {"data": conversation}
    return {"message": "No conversation"}


@app.post("/new", status_code=status.HTTP_201_CREATED, response_model=Conversation)
async def CreateConversation(conversation: Conversation):
    try:
        conversations.append(conversation)
        return conversation

    except ValidationError as e:
        print("Vallidation error:", e)


@app.post("/conversation/{id}/chat", status_code=status.HTTP_201_CREATED)
async def SendMessage(id: int, message: Message):
    try:
        conversation = findConversation(id)
        if conversation:
            conversation.messages.append(message)
            return {"data": conversation}
        return {"message": "No conversation"}

    except ValidationError as e:
        print("Validation error:", e)
