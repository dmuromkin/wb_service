from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from src.database import Base

class ABCAnalysis(Base):
    """
        Модель для хранения результатов ABC-анализа по предметам (subject)
        
        - id: уникальный идентификатор записи (primary key)
        - subject: наименование товара или предмета
        - revenue: выручка или доход по предмету за период
        - category: категория ABC ('A', 'B', 'C')
        - date_from: начало периода анализа
        - date_to: конец периода анализа
    """
    __tablename__ = "abc_analysis"

    id = Column(Integer, primary_key=True)
    subject = Column(String)
    revenue = Column(Float)
    category = Column(String(1))
    date_from = Column(DateTime, index=True)
    date_to = Column(DateTime, index=True)

    __table_args__ = (
        UniqueConstraint("subject", "date_from", "date_to", name="uix_period_subject"),
    )