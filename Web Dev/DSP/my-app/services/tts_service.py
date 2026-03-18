from __future__ import annotations

from pathlib import Path


def generate_tts_audio(segments: list[dict], output_path: Path, model_name: str = "tts_models/en/ljspeech/tacotron2-DDC") -> Path:
    try:
        from TTS.api import TTS
    except Exception as error:
        raise RuntimeError("Coqui TTS is not installed or failed to import") from error

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joined_text = " ".join(segment["text"] for segment in segments if segment["text"].strip())
    if not joined_text:
        raise RuntimeError("No subtitle text available for TTS")

    tts = TTS(model_name=model_name, progress_bar=False)
    tts.tts_to_file(text=joined_text, file_path=str(output_path))
    return output_path
