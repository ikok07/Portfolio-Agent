import hashlib
import io
import os
from typing import Annotated

import PyPDF2
import chromadb
from clerk_backend_api import User
from fastapi import APIRouter, UploadFile, Depends, Query
from langchain_core.documents import Document
from starlette import status

from src.api.dependencies.protect import protect_dependency
from src.api.models.db.profiles import Profile
from src.api.models.enums.supported_filetypes import SupportedFileType
from src.api.models.errors.api_error import APIError
from src.api.models.response.generic import GenericResponse
from src.api.models.services.text_splitter import TextSplitter
from src.api.models.services.vector_store import VectorStore, StoreFullFile

router = APIRouter()
collection = "user-files"

@router.get("/retrieve-files")
async def retrieve_files(userdata: tuple[User, Profile] = Depends(protect_dependency)):
    store_docs = VectorStore.get_docs_by_user_id(user_id=userdata[0].id, collection_name=collection)
    full_files: list[StoreFullFile] = []
    for store_document in store_docs:
        if not store_document.metadata["filename"] in [file.filename for file in full_files]:
            full_files.append(
                StoreFullFile(
                    filename=store_document.metadata["filename"],
                    filetype=store_document.metadata["filetype"],
                    created_at=store_document.metadata["created_at"]
                )
            )

    return GenericResponse(
        data=[dict(file) for file in full_files]
    )

@router.post("/store-files")
async def store_files(files: list[UploadFile], userdata: tuple[User, Profile] = Depends(protect_dependency)):

    # Check for file support before doing anything
    for file in files:
        if not file.content_type in SupportedFileType:
            return APIError(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, message=f"Supported file formats: {", ".join(SupportedFileType)}")

    for file in files:
        chunks: list[Document] = []
        if file.content_type == SupportedFileType.pdf:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(await file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"

            chunks += TextSplitter.generic_split(text)
        elif file.content_type == SupportedFileType.markdown:
            chunks += TextSplitter.markdown_split([(await file.read()).decode("utf-8")])
        else:
            chunks += TextSplitter.generic_split([(await file.read()).decode("utf-8")])

        VectorStore.insert_docs(
            docs=[chunk.page_content for chunk in chunks],
            collection_name=collection,
            filename=file.filename,
            filetype=str(file.content_type),
            user_id=userdata[0].id,
            custom_ids=[hashlib.sha256(chunk.page_content.encode("utf-8")).hexdigest() for chunk in chunks]
        )

    return GenericResponse()

@router.delete("/delete-files")
async def delete_files(filenames: Annotated[list[str], Query()], userdata: tuple[User, Profile] = Depends(protect_dependency)):
    for filename in filenames:
        VectorStore.delete_document_by_name(filename, user_id=userdata[0].id, collection_name=collection)

    return GenericResponse()