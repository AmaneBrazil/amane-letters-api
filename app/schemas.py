from uuid import UUID
from pydantic import BaseModel, AfterValidator
from typing import Optional, Annotated


def not_blank(value:str) -> str:
    if not value.strip():
        raise ValueError("Esse campo não pode ser vazio")
    return value

NonBlankStr = Annotated[str, AfterValidator(not_blank)]

class LetterCreate(BaseModel):
    title: NonBlankStr
    content: NonBlankStr
    password: Optional[str] = None
    style_theme: Optional[str] = "base"
    image_url: Optional[str] = None

class LetterAccess(BaseModel):
    password: Optional[str] = None

class LetterResponse(BaseModel):
    id: UUID
    title: str
    content: str
    is_public: Optional[bool] = True
    style_theme: str
    image_url: Optional[str] = None

    model_config = {
        "from_attributes": True
    }