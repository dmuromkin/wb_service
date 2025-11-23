from pydantic import BaseModel
from datetime import datetime

class OrderSchema(BaseModel):
    """
        Модель заказа из WB API 
    """
    date: datetime
    lastChangeDate: datetime
    countryName: str
    oblastOkrugName: str
    regionName: str
    supplierArticle: str
    nmId: int
    category: str
    subject: str
    brand: str
    techSize: str   
    totalPrice: float
    discountPercent: int
    spp: float
    finishedPrice: float
    priceWithDisc: float    
    isCancel: bool
    sticker: str