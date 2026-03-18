from __future__ import annotations

import json
from pathlib import Path

from app.core.config import DOWNLOADS_DIR, JOBS_DIR, WHISPER_MODEL
from app.models.job_store import get_job, parse_job_record, update_job
from services.subtitle_service import (
    segments_to_srt,
    segments_to_txt,
    segments_to_vtt,
    transcribe_audio_to_segments,
    vtt_to_segments,
)
from services.translation_service import translate_segments
from services.tts_service import generate_tts_audio
from services.youtube_service import (
    convert_to_mp3,
    extract_audio,
    extract_subtitles,
    list_available_subtitle_languages,
    reencode_to_mp4,
)


def process_job(job_id: str) -> None:
    raw = get_job(job_id)
    if not raw:
        return

    job = parse_job_record(raw)
    payload = json.loads(raw.get("payload", "{}"))
    source_lang = payload.get("source_lang", "en")
    target_lang = payload.get("target_lang", "km")
    url = payload["url"]

    job_dir = JOBS_DIR / job_id
    out_dir = DOWNLOADS_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        update_job(job_id, status="processing", progress=5, step="checking_subtitle_languages")
        available_languages = list_available_subtitle_languages(url)
        update_job(job_id, available_subtitle_languages=available_languages)

        update_job(job_id, progress=20, step="extracting_subtitles")
        vtt_path = extract_subtitles(url, source_lang, job_dir)

        if vtt_path:
            source_segments = vtt_to_segments(vtt_path)
            update_job(job_id, progress=45, step="subtitles_extracted")
        else:
            update_job(job_id, progress=35, step="running_whisper")
            audio_path = extract_audio(url, job_dir)
            source_segments = transcribe_audio_to_segments(
                audio_path=audio_path,
                model_name=WHISPER_MODEL,
                source_lang=source_lang,
            )
            update_job(job_id, progress=55, step="whisper_complete")

        update_job(job_id, progress=70, step="translating")
        translated_segments = translate_segments(source_segments, source_lang, target_lang)

        update_job(job_id, progress=82, step="exporting_files")
        srt_path = segments_to_srt(translated_segments, out_dir / "subtitles.srt")
        vtt_output = segments_to_vtt(translated_segments, out_dir / "subtitles.vtt")
        txt_output = segments_to_txt(translated_segments, out_dir / "subtitles.txt")

        output_files = {
            "srt": str(srt_path),
            "vtt": str(vtt_output),
            "txt": str(txt_output),
        }

        if payload.get("generate_mp3"):
            update_job(job_id, progress=88, step="converting_mp3")
            mp3_path = convert_to_mp3(url, out_dir)
            output_files["mp3"] = str(mp3_path)

        if payload.get("reencode_mp4"):
            update_job(job_id, progress=92, step="exporting_mp4")
            mp4_path = reencode_to_mp4(url, out_dir)
            output_files["mp4"] = str(mp4_path)

        if payload.get("generate_tts"):
            update_job(job_id, progress=96, step="generating_tts")
            tts_path = generate_tts_audio(translated_segments, out_dir / "tts.wav")
            output_files["tts"] = str(tts_path)

        update_job(
            job_id,
            status="completed",
            progress=100,
            step="completed",
            files=output_files,
        )
    except Exception as error:
        update_job(job_id, status="failed", progress=100, step="failed", error=str(error))
