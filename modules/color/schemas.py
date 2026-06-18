from typing import Any
from pydantic import BaseModel
from fastapi import Form, HTTPException
from sqlalchemy.orm import Session
from core.prefix_id import generate_prefixed_id
from modules.color.models import TBL_COLOR

class ColorSchemas(BaseModel):
    name     : str | None = None
    name_lc  : str | None = None
    hex_color: str | None = None
    active   : bool

class ColorModels(ColorSchemas):
    @classmethod
    def form(
            cls,
            name      : str  = Form(None, examples=[""]),
            name_lc   : str  = Form(None, examples=[""]),
            hex_color : str  = Form(None, examples=[""]),
            active    : bool = True,
    ):
        return cls(
            name = name,
            name_lc = name_lc,
            hex_color = hex_color,
            active = active,
        )

def generate_id(db: Session)-> str:
    result = generate_prefixed_id(db, [
        TBL_COLOR
    ], "COL")
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to generate a qnique ID")
    return result

def color_response(item: Any)-> dict[str, Any]:
    return{
        "id"       : getattr(item, "id"),
        "name"     : getattr(item, "name"),
        "name_lc"  : getattr(item, "name_lc"),
        "hex_color": getattr(item, "hex_color"),
        "active"   : getattr(item, "active"),
    }