from typing import Annotated

async def get_optional_user(request: Request, db: SessionDep):
    """Returns the current user if logged in, otherwise returns None."""
    try:
        return await get_current_user(request, db)
    except Exception:
        return None

OptionalUser = Annotated[User | None, Depends(get_optional_user)]
