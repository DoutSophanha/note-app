from __future__ import annotations

import json
from pathlib import Path
import subprocess


def _run_command(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def list_available_subtitle_languages(url: str) -> list[str]:
    command = ["yt-dlp", "--list-subs", "--dump-json", url]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)

    subtitles = data.get("subtitles", {})
    auto_captions = data.get("automatic_captions", {})
    languages = sorted(set(list(subtitles.keys()) + list(auto_captions.keys())))
    return languages


def extract_subtitles(url: str, language: str, output_dir: Path) -> Path | None:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(output_dir / "source")

    command = [
        "yt-dlp",
        "--skip-download",
        "--write-sub",
        "--write-auto-sub",
        "--sub-lang",
        language,
        "--sub-format",
        "vtt",
        "-o",
        output_template,
        url,
    ]

    _run_command(command)

    candidates = sorted(output_dir.glob("source*.vtt"))
    return candidates[0] if candidates else None


def extract_audio(url: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(output_dir / "audio")
    command = [
        "yt-dlp",
        "-x",
        "--audio-format",
        "wav",
        "-o",
        output_template,
        url,
    ]
    _run_command(command)

    candidates = sorted(output_dir.glob("audio*.wav"))
    if not candidates:
        raise RuntimeError("Failed to extract audio from URL")
    return candidates[0]


def convert_to_mp3(url: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(output_dir / "audio")
    command = ["yt-dlp", "-x", "--audio-format", "mp3", "-o", output_template, url]
    _run_command(command)

    candidates = sorted(output_dir.glob("audio*.mp3"))
    if not candidates:
        raise RuntimeError("Failed to convert audio to MP3")
    return candidates[0]


def reencode_to_mp4(url: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(output_dir / "video")
    command = [
        "yt-dlp",
        "-f",
        "bestvideo+bestaudio/best",
        "--merge-output-format",
        "mp4",
        "-o",
        output_template,
        url,
    ]
    _run_command(command)

    candidates = sorted(output_dir.glob("video*.mp4"))
    if not candidates:
        raise RuntimeError("Failed to produce MP4")
    return candidates[0]
