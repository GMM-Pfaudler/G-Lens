from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FullBOMComparisonTbl(Base):
    __tablename__ = "full_bom_comparison_tbl"

    id = Column(Integer, primary_key=True, index=True)
    generation_date = Column(DateTime, nullable=False)
    comparison_file_path = Column(String(255), nullable=False)
    file1_name = Column(String(255), nullable=True)
    file2_name = Column(String(255), nullable=True)
    bom_level = Column(String(10), nullable=True)
