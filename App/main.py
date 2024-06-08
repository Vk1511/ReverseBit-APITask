from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routers.auth import router as auth_router
from fastapi import FastAPI

# Initilize FastAPI app
app = FastAPI(title="reversebit-api")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)