from core.db import Base
from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, Integer
from sqlalchemy.orm import relationship

class TBL_PRODUCT(Base):
    __tablename__ = "tbl_product"

    id                      = Column(String(55), primary_key= True, unique= True)
    category_id             = Column(String(55), ForeignKey("tbl_category.id"))
    name                    = Column(String(150))
    name_lc                 = Column(String(150))
    product_qty             = Column(Integer)
    out_stock               = Column(Integer)
    in_stock                = Column(Integer)
    rating                  = Column(Numeric(5,2))
    viewer                  = Column(Integer)
    original_price          = Column(Numeric(5,2))
    old_price               = Column(Numeric(5,2))
    selling_price           = Column(Numeric(5,2))
    discount                = Column(Numeric(5,2))
    saving_price            = Column(Numeric(5,2))
    profit_price            = Column(Numeric(5,2))
    profit_percentage       = Column(Numeric(5,2))
    total_price_in_stock    = Column(Numeric(5,2))
    total_price_out_stock   = Column(Numeric(5,2))
    total_original_price    = Column(Numeric(5,2))
    total_selling_price     = Column(Numeric(5,2))
    total_profit_price      = Column(Numeric(5,2))
    total_profit_percentage = Column(Numeric(5,2))
    product_image_id        = Column(String(55), ForeignKey("tbl_product_image.id"))
    shipping                = Column(Numeric(5,2))
    badge                   = Column(String(100))
    is_favorite             = Column(Boolean, default=False)
    is_new                  = Column(Boolean, default=True)
    active                  = Column(Boolean, default=True)

    category = relationship(
        "TBL_CATEGORY",
        back_populates="products",
        lazy="selectin",
    )
    product_image = relationship(
        "TBL_PRODUCT_IMAGE",
        back_populates="products",
        lazy="selectin",
    )
