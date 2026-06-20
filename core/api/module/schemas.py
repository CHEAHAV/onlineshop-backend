from typing import Any, cast
from fastapi import Form, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.prefix_id import generate_prefixed_id
from core.upload_utils import upload_image_to_cloudinary


class ModuleSchemas(BaseModel):
    name    : str
    name_lc : str
    url     : str
    icon    : UploadFile | None = None
    model   : str
    ordering: int
    active  : bool

class ModuleModels(ModuleSchemas):
    @classmethod
    def form(
        cls,
        name     : str        = Form(..., examples= [""]),
        name_lc  : str        = Form(..., examples=[""]),
        url      : str        = Form(..., examples=[""]),
        icon     : UploadFile = File(None),
        model    : str        = Form(..., examples=[""]),
        ordering : int        = Form(..., examples=[""]),
        active   : bool       = True,

    ):
        return cls(
            name     = name,
            name_lc  = name_lc,
            url      = url,
            icon     = icon,
            model    = model,
            ordering = ordering,
            active   = active,
        )

def generate_id(db: Session)-> str:
    result = generate_prefixed_id(db, [

    ], "MOD")
    if result is None:
        raise HTTPException(status_code=500, detail= "Failed to generate a unique ID")
    return result

def save_icon(icon : UploadFile)-> str:
    return upload_image_to_cloudinary(icon, "Module")

def module_response(item : Any)-> dict[str, Any]:
    icon = cast(str | None, getattr(item, "icon"))
    return{
        "id"      : getattr(item, "id"),
        "name"    : getattr(item, "name"),
        "name_lc" : getattr(item, "name_lc"),
        "url"     : getattr(item, "url"),
        "icon"    : getattr(item, "icon"),
        "model"   : getattr(item, "model"),
        "ordering": getattr(item, "ordering"),
        "active"  : getattr(item, "active"),
    }