from sqlalchemy import Column, String, Boolean, Integer, Text
from core.db import Base

class TBL_SUB_MODULE(Base):
    __tablename__ = "tbl_sub_module"

    id        = Column(String(55), primary_key=True, unique=True)
    module_id = Column(String(55))
    name      = Column(String(150))
    name_lc   = Column(String(150))
    url       = Column(String(255))
    icon      = Column(Text)
    model     = Column(String(255))
    ordering  = Column(Integer)
    active    = Column(Boolean)