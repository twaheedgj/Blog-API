from fastapi import FastAPI
from db import init_db
from contextlib import asynccontextmanager
from routes import blog_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
app = FastAPI(
    title="Blog API",
    description="API for managing blog posts",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Blog API of Infryne"}

app.include_router(blog_router)