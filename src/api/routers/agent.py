from typing import Annotated

from clerk_backend_api import User
from fastapi import APIRouter, Body
from fastapi.params import Depends, Query
from langchain_core.messages import HumanMessage, AIMessageChunk
from langchain_core.runnables import RunnableConfig
from pydantic import Field, BaseModel
from starlette import status
from starlette.responses import StreamingResponse
from tortoise.exceptions import DoesNotExist

from src.api.dependencies.protect import protect_dependency

from src.agents.chatbot.chatbot_agent import chatbot_graph, State
from src.api.models.db import Profile, ChatbotSession
from src.api.models.errors.api_error import APIError

router = APIRouter()

class InvokeAgentBody(BaseModel):
    prompt: str = Field(min_length=1)
    session_id: str = Field(min_length=1)

@router.post("/invoke")
async def ask_agent(body: Annotated[InvokeAgentBody, Body()], userdata: tuple[User, Profile] = Depends(protect_dependency)):
    try:
        session = await ChatbotSession.get(id=body.session_id)
        async def generate_response():
            async for chunk, metadata in (await chatbot_graph()).astream(
                    State(
                        messages=[HumanMessage(body.prompt)],
                        user_id=userdata[0].id,
                        session_id=body.session_id,
                        session_name=session.name
                    ),
                    stream_mode="messages",
                    config=RunnableConfig(configurable={"thread_id": body.session_id})
            ):
                if not isinstance(chunk, AIMessageChunk):
                    continue
                message_chunk: AIMessageChunk = chunk
                if  message_chunk.content :
                    yield f"{message_chunk.content}\n"

        return StreamingResponse(
            generate_response(),
            media_type="text/plain"
        )
    except DoesNotExist:
        raise APIError(status_code=status.HTTP_400_BAD_REQUEST, message="Session not found")

