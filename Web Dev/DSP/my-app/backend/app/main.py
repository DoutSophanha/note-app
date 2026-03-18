from fastapi import FastAPI
from fastapi import HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

from app.api.routes_jobs import router as job_router
from app.core.config import STORAGE_DIR

app = FastAPI(title="Subtitle Pipeline API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/static-file")
def download_file(path: str = Query(..., min_length=1)):
    requested = Path(path).resolve()
    storage_root = STORAGE_DIR.resolve()

    if not str(requested).startswith(str(storage_root)):
        raise HTTPException(status_code=403, detail="Access denied")
    if not requested.exists() or not requested.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=requested)
