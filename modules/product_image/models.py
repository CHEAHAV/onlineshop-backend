from sqlalchemy import Boolean, Column, String, Text

from core.db import Base

class TBL_PRODUCT_IMAGE(Base):
    __tablename__ = "tbl_product_image"

    id             = Column(String(55), primary_key= True, unique=True)
    title          = Column(String(255))
    title_lc       = Column(String(255))
    description    = Column(Text)
    description_lc = Column(Text)
    color_id       = Column(String(55))
    image          = Column(String(255))
    active         = Column(Boolean)