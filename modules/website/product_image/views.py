import math
from modules.product_image.schemas import *
from fastapi import Depends, Query, status
from sqlalchemy.orm import Session
from core.db_session import get_db
from modules.product_image.models import TBL_PRODUCT_IMAGE
from main import website

@website.get(
    "/get_product_image",
    tags         = ["Product Image"],
    operation_id = "get_product_image",
)
async def get_product_image(
    page: int     = Query(default=1, ge=1),
    size: int     = Query(default=10, ge=1),
    db  : Session = Depends(get_db)
):
    base_query = db.query(TBL_PRODUCT_IMAGE).filter(TBL_PRODUCT_IMAGE.active == True)

    total   = base_query.count()
    results = base_query.order_by(TBL_PRODUCT_IMAGE.title\
                        .asc())\
                        .offset((page - 1) * size)\
                        .limit(size)\
                        .all()
    total_pages = math.ceil(total / size) if size else 1
    
    data_list = [product_image_resonse(c) for c in results]

    return {
        'ok'     : True,
        'status' : 200,
        'title'  : 'Product Image',
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
    "/get_product_image/{product_image_id}",
    tags=["Product Image"],
    operation_id="get_product_image_by_id",
)
async def get_product_image_by_id(
    product_image_id: str,
    db         : Session = Depends(get_db),
):
    item = db.query(TBL_PRODUCT_IMAGE).filter(TBL_PRODUCT_IMAGE.id == product_image_id).first()
    if not item:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "Product Image not found",
        )

    return {
        "ok"     : True,
        "status" : 200,
        "title"  : "Product Image",
        "message": "Data retrieved successfully",
        "data"   : product_image_resonse(item),
        "error"  : {},
    }