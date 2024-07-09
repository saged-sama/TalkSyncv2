from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, images, messages, users
from app.database import engine, Base

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(images.router)
app.include_router(messages.router)
app.include_router(users.router)

Base.metadata.create_all(bind=engine)