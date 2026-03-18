from __future__ import annotations

from argostranslate import package, translate

LANGUAGE_MAP = {
    "en": "en",
    "english": "en",
    "km": "km",
    "khmer": "km",
}


def _normalize(code: str) -> str:
    return LANGUAGE_MAP.get(code.lower(), code.lower())


def ensure_model_installed(source_lang: str, target_lang: str) -> None:
    source = _normalize(source_lang)
    target = _normalize(target_lang)

    installed_languages = translate.get_installed_languages()
    from_lang = next((lang for lang in installed_languages if lang.code == source), None)
    if from_lang:
        for translation in from_lang.translations:
            if translation.to_lang.code == target:
                return

    package.update_package_index()
    packages = package.get_available_packages()
    selected = next(
        (
            pkg
            for pkg in packages
            if pkg.from_code == source and pkg.to_code == target
        ),
        None,
    )
    if not selected:
        raise RuntimeError(f"No Argos package available for {source} -> {target}")

    path = selected.download()
    package.install_from_path(path)


def translate_segments(segments: list[dict], source_lang: str, target_lang: str) -> list[dict]:
    source = _normalize(source_lang)
    target = _normalize(target_lang)
    ensure_model_installed(source, target)

    translated = []
    for segment in segments:
        translated_text = translate.translate(segment["text"], source, target)
        translated.append(
            {
                "start": segment["start"],
                "end": segment["end"],
                "text": translated_text,
            }
        )
    return translated
