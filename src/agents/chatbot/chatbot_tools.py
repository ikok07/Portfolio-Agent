import os

import requests
from langchain_core.tools import tool

from src.api.models.db import Company
from src.api.models.services.vector_store import VectorStore


@tool
def send_notification_tool(text: str):
    """ Sends a push notification
        :parameter text Message to be sent
        :returns Dictionary with status field indicating success or failure
     """
    try:
        requests.post(os.getenv("PUSHOVER_URL"), data={"token": os.getenv("PUSHOVER_TOKEN"), "user": os.getenv("PUSHOVER_USER"), "message": text})
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail", "error": e}

@tool
async def get_available_companies() -> dict:
    """ Retrieve the companies for which we have information """
    return await Company.all().values()

@tool
def semantic_search(queries: list[str], user_id: str):
    """
        Use this tool to create a semantic search in a vector store to retrieve the most relevant information about the desired topic
        :arg queries Questions or search texts
        :arg user_id The id of the user
    """

    search_results = VectorStore.semantic_search(
        collection_name="user-files",
        texts=queries,
        user_id=user_id
    )

    return [
        doc.model_dump()
        for batch in search_results
        for doc in batch
    ]

tools = [send_notification_tool, get_available_companies, semantic_search]