import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.route.routes import router

logger = logging.getLogger("app")

app = FastAPI(
    title="Event Invitation System API",
    version="1.0.0",
    description="Personalized event invitations using RAG + LLM"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
