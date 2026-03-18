from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import QUEUE_KEY  # noqa: E402
from app.core.redis_client import get_redis  # noqa: E402
from workers.pipeline import process_job  # noqa: E402


def run_worker() -> None:
    redis_client = get_redis()
    print("Worker started. Waiting for jobs...")

    while True:
        _, message = redis_client.brpop(QUEUE_KEY)
        payload = json.loads(message)
        job_id = payload["job_id"]
        process_job(job_id)


if __name__ == "__main__":
    run_worker()
