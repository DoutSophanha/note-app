from __future__ import annotations

from pathlib import Path
import re
from typing import Iterable

import srt
import webvtt
from faster_whisper import WhisperModel


def _clean_caption_text(text: str) -> str:
    cleaned = re.sub(r"<[^>]+>", "", text)
    return cleaned.strip()


def vtt_to_segments(vtt_path: Path) -> list[dict]:
    subtitles = []
    for caption in webvtt.read(str(vtt_path)):
        subtitles.append(
            {
                "start": caption.start,
                "end": caption.end,
                "text": _clean_caption_text(caption.text),
            }
        )
    return subtitles


def segments_to_srt(segments: Iterable[dict], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subtitles = []
    for index, segment in enumerate(segments, start=1):
        subtitles.append(
            srt.Subtitle(
                index=index,
                start=_timestamp_to_timedelta(segment["start"]),
                end=_timestamp_to_timedelta(segment["end"]),
                content=segment["text"],
            )
        )

    output_path.write_text(srt.compose(subtitles), encoding="utf-8")
    return output_path


def segments_to_vtt(segments: Iterable[dict], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["WEBVTT", ""]
    for segment in segments:
        lines.append(f"{segment['start'].replace(',', '.')} --> {segment['end'].replace(',', '.')}")
        lines.append(segment["text"])
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def segments_to_txt(segments: Iterable[dict], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(segment["text"] for segment in segments)
    output_path.write_text(text, encoding="utf-8")
    return output_path


def transcribe_audio_to_segments(audio_path: Path, model_name: str, source_lang: str) -> list[dict]:
    model = WhisperModel(model_name, compute_type="int8")
    segments, _ = model.transcribe(str(audio_path), language=source_lang)

    results = []
    for segment in segments:
        results.append(
            {
                "start": _seconds_to_srt_timestamp(segment.start),
                "end": _seconds_to_srt_timestamp(segment.end),
                "text": segment.text.strip(),
            }
        )
    return results


def _seconds_to_srt_timestamp(total_seconds: float) -> str:
    total_milliseconds = int(total_seconds * 1000)
    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def _timestamp_to_timedelta(timestamp: str):
    import datetime as dt

    normalized = timestamp.replace(".", ",")
    hours, minutes, rest = normalized.split(":")
    seconds, milliseconds = rest.split(",")
    return dt.timedelta(
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
        milliseconds=int(milliseconds),
    )
