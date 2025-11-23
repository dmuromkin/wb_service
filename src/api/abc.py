from fastapi import APIRouter, Query, Depends
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.services.abc_service import process_abc_analysis

router = APIRouter(prefix="/abc", tags=["ABC analysis"])

@router.get("/", 
            description="Вычисление ABC по данным заказов за заданный интервал",
            summary="Calculate ABC for period")

async def abc_analysis(
    dateFrom: datetime = Query(..., description="Начало периода (YYYY-MM-DD)"),
    dateTo: datetime = Query(..., description="Конец периода (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
):
    """EndPoint на запрос ABC за указанный период

    Args:
        dateFrom (datetime): Начальная дата.
        dateTo (datetime): Конечная дата.
        db (AsyncSession): Defaults to Depends(get_db).

    Returns:
        List[ABCResultSchema]: Результат расчета ABC
    """
    return await process_abc_analysis(
        db=db,
        date_from=dateFrom,
        date_to=dateTo,
    )
