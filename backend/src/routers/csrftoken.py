from fastapi import APIRouter
from starlette import status

router = APIRouter()


@router.get(path="/", name="send_csrf_token", status_code=status.HTTP_204_NO_CONTENT)
async def send_csrf_token() -> None:
    pass
