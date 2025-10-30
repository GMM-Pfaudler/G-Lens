from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ModelRefBOMComparisonTbl(Base):
    __tablename__ = "model_ref_bom_comparison_tbl"

    id = Column(Integer, primary_key=True, index=True)
    generation_date = Column(DateTime, nullable=False)
    comparison_file_path = Column(String(255), nullable=False)
    model_bom_file = Column(String(255), nullable=True)
    ref_bom_file = Column(String(255), nullable=True)
