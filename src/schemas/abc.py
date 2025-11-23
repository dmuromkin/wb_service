from datetime import datetime
from pydantic import BaseModel

class ABCResultSchema(BaseModel):
    """
        Модель объекта из ABC анализа 
    """
    id: int | None = None
    subject: str
    revenue: float
    category: str
    date_from: datetime
    date_to: datetime