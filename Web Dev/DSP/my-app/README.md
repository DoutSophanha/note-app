# Offline Subtitle Pipeline (EN ↔ KM)

Production-ready starter scaffold for a local/self-hosted subtitle platform using only free and open-source tools.

## Stack

- Frontend: Next.js (App Router) + Tailwind CSS
- Backend: FastAPI
- Processing: `yt-dlp`, `ffmpeg`, `faster-whisper`, `argos-translate`, optional `Coqui TTS`
- Queue: Redis + simple Python worker
- Storage: local filesystem (`storage/`)

## Project Structure

```text
my-app/
	frontend/
		app/
		components/
	backend/
		app/
			api/
			core/
			models/
			schemas/
	services/
		youtube_service.py
		subtitle_service.py
		translation_service.py
		tts_service.py
	workers/
		job_worker.py
		pipeline.py
	storage/
		jobs/
		downloads/
		temp/
```

## API

- `POST /api/job` - create processing job
- `GET /api/job/{id}` - read progress and step
- `GET /api/job/{id}/result` - fetch output metadata
- `GET /static-file?path=...` - download generated files from local storage

## Processing Flow

1. Check available subtitle languages (`yt-dlp --list-subs`)
2. Try extracting subtitles for selected source language
3. If unavailable, extract audio and run Whisper transcription
4. Translate subtitle text offline with Argos Translate
5. Export SRT + VTT + TXT
6. Optional: MP3, MP4, and TTS audio generation

## Prerequisites

- Python 3.11+
- Node.js 20+
- `ffmpeg` installed and in `PATH`
- Redis server (local or Docker)

macOS (Homebrew):

```bash
brew install ffmpeg redis
```

## Local Run

### 1) Start Redis

```bash
docker compose up -d redis
```

### 2) Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### 3) Worker setup (new terminal)

```bash
cd my-app
source backend/.venv/bin/activate
python workers/job_worker.py
```

### 4) Frontend setup (new terminal)

```bash
cd frontend
cp .env.local.example .env.local
pnpm install
pnpm dev
```

Open `http://localhost:3000`.

## Notes

- All artifacts are written under `storage/downloads/<job_id>/`
- Translation model download happens once (Argos package install) and is then reused
- Coqui TTS is optional and can be disabled in UI per-job
