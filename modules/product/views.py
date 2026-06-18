import math

from fastapi import Depends, Query
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
        rating           = product.rating,
        viewer           = product.viewer,
        original_price   = product.original_price,
        selling_price    = product.selling_price,
        discount         = product.discount,
        saving_price     = product.saving_price,
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