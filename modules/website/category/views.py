import math
from fastapi import Depends, Query
from sqlalchemy.orm import Session
from core.db_session import get_db
from main import website
from modules.category.models import TBL_CATEGORY
from modules.category.schemas import category_response

@website.get(
    "/get_category",
    tags=["Category"],
    operation_id="get_category",
)
async def get_category(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1),
    db: Session = Depends(get_db),
):
    base_query = db.query(TBL_CATEGORY).filter(TBL_CATEGORY.active == True)

    total = base_query.count()
    results = (
        base_query.order_by(TBL_CATEGORY.name.asc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    total_pages = math.ceil(total / size) if size else 1

    data_list = [category_response(c) for c in results]

    return {
        "ok": True,
        "status": 200,
        "title": "Category",
        "message": "Data retrieved successfully",
        "data": {
            "lists": data_list,
            "meta_data": {
                "total": total,
                "total_page": total_pages,
                "current_page": page,
                "size": size,
            },
        },
        "error": {},
    }
