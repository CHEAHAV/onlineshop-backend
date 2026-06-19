import math
from typing import cast
from fastapi import Depends, HTTPException, Query, status
from core.db_session import get_db
from core.api.user.views import get_current_user
from main import app
from modules.product.models import TBL_PRODUCT
from modules.product.schemas import *

@app.post("/create_product", tags=["Product"], status_code=201, operation_id="create_product",dependencies=[Depends(get_current_user)])

async def create_product(
    product : ProductModels = Depends(ProductModels.form),
    db      : Session       = Depends(get_db),
):
    new_id   = generate_id(db)
    new_item = TBL_PRODUCT(
        id               = new_id,
        name             = product.name,
        name_lc          = product.name_lc,
        product_qty      = product.product_qty,
        out_stock        = product.out_stock,
        in_stock         = product.in_stock,
        rating           = product.rating,
        viewer           = product.viewer,
        old_price        = product.old_price,
        original_price   = product.original_price,
        selling_price    = product.selling_price,
        discount         = product.discount,
        saving_price     = product.saving_price,
        profit_price     = product.profit_price,
        profit_percentage = product.profit_percentage,
        total_original_price = product.total_original_price,
        total_selling_price = product.total_selling_price,
        total_profit_price = product.total_profit_price,
        total_profit_percentage = product.total_profit_percentage,
        product_image_id = product.product_image_id,
        shipping         = product.shipping,
        badge            = product.badge,
        is_favorite      = product.is_favorite,
        is_new           = product.is_new,
        active           = product.active,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return{
        "ok"     : True,
        "status" : 201,
        "title"  : "Product",
        "message": "Data created successfully",
        "data"   : product_response(new_item),
        "error"  : {},
    }


@app.get(
    "/get_product",
    tags=["Product"],
    operation_id="get_product",
    dependencies=[Depends(get_current_user)],
)
async def get_product(
    page: int     = Query(default=1, ge=1),
    size: int     = Query(default=10, ge=1),
    db  : Session = Depends(get_db)
):
    base_query = db.query(TBL_PRODUCT).filter(TBL_PRODUCT.active == True)

    total   = base_query.count()
    results = base_query.order_by(TBL_PRODUCT.name\
                        .asc())\
                        .offset((page - 1) * size)\
                        .limit(size)\
                        .all()
    total_pages = math.ceil(total / size) if size else 1
    
    data_list = [product_response(c) for c in results]

    return {
        'ok'     : True,
        'status' : 200,
        'title'  : 'Product',
        'message': 'Data retrieved successfully',
        'data'   : {
            'lists'    : data_list,
            'meta_data': {
                'total'       : total,
                'total_page'  : total_pages,
                'current_page': page,
                'size'        : size,
            }
        },
        'error': {}
    }


@app.get(
    "/get_product/{product_id}",
    tags=["Product"],
    operation_id="get_product_by_id",
    dependencies=[Depends(get_current_user)],
)
async def get_product_by_id(
    product_id: str,
    db         : Session = Depends(get_db),
):
    item = db.query(TBL_PRODUCT).filter(TBL_PRODUCT.id == product_id).first()
    if not item:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "Product not found",
        )
    return {
        "ok"     : True,
        "status" : 200,
        "title"  : "Product",
        "message": "Data retrieved successfully",
        "data"   : product_response(item),
        "error"  : {},
    }

@app.put(
    "/update_product/{product_id}",
    tags         = ["Product"],
    operation_id = "update_product",
    dependencies = [Depends(get_current_user)],
)
async def update_product(
    product_id: str,
    product   : ProductModels = Depends(ProductModels.form),
    db         : Session        = Depends(get_db),
):
    item = db.query(TBL_PRODUCT).filter(TBL_PRODUCT.id == product_id).first()
    if not item:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "product not found",
    )
    setattr(item, "name", product.name)
    setattr(item, "name_lc", product.name_lc)
    setattr(item, "product_qty", product.product_qty)
    setattr(item, "out_stock", product.out_stock)
    setattr(item, "in_stock", product.in_stock)
    setattr(item, "rating", product.rating)
    setattr(item, "viewer", product.viewer)
    setattr(item, "old_price", product.old_price)
    setattr(item, "original_price", product.original_price)
    setattr(item, "selling_price", product.selling_price)
    setattr(item, "discount", product.discount)
    setattr(item, "saving_price", product.saving_price)
    setattr(item, "profit_price", product.profit_price)
    setattr(item, "profit_percentage", product.profit_percentage)
    setattr(item, "total_original_price", product.total_original_price)
    setattr(item, "total_selling_price", product.total_selling_price)
    setattr(item, "total_profit_price", product.total_profit_price)
    setattr(item, "total_profit_percentage", product.total_profit_percentage)
    setattr(item, "product_image_id", product.product_image_id)
    setattr(item, "shipping", product.shipping)
    setattr(item, "badge", product.badge)
    setattr(item, "is_favorite", product.is_favorite)
    setattr(item, "is_new", product.is_new)
    setattr(item, "active", product.active)

    db.commit()
    db.refresh(item)

    return {
        "ok"     : True,
        "status" : 200,
        "title"  : "Product",
        "message": "Data updated successfully",
        "data"   : product_response(item),
        "error"  : {},
    }


@app.delete(
    "/delete_product/{product_id}",
    tags         = ["Product"],
    operation_id = "delete_product",
    dependencies = [Depends(get_current_user)],
)
async def delete_product(
    product_id: str,
    db         : Session = Depends(get_db),
):
    item = db.query(TBL_PRODUCT).filter(TBL_PRODUCT.id == product_id).first()
    if not item:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "Product not found",
        )

    data = product_response(item)
    db.delete(item)
    db.commit()

    return {
        "ok"     : True,
        "status" : 200,
        "title"  : "Product",
        "message": "Data deleted successfully",
        "data"   : data,
        "error"  : {},
    }
