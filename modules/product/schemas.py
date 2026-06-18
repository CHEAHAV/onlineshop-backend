
from typing import Any

from fastapi import Form, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.prefix_id import generate_prefixed_id
from modules.product.models import TBL_PRODUCT


class ProductSchemas(BaseModel):
    name            : str | None = None
    name_lc         : str | None = None
    rating          : float | None = None
    viewer          : int | None = None
    original_price  : float | None = None
    selling_price   : float | None = None
    discount        : float | None = None
    saving_price    : float | None = None
    product_image_id: str | None = None
    shipping        : float | None = None
    badge           : str | None = None
    is_favorite     : bool
    is_new          : bool
    active          : bool


class ProductModels(ProductSchemas):
    @classmethod
    def form(
        cls,
        name             : str   = Form(None, examples=[""]),
        name_lc          : str   = Form(None, examples=[""]),
        rating           :float  = Form(None, examples=[""]),
        viewer           : int   = Form(None, examples=[""]),
        original_price   : float = Form(None, examples=[""]),
        selling_price    : float = Form(None, examples=[""]),
        discount         : float = Form(None, examples=[""]),
        saving_price     : float = Form(None, examples=[""]),
        product_image_id : str   = Form(None, examples=[""]),
        shipping         : float   = Form(None, examples=[""]),
        badge            : str   = Form(None, examples=[""]),
        is_favorite      : bool  = False,
        is_new           : bool  = True,
        active           : bool  = True
    ):
        return cls(
            name             = name,
            name_lc          = name_lc,
            rating           = rating,
            viewer           = viewer,
            original_price   = original_price,
            selling_price    = selling_price,
            discount         = discount,
            saving_price     = saving_price,
            product_image_id = product_image_id,
            shipping         = shipping,
            badge            = badge,
            is_favorite      = is_favorite,
            is_new           = is_new,
            active           = active
        )

def generate_id(db: Session) -> str:
    result = generate_prefixed_id(db, [
        TBL_PRODUCT
    ], "PRO")
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to generate a unique ID")
    return result

def product_response(item: Any)-> dict[str, Any]:
    return{
        "id"              : getattr(item, "id"),
        "name"            : getattr(item, "name"),
        "name_lc"         : getattr(item, "name_lc"),
        "rating"          : getattr(item, "rating"),
        "viewer"          : getattr(item, "viewer"),
        "original_price"  : getattr(item, "original_price"),
        "selling_price"   : getattr(item, "selling_price"),
        "discount"        : getattr(item, "discount"),
        "saving_price"    : getattr(item, "saving_price"),
        "product_image_id": getattr(item, "product_image_id"),
        "shipping"        : getattr(item, "shipping"),
        "badge"           : getattr(item, "badge"),
        "is_favorite"     : getattr(item, "is_favorite"),
        "is_new"          : getattr(item, "is_new"),
        "active"          : getattr(item, "active"),
    }