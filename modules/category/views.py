from core.db_session import get_db
from core.api.user.views import get_current_user
from core.upload_utils import delete_cloudinary_image
import math
from typing import cast
from main import app
from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from modules.category.models import TBL_CATEGORY
from modules.category.schemas import *

@app.post(
    "/create_category",
    tags=["Category"],
    status_code=201,
    operation_id="create_category",
    dependencies=[Depends(get_current_user)],
)
async def create_category(
    category: CategoryModels = Depends(CategoryModels.form),
    db      : Session        = Depends(get_db),
):
    # 1. Generate a unique, prefixed ID
    new_id = generate_id(db)

    # 2. Persist the image (if provided)
    image_filename: str | None = None
    if category.image and category.image.filename:
        image_filename = save_image(category.image)

    # 3. Insert the new record
    new_item = TBL_CATEGORY(
        id            = new_id,
        name          = category.name,
        name_lc       = category.name_lc,
        description   = category.description,
        image         = image_filename,
        active        = category.active
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    data = category_response(new_item)

    return {
        "ok"     : True,
        "status" : 201,
        "title"  : "Category",
        "message": "Data created successfully",
        "data"   : data,
        "error"  : {},
    }


@app.get(
    "/get_category",
    tags=["Category"],
    operation_id="get_category",
    dependencies=[Depends(get_current_user)],
)
async def get_category(
    page: int     = Query(default=1, ge=1),
    size: int     = Query(default=10, ge=1),
    db  : Session = Depends(get_db)
):
    base_query = db.query(TBL_CATEGORY).filter(TBL_CATEGORY.active == True)

    total   = base_query.count()
    results = base_query.order_by(TBL_CATEGORY.name\
                        .asc())\
                        .offset((page - 1) * size)\
                        .limit(size)\
                        .all()
    total_pages = math.ceil(total / size) if size else 1
    
    data_list = [category_response(c) for c in results]

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


@app.get(
    "/get_category/{category_id}",
    tags=["Category"],
    operation_id="get_category_by_id",
    dependencies=[Depends(get_current_user)],
)
async def get_category_by_id(
    category_id: str,
    db         : Session = Depends(get_db),
):
    item = db.query(TBL_CATEGORY).filter(TBL_CATEGORY.id == category_id).first()
    if not item:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "Category not found",
        )

    return {
        "ok"     : True,
        "status" : 200,
        "title"  : "Category",
        "message": "Data retrieved successfully",
        "data"   : category_response(item),
        "error"  : {},
    }


@app.put(
    "/update_category/{category_id}",
    tags         = ["Category"],
    operation_id = "update_category",
    dependencies = [Depends(get_current_user)],
)
async def update_category(
    category_id: str,
    category   : CategoryModels = Depends(CategoryModels.form),
    db         : Session        = Depends(get_db),
):
    item = db.query(TBL_CATEGORY).filter(TBL_CATEGORY.id == category_id).first()
    if not item:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "Category not found",
    )
    setattr(item, "name", category.name)
    setattr(item, "name_lc", category.name_lc)
    setattr(item, "description", category.description)
    setattr(item, "active", category.active)
    if category.image and category.image.filename: 
        setattr(item, "image", save_image(category.image))

    db.commit()
    db.refresh(item)
    
    return {
        "ok"     : True,
        "status" : 200,
        "title"  : "Category",
        "message": "Data updated successfully",
        "data"   : category_response(item),
        "error"  : {},
    }


@app.delete(
    "/delete_category/{category_id}",
    tags         = ["Category"],
    operation_id = "delete_category",
    dependencies = [Depends(get_current_user)],
)
async def delete_category(
    category_id: str,
    db         : Session = Depends(get_db),
):
    item = db.query(TBL_CATEGORY).filter(TBL_CATEGORY.id == category_id).first()
    if not item:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "Category not found",
        )

    data = category_response(item)
    image = cast(str | None, getattr(item, "image", None))
    delete_cloudinary_image(image)
    db.delete(item)
    db.commit()

    return {
        "ok"     : True,
        "status" : 200,
        "title"  : "Category",
        "message": "Data deleted successfully",
        "data"   : data,
        "error"  : {},
    }
