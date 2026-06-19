import math
from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from core.api.user.views import get_current_user
from core.db_session import get_db
from main import website
from modules.product.models import TBL_PRODUCT
from modules.product.schemas import product_response

@website.get(
    "/get_product",
    tags=["Product"],
    operation_id="get_product",
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
        'title'  : 'Category',
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

@website.get(
    "/get_product/{product_id}",
    tags=["Product"],
    operation_id="get_product_by_id",
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