import asyncio
import os

from clerk_backend_api import Clerk, AuthenticateRequestOptions, User
from clerk_backend_api.security import AuthStatus
from starlette import status
from starlette.requests import Request

from src.api.models.db.profiles import Profile
from src.api.models.errors.api_error import APIError

async def protect_dependency(request: Request) -> (User, Profile):
    try:
        sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

        def auth():
            state = sdk.authenticate_request(
                request=request,
                options=AuthenticateRequestOptions()
            )
            if state.status == AuthStatus.SIGNED_IN:
                user = sdk.users.get(user_id=state.payload["sub"])
                if not user:
                    raise APIError(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return user
            else:
                raise APIError(status_code=status.HTTP_401_UNAUTHORIZED, message="Unauthorized")

        clerk_user = await asyncio.to_thread(auth)
        profile = await Profile.get(id=clerk_user.id)
        return clerk_user, profile
    except APIError as e:
        raise e
    except Exception as e:
        print(e)
        raise APIError(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

