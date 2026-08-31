import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import (
    AppCustomException,
    app_exception_handler,
    http_exception_handler,
    generic_exception_handler
)
from app.database.session import init_db
from app.api import auth, chat, messages, documents, analytics, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables on startup
    init_db()
    print("[INFO] Database initialized successfully.")
    yield
    print("[INFO] Application shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(AppCustomException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include API Routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Authentication"])
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["Chat"])
app.include_router(messages.router, prefix=settings.API_V1_STR, tags=["Messages"])
app.include_router(documents.router, prefix=settings.API_V1_STR, tags=["Documents"])
app.include_router(analytics.router, prefix=settings.API_V1_STR, tags=["Analytics"])

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }
