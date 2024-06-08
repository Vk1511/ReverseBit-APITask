from fastapi import APIRouter, Response, Request
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

router = APIRouter(prefix="/auth")


@router.get("/")
async def root():
    return {"message": "Hello World"}
