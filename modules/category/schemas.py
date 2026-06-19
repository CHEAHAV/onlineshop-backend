from typing import Any, cast
from fastapi import File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.prefix_id import generate_prefixed_id
from core.upload_utils import media_name, media_url, upload_image_to_cloudinary
from modules.category.models import TBL_CATEGORY

class CategorySchemas(BaseModel):
    name       : str | None = None
    name_lc    : str | None = None
    description: str | None = None
    image      : UploadFile | None = None
    active     : bool = True

class CategoryModels(CategorySchemas):
    @classmethod
    def form(
        cls,
        name        : str        = Form(None, examples=[""]),
        name_lc     : str        = Form(None, examples=[""]),
        description : str        = Form(None, examples=[""]),
        image       : UploadFile = File(None),
        active      : bool       = True,
    ):
        return cls(
            name        = name,
            name_lc     = name_lc,
            description = description,
            image       = image,
            active      = active,
        )

def generate_id(db: Session) -> str:
    result = generate_prefixed_id(db, [
        TBL_CATEGORY
    ], "CAT")
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to generate a unique ID")
    return result

def save_image(image: UploadFile) -> str:
    return upload_image_to_cloudinary(image, "Category")


def category_response(item: Any) -> dict[str, Any]:
    image = cast(str | None, getattr(item, "image"))
    return {
        "id"         : getattr(item, "id"),
        "name"       : getattr(item, "name"),
        "name_lc"    : getattr(item, "name_lc"),
        "description": getattr(item, "description"),
        "image"      : media_name(image),
        "image_link" : media_url(image),
        "active"     : getattr(item, "active"),
    }