import json
from datetime import datetime, timezone

from app.core.redis_client import get_redis


def _job_key(job_id: str) -> str:
    return f"job:{job_id}"


def create_job(job_id: str, payload: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    data = {
        "id": job_id,
        "status": "queued",
        "progress": 0,
        "step": "queued",
        "error": "",
        "files": json.dumps({}),
        "available_subtitle_languages": json.dumps([]),
        "payload": json.dumps(payload),
        "created_at": now,
        "updated_at": now,
    }
    r = get_redis()
    r.hset(_job_key(job_id), mapping=data)
    return data


def get_job(job_id: str) -> dict | None:
    r = get_redis()
    data = r.hgetall(_job_key(job_id))
    return data or None


def update_job(job_id: str, **updates) -> None:
    updates["updated_at"] = datetime.now(timezone.utc).isoformat()
    sanitized = {}
    for key, value in updates.items():
        if isinstance(value, (dict, list)):
            sanitized[key] = json.dumps(value)
        elif value is None:
            sanitized[key] = ""
        else:
            sanitized[key] = str(value)

    r = get_redis()
    r.hset(_job_key(job_id), mapping=sanitized)


def parse_job_record(raw: dict) -> dict:
    if not raw:
        return {}

    parsed = dict(raw)
    parsed["progress"] = int(parsed.get("progress", 0))
    parsed["files"] = json.loads(parsed.get("files", "{}"))
    parsed["available_subtitle_languages"] = json.loads(
        parsed.get("available_subtitle_languages", "[]")
    )
    return parsed
