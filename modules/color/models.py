from sqlalchemy import Boolean, String, Column
from sqlalchemy.orm import relationship

from core.db import Base

class TBL_COLOR(Base):
    __tablename__ = "tbl_color"

    id        = Column(String(55), primary_key=True, unique=True)
    name      = Column(String(100))
    name_lc   = Column(String(100))
    hex_color = Column(String(100))
    active    = Column(Boolean, default=True)

    product_images = relationship(
        "TBL_PRODUCT_IMAGE",
        back_populates="color",
        lazy="selectin",
    )
