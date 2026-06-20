
from typing import Any, cast
from fastapi import File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session
from modules.product_image.models import TBL_PRODUCT_IMAGE
from core.upload_utils import media_name, media_url, upload_image_to_cloudinary
from core.prefix_id import generate_prefixed_id




class ProductImageSchemas(BaseModel):
    title          : str | None        = None
    title_lc       : str | None        = None
    description    : str | None        = None
    description_lc : str | None        = None
    color_id       : str | None        = None
    image          : UploadFile | None = None
    active         : bool              = True

class ProductImageModels(ProductImageSchemas):
    @classmethod
    def form(
        cls,
        title          : str        = Form(None, examples=[""]),
        title_lc       : str        = Form(None, examples=[""]),
        description    : str        = Form(None, examples=[""]),
        description_lc : str        = Form(None, examples=[""]),
        color_id       : str        = Form(None, examples=[""]),
        image          : UploadFile = File(None),
        active         : bool       = True
    ):
        return cls(
            title          = title,
            title_lc       = title_lc,
            description    = description,
            description_lc = description_lc,
            color_id       = color_id,
            image          = image,
            active         = active
        )

def generate_id(db: Session) -> str:
    result = generate_prefixed_id(db, [
        TBL_PRODUCT_IMAGE
    ], "PIM")
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to generate a unique ID")
    return result

def save_image(image: UploadFile) -> str:
    return upload_image_to_cloudinary(image, "ProductImage")

def product_image_response(item: Any, include_color: bool = True) -> dict[str, Any]:
    image = cast(str | None, getattr(item, "image"))
    data = {
        "id"            : getattr(item, "id"),
        "title"         : getattr(item, "title"),
        "title_lc"     : getattr(item, "title_lc"),
        "description"   : getattr(item, "description"),
        "description_lc": getattr(item, "description_lc"),
        "color_id"      : getattr(item, "color_id"),
        "image"         : media_name(image),
        "image_link"    : media_url(image),
        "active"        : getattr(item, "active"),
    }

    if include_color:
        from modules.color.schemas import color_response

        color = getattr(item, "color", None)
        data["color"] = color_response(color) if color else None

    return data


def product_image_resonse(item: Any, include_color: bool = True) -> dict[str, Any]:
    return product_image_response(item, include_color=include_color)
