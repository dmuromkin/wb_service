from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.converters.abc import model_to_abc_schema
from src.schemas.abc import ABCResultSchema
from src.clients.wb import fetch_orders_from_wb
from src.schemas.order import OrderSchema
from src.services.abc_calculator import calculate_abc
from src.repositories.abc import get_abc_results_for_period, save_abc_results


async def process_abc_analysis(
    db: AsyncSession,
    date_from: datetime,
    date_to: datetime,
)-> List[ABCResultSchema]:
    """
    Выполнение ABC анализа за период

    Args:
        db (AsyncSession): БД
        date_from (datetime): Начальная дата
        date_to (datetime): Конечная дата

    Returns:
        List[ABCResultSchema]: Результат расчета АВС
    """
    
    existing = await get_abc_results_for_period(db, date_from, date_to)

    # если в БД уже есть расчеты за заданный период - возвращаем их
    if existing:
        return [model_to_abc_schema(item) for item in existing]

    # Запрос заказов из WB API
    orders_raw = await fetch_orders_from_wb(date_from.isoformat())

    # Ограничение по конечной дате
    filtered_orders: List[OrderSchema] = []
    for o in orders_raw:
        order_dt = datetime.fromisoformat(o["date"])
        if date_from <= order_dt <= date_to:
            filtered_orders.append(OrderSchema(**o).dict())

    # ABC анализ
    abc_results = calculate_abc(filtered_orders)

    # Сохранение в БД
    result = await save_abc_results(db, abc_results, date_from, date_to)


    return [model_to_abc_schema(obj) for obj in result]
