from typing import Annotated

import aiosqlite
from clerk_backend_api import User
from fastapi import APIRouter, Path
from fastapi.params import Depends
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from src.api.dependencies.protect import protect_dependency
from src.api.models.db import Profile, ChatbotSession
from src.api.models.response.generic import GenericResponse

router = APIRouter()

@router.get("/")
async def get_chatbot_sessions(userdata: tuple[User, Profile] = Depends(protect_dependency)):
    sessions = await ChatbotSession.filter(profile_id=userdata[0].id).all().values()
    return GenericResponse(data=sessions)

@router.post("/")
async def create_chatbot_session(userdata: tuple[User, Profile] = Depends(protect_dependency)):
    session = await ChatbotSession.create(
        profile = userdata[1],
    )

    return GenericResponse(data={"id": session.id, "name": session.name, "profile_id": session.profile.id, "created_at": session.created_at})

@router.delete("/{session_id}")
async def delete_chatbot_session(session_id: Annotated[str, Path()], userdata: tuple[User, Profile] = Depends(protect_dependency)):
    await ChatbotSession.filter(id=session_id, profile_id=userdata[0].id).delete()
    memory = AsyncSqliteSaver(conn=(await aiosqlite.connect("db/db.sqlite3")))
    await memory.adelete_thread(thread_id=session_id)
    return GenericResponse()
