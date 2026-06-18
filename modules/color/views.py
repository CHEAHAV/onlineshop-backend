import math
from main import app
from sqlalchemy.orm import Session
from modules.color.models import TBL_COLOR
from fastapi import Depends, Query
from core.api.user.views import get_current_user
from core.db_session import get_db
from modules.color.schemas import *

@app.post("/create_color", tags=["Color"], status_code=201, operation_id="create_color", dependencies=[Depends(get_current_user)])
async def create_color(
    color : ColorModels = Depends(ColorModels.form),
    db : Session = Depends(get_db)
): 
    new_id = generate_id(db)
    new_item = TBL_COLOR(
        id        = new_id,
        name      = color.name,
        name_lc   = color.name_lc,
        hex_color = color.hex_color,
        active    = True,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return{
        "ok"     : True,
        "status" : 201,
        "title"  : "Color",
        "message": "Data created successfully",
        "data"   : color_response(new_item),
        "error" : {},
    }



@app.get(
    "/get_color",
    tags=["Color"],
    operation_id="get_color",
    dependencies=[Depends(get_current_user)],
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
