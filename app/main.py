from fastapi import FastAPI
from app.routes import categories

app = FastAPI()
app.include_router(categories.router)
