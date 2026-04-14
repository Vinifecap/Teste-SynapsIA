"""
SynapsIA Backend — FastAPI entry point
Provides REST API for fMRI exam upload and pre-report generation
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.exam import router as exam_router

# Ensure temp upload directory exists
os.makedirs("temp_uploads", exist_ok=True)

app = FastAPI(
    title="SynapsIA API",
    description="AI-powered neurological diagnostic assistant — fMRI pre-report generator",
    version="1.0.0",
)

# Allow frontend dev server to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated brain images as static files
app.mount("/uploads", StaticFiles(directory="temp_uploads"), name="uploads")

# Register exam routes under /api
app.include_router(exam_router, prefix="/api")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "SynapsIA API", "version": "1.0.0"}
