from fastapi import FastAPI, HTTPException
from src.api.router import router as api_router

app = FastAPI()


app.include_router(api_router)