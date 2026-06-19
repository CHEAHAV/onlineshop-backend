from core.db_session import get_db
from core.api.user.views import get_current_user
import math
from main import app
from fastapi import Depends, Query, status
from sqlalchemy.orm import Session
from modules.product_image.models import TBL_PRODUCT_IMAGE
from modules.product_image.schemas import *
from core.upload_utils import delete_cloudinary_image

@app.post(
    "/create_product_image",
    tags         = ["Product Image"],
    status_code  = 201,
    operation_id = "create_product_image",
    dependencies = [Depends(get_current_user)],
)
async def create_product_image(
    pimage: ProductImageModels = Depends(ProductImageModels.form),
    db      : Session        = Depends(get_db),
):
    # 1. Generate a unique, prefixed ID
    new_id = generate_id(db)

    # 2. Persist the image (if provided)
    image_filename: str | None = None
    if pimage.image and pimage.image.filename:
        image_filename = save_image(pimage.image)

    # 3. Insert the new record
    new_item = TBL_PRODUCT_IMAGE(
        id             = new_id,
        title          = pimage.title,
        title_lc      = pimage.title_lc,
        description    = pimage.description,
        description_lc = pimage.description_lc,
        color_id       = pimage.color_id,
        image          = image_filename,
        active         = pimage.active
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {
        "ok"     : True,
        "status" : 201,
        "title"  : "Product Image",
        "message": "Data created successfully",
        "data"   : product_image_resonse(new_item),
        "error"  : {},
    }

@app.get(
    "/get_product_image",
    tags         = ["Product Image"],
    operation_id = "get_product_image",
    dependencies = [Depends(get_current_user)],
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


@app.get(
    "/get_product_image/{product_image_id}",
    tags=["Product Image"],
    operation_id="get_product_image_by_id",
    dependencies=[Depends(get_current_user)],
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


@app.put(
    "/update_product_image/{product_image_id}",
    tags         = ["Product Image"],
    operation_id = "update_product_image",
    dependencies = [Depends(get_current_user)],
)
async def update_product_image(
    product_image_id: str,
    pimage   : ProductImageModels = Depends(ProductImageModels.form),
    db         : Session        = Depends(get_db),
):
    item = db.query(TBL_PRODUCT_IMAGE).filter(TBL_PRODUCT_IMAGE.id == product_image_id).first()
    if not item:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "Product Image not found",
    )
    setattr(item, "title", pimage.title)
    setattr(item, "title_lc", pimage.title_lc)
    setattr(item, "description", pimage.description)
    setattr(item, "description_lc", pimage.description_lc)
    setattr(item, "color_id", pimage.color_id)
    setattr(item, "active", pimage.active)
    if pimage.image and pimage.image.filename: 
        setattr(item, "image", save_image(pimage.image))

    db.commit()
    db.refresh(item)
    
    return {
        "ok"     : True,
        "status" : 200,
        "title"  : "Product Image",
        "message": "Data updated successfully",
        "data"   : product_image_resonse(item),
        "error"  : {},
    }


@app.delete(
    "/delete_product_image/{product_image_id}",
    tags         = ["Product Image"],
    operation_id = "delete_product_image",
    dependencies = [Depends(get_current_user)],
)
async def delete_product_image(
    product_image_id: str,
    db         : Session = Depends(get_db),
):
    item = db.query(TBL_PRODUCT_IMAGE).filter(TBL_PRODUCT_IMAGE.id == product_image_id).first()
    if not item:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "Product Image not found",
        )

    data = product_image_resonse(item)
    image = cast(str | None, getattr(item, "image", None))
    delete_cloudinary_image(image)
    db.delete(item)
    db.commit()

    return {
        "ok"     : True,
        "status" : 200,
        "title"  : "Product Image",
        "message": "Data deleted successfully",
        "data"   : data,
        "error"  : {},
    }
