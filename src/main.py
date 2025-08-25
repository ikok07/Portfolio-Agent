from dotenv import load_dotenv

from src.api.models.db import Company
from src.config.tortoise import TORTOISE_CONFIG

load_dotenv()

from src.api.models.services.vector_store import VectorStore
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from tortoise import Tortoise

from src.api.models.errors.api_error import APIError
from src.api.routers import clerk_auth, agent, vector_store

VectorStore.semantic_search(collection_name="user-files", texts=["What is the main product that I&M NextGen develop?", "What is Cray?"], user_id="user_31lkhOoDx5okXNybqQohOMhQxwX")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(
        config=TORTOISE_CONFIG
    )
    await Tortoise.generate_schemas(safe=True)
    print("ORM Initialized")
    yield
    print("ORM De-Initialized")
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)
app.include_router(clerk_auth.router, prefix="/webhooks/clerk", tags=["Clerk Webhooks"])
app.include_router(agent.router, prefix="/agent", tags=["Agent"])

app.include_router(vector_store.router, prefix="/vector-store", tags=["Vector Store"])

@app.exception_handler(APIError)
async def api_error_handler(req: Request, err: APIError):
    """ Handle all errors during api route handlers """
    return JSONResponse(
        status_code=err.status_code,
        content={"error": err.message}
    )
