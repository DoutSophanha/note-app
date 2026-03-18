from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class JobCreateRequest(BaseModel):
    url: HttpUrl
    source_lang: str = Field(default="en")
    target_lang: str = Field(default="km")
    generate_mp3: bool = False
    reencode_mp4: bool = False
    generate_tts: bool = False


class JobCreateResponse(BaseModel):
    id: str
    status: str


class JobStatusResponse(BaseModel):
    id: str
    status: str
    progress: int
    step: str
    error: Optional[str] = None


class JobResultResponse(BaseModel):
    id: str
    status: str
    files: dict[str, str]
    available_subtitle_languages: list[str] = Field(default_factory=list)
