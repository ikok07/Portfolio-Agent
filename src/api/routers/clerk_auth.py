import os

from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from svix import WebhookVerificationError, Webhook

from src.api.models.body.clerk_auth import ClerkUserCreatedBody
from src.api.models.db.profiles import Profile

router = APIRouter()

@router.post("/user/created", status_code=status.HTTP_204_NO_CONTENT)
async def user_created(request: Request, response: Response):
    headers = request.headers
    payload = await request.body()
    try:
        wh = Webhook(os.getenv("CLERK_USER_CREATED_SECRET"))
        body: ClerkUserCreatedBody = ClerkUserCreatedBody(**wh.verify(payload, dict(headers)))
        profile = Profile(id=body.data.id, first_name=body.data.first_name or "<no-first-name>", last_name=body.data.last_name or "<no-last-name>", email=body.data.email_addresses[0].email_address)
        await profile.save()
    except WebhookVerificationError as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(e)
        return
