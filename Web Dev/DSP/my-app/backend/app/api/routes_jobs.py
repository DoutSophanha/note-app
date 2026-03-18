import json
import uuid

from fastapi import APIRouter, HTTPException

from app.core.config import QUEUE_KEY
from app.core.redis_client import get_redis
from app.models.job_store import create_job, get_job, parse_job_record
from app.schemas.job import (
    JobCreateRequest,
    JobCreateResponse,
    JobResultResponse,
    JobStatusResponse,
)

router = APIRouter(prefix="/api", tags=["jobs"])


@router.post("/job", response_model=JobCreateResponse)
def create_job_endpoint(request: JobCreateRequest) -> JobCreateResponse:
    job_id = str(uuid.uuid4())
    payload = request.model_dump(mode="json")

    create_job(job_id=job_id, payload=payload)

    queue_message = json.dumps({"job_id": job_id})
    get_redis().lpush(QUEUE_KEY, queue_message)

    return JobCreateResponse(id=job_id, status="queued")


@router.get("/job/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str) -> JobStatusResponse:
    raw = get_job(job_id)
    if not raw:
        raise HTTPException(status_code=404, detail="Job not found")

    job = parse_job_record(raw)
    return JobStatusResponse(
        id=job["id"],
        status=job["status"],
        progress=job["progress"],
        step=job.get("step", "unknown"),
        error=job.get("error") or None,
    )


@router.get("/job/{job_id}/result", response_model=JobResultResponse)
def get_job_result(job_id: str) -> JobResultResponse:
    raw = get_job(job_id)
    if not raw:
        raise HTTPException(status_code=404, detail="Job not found")

    job = parse_job_record(raw)
    if job["status"] not in {"completed", "failed"}:
        raise HTTPException(status_code=409, detail="Job not completed yet")

    return JobResultResponse(
        id=job["id"],
        status=job["status"],
        files=job.get("files", {}),
        available_subtitle_languages=job.get("available_subtitle_languages", []),
    )
