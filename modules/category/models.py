from sqlalchemy import Boolean, String, Column
from core.db import Base


class TBL_CATEGORY(Base):
    __tablename__ = "tbl_category"

    id          = Column(String(55), primary_key=True, unique=True)
    name        = Column(String(255), nullable=False)
    name_lc     = Column(String(255), nullable=True)
    description = Column(String(500), nullable=True)
    image       = Column(String(500), nullable=True)
    active      = Column(Boolean, default=True)
