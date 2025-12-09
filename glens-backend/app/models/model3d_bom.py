from sqlalchemy import Column,Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base =  declarative_base()


class Model3DBOMComparisonTbl(Base):
    __tablename__ = "modelbom_modelbom_comparison_tbl"

    id = Column(Integer,primary_key=True, index=True)
    generation_date = Column(DateTime, nullable=False)
    comparison_file = Column(String(255),nullable=False)
    model_a_file = Column(String(255), nullable=False)
    model_b_file = Column(String(255),nullable=False)