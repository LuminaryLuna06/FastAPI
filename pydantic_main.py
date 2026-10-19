from datetime import datetime
from typing import Annotated

from fastapi import Body, FastAPI, status
from pydantic import BaseModel, Field, ValidationError, field_validator

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: str
    full_name: str | None = None

# Seperate RequestSchema and ResponseSchema
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> any:
    return user


# Recursive model
class RecursiveMessage(BaseModel):
    sender: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    replies: list["RecursiveMessage"] = []


# 1.3 Enforce field constraint
class Message(BaseModel):
    sender: Annotated[str, Field(min_length=3, max_length=50)]
    email: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Email not in correct format")
        return v.lower()

    # @model_validator(mode="after")
    # def passwords_match(self):
    #     if self.password != self.confirm_password:
    #         raise ValueError("mật khẩu nhập lại không khớp")
    #     return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sender": "Foo",
                    "email": "hello@gmail.com",
                    "content": "Hello World",
                    "created_at": "2026-10-19T22:19:44.637927",
                }
            ]
        }
    }


class Conversation(BaseModel):
    id: int
    title: str
    messages: list[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)


conversations: list[Conversation] = []


@app.get("/")
def main():
    return {"message": "Welcome home", "status": status.HTTP_200_OK}


def findConversation(id: int) -> Conversation | None:
    if conversations:
        # Add default value = None
        conversation = next((conv for conv in conversations if conv.id == id), None)
    return conversation


@app.get("/conversation/{id}")
def GetConversation(id: int):
    conversation = findConversation(id)
    if conversation:
        return {"data": conversation}
    return {"message": "No conversation"}


@app.post("/new", status_code=status.HTTP_201_CREATED, response_model=Conversation)
async def CreateConversation(
    conversation: Annotated[
        Conversation,
        Body(examples=[{"id": 1, "title": "Foo"}]),
    ],
) -> Conversation | None:
    try:
        conversations.append(conversation)
        return conversation

    except ValidationError as e:
        print("Vallidation error:", e)
        return None


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
