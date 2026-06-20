
from typing import Any

from fastapi import Form, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.prefix_id import generate_prefixed_id
from modules.product.models import TBL_PRODUCT


class ProductSchemas(BaseModel):
    name                    : str | None   = None
    name_lc                 : str | None   = None
    category_id             : str | None   = None
    product_qty             : int | None   = None
    out_stock               : int | None   = None
    in_stock                : int | None   = None
    rating                  : float | None = None
    viewer                  : int | None   = None
    old_price               : float | None = None
    original_price          : float | None = None
    selling_price           : float | None = None
    discount                : float | None = None
    saving_price            : float | None = None
    profit_price            : float | None = None
    profit_percentage       : float | None = None
    total_price_in_stock    : float | None = None
    total_price_out_stock   : float | None = None
    total_original_price    : float | None = None
    total_selling_price     : float | None = None
    total_profit_price      : float | None = None
    total_profit_percentage : float | None = None
    product_image_id        : str | None   = None
    shipping                : float | None = None
    badge                   : str | None   = None
    is_favorite             : bool         = False
    is_new                  : bool         = True
    active                  : bool         = True

class ProductModels(ProductSchemas):
    @classmethod
    def form(
        cls,
        name             : str | None   = Form(None, examples=[""]),
        name_lc          : str | None   = Form(None, examples=[""]),
        category_id      : str | None   = Form(None, examples=[""]),
        product_qty      : int | None   = Form(None, examples=[""]),
        out_stock        : int | None   = Form(None, examples=[""]),
        rating           : float | None = Form(None, examples=[""]),
        viewer           : int | None   = Form(None, examples=[""]),
        original_price   : float | None = Form(None, examples=[""]),
        old_price        : float | None = Form(None, examples=[""]),
        selling_price    : float | None = Form(None, examples=[""]),
        product_image_id : str | None   = Form(None, examples=[""]),
        shipping         : float | None = Form(None, examples=[""]),
        badge            : str | None   = Form(None, examples=[""]),
        is_favorite      : bool         = False,
        is_new           : bool         = True,
        active           : bool         = True
    ):
        saving_price            = None
        discount                = None
        in_stock                = None
        profit_price            = None
        profit_percentage       = None
        total_price_in_stock    = None
        total_price_out_stock   = None
        total_original_price    = None
        total_selling_price     = None
        total_profit_price      = None
        total_profit_percentage = None

        if old_price is not None and selling_price is not None: 
            saving_price = old_price - selling_price
            if old_price: 
                discount = (saving_price / old_price) * 100

        if product_qty is not None and out_stock is not None: 
            in_stock = product_qty - out_stock

        if selling_price is not None and original_price is not None: 
            profit_price = selling_price - original_price
            if original_price: 
                profit_percentage = (profit_price / original_price) * 100

        if original_price is not None and product_qty is not None: 
            total_original_price = original_price * product_qty

        if selling_price is not None and product_qty is not None: 
            total_selling_price = selling_price * product_qty

        if selling_price is not None and out_stock is not None:
            total_price_out_stock = selling_price * out_stock

        if total_selling_price is not None and total_price_out_stock is not None:
            total_price_in_stock = total_selling_price - total_price_out_stock

        if total_selling_price is not None and total_original_price is not None: 
            total_profit_price = total_selling_price - total_original_price
            if total_original_price: 
                total_profit_percentage = (total_profit_price / total_original_price) * 100

        return cls(
            name                    = name,
            name_lc                 = name_lc,
            category_id             = category_id,
            product_qty             = product_qty,
            out_stock               = out_stock,
            in_stock                = in_stock,
            rating                  = rating,
            viewer                  = viewer,
            old_price               = old_price,
            original_price          = original_price,
            selling_price           = selling_price,
            discount                = discount,
            saving_price            = saving_price,
            profit_price            = profit_price,
            profit_percentage       = profit_percentage,
            total_price_in_stock    = total_price_in_stock,
            total_price_out_stock   = total_price_out_stock,
            total_original_price    = total_original_price,
            total_selling_price     = total_selling_price,
            total_profit_price      = total_profit_price,
            total_profit_percentage = total_profit_percentage,
            product_image_id        = product_image_id,
            shipping                = shipping,
            badge                   = badge,
            is_favorite             = is_favorite,
            is_new                  = is_new,
            active                  = active
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
        "id"                     : getattr(item, "id"),
        "name"                   : getattr(item, "name"),
        "name_lc"                : getattr(item, "name_lc"),
        "category_id"            : getattr(item, "category_id"),
        "product_qty"            : getattr(item, "product_qty"),
        "out_stock"              : getattr(item, "out_stock"),
        "in_stock"               : getattr(item, "in_stock"),
        "rating"                 : getattr(item, "rating"),
        "viewer"                 : getattr(item, "viewer"),
        "old_price"              : getattr(item, "old_price"),
        "original_price"         : getattr(item, "original_price"),
        "selling_price"          : getattr(item, "selling_price"),
        "discount"               : getattr(item, "discount"),
        "saving_price"           : getattr(item, "saving_price"),
        "profit_price"           : getattr(item, "profit_price"),
        "profit_percentage"      : getattr(item, "profit_percentage"),
        "total_price_in_stock"   : getattr(item, "total_price_in_stock"),
        "total_price_out_stock"  : getattr(item, "total_price_out_stock"),
        "total_original_price"   : getattr(item, "total_original_price"),
        "total_selling_price"    : getattr(item, "total_selling_price"),
        "total_profit_price"     : getattr(item, "total_profit_price"),
        "total_profit_percentage": getattr(item, "total_profit_percentage"),
        "product_image_id"       : getattr(item, "product_image_id"),
        "shipping"               : getattr(item, "shipping"),
        "badge"                  : getattr(item, "badge"),
        "is_favorite"            : getattr(item, "is_favorite"),
        "is_new"                 : getattr(item, "is_new"),
        "active"                 : getattr(item, "active"),
    }
