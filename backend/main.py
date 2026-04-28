from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .api import chat_routes, agent_routes, task_routes, memory_routes, settings_routes, document_routes

app = FastAPI(title="AI Agent Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_routes.router)
app.include_router(agent_routes.router)
app.include_router(task_routes.router)
app.include_router(memory_routes.router)
app.include_router(settings_routes.router)
app.include_router(document_routes.router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}
