from fastapi import FastAPI
from app.database import Base, engine

from app import models
from app.routes import router as distance_router
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Distance App")

origins = [
    "http://localhost:3000",  # React dev server
    "https://distance-app-frontend-957a17762b8e.herokuapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # or specify ["POST", "GET"] etc.
    allow_headers=["*"],
)

app.include_router(distance_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
