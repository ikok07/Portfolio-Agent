import uuid
from typing import Annotated

from clerk_backend_api import User
from fastapi import APIRouter
from fastapi.params import Depends, Query
from langchain_core.messages import HumanMessage, AIMessageChunk
from langchain_core.runnables import RunnableConfig
from starlette.responses import StreamingResponse

from src.api.dependencies.protect import protect_dependency

from src.agents.chatbot.chatbot_agent import graph, State
from src.api.models.db import Profile

router = APIRouter()

@router.get("/ask")
async def ask_agent(prompt: Annotated[str, Query()], userdata: tuple[User, Profile] = Depends(protect_dependency)):
    async def generate_response():
        async for chunk, metadata in graph.astream(State(messages=[HumanMessage(prompt)], user_id=userdata[0].id), stream_mode="messages", config=RunnableConfig(configurable={"thread_id": str(uuid.uuid4())})):
            if not isinstance(chunk, AIMessageChunk):
                continue
            message_chunk: AIMessageChunk = chunk
            if  message_chunk.content :
                yield f"{message_chunk.content}\n"

    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream"
    )
