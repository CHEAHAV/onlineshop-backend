from sqlalchemy import Boolean, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from core.db import Base

class TBL_PRODUCT_IMAGE(Base):
    __tablename__ = "tbl_product_image"

    id             = Column(String(55), primary_key= True, unique=True)
    title          = Column(String(255))
    title_lc       = Column(String(255))
    description    = Column(Text)
    description_lc = Column(Text)
    color_id       = Column(String(55), ForeignKey("tbl_color.id"))
    image          = Column(String(255))
    active         = Column(Boolean)

    color = relationship(
        "TBL_COLOR",
        back_populates="product_images",
        lazy="selectin",
    )
    products = relationship(
        "TBL_PRODUCT",
        back_populates="product_image",
        lazy="selectin",
    )
