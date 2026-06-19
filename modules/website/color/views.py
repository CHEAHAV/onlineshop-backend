import math
from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from core.api.user.views import get_current_user
from core.db_session import get_db
from main import website
from modules.color.models import TBL_COLOR
from modules.color.schemas import color_response


@website.get(
    "/get_color",
    tags=["Color"],
    operation_id="get_color",
)
async def get_color(
    page: int     = Query(default=1, ge=1),
    size: int     = Query(default=10, ge=1),
    db  : Session = Depends(get_db)
):
    base_query = db.query(TBL_COLOR).filter(TBL_COLOR.active == True)

    total   = base_query.count()
    results = base_query.order_by(TBL_COLOR.name\
                        .asc())\
                        .offset((page - 1) * size)\
                        .limit(size)\
                        .all()
    total_pages = math.ceil(total / size) if size else 1
    
    data_list = [color_response(c) for c in results]

    return {
        'ok'     : True,
        'status' : 200,
        'title'  : 'Color',
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
    "/get_color/{color_id}",
    tags=["Color"],
    operation_id="get_color_by_id",
    dependencies=[Depends(get_current_user)],
)
async def get_color_by_id(
    color_id: str,
    db         : Session = Depends(get_db),
):
    item = db.query(TBL_COLOR).filter(TBL_COLOR.id == color_id).first()
    if not item:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "Color not found",
        )

    return {
        "ok"     : True,
        "status" : 200,
        "title"  : "Color",
        "message": "Data retrieved successfully",
        "data"   : color_response(item),
        "error"  : {},
    }