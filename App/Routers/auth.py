from fastapi import APIRouter, Response, Request
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    request: Request,
    response: Response,
):
    # Authenticate the user against Keycloak
    try:
        pass
    except Exception as e:
        pass

    return response
