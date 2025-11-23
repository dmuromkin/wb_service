from datetime import datetime
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select
from src.models.abc import ABCAnalysis


async def get_abc_results_for_period(
    db: AsyncSession,
    date_from: datetime,
    date_to: datetime
)-> Sequence[ABCAnalysis]:
    """
    Поиск существующего расчета ABC за период

    Args:
        db (AsyncSession): БД
        date_from (datetime): Начальная дата
        date_to (datetime): Конечная дата

    Returns:
        Sequence[ABCAnalysis]: ABC по товарам за период
    """
    
    query = (
        select(ABCAnalysis)
        .where(
            ABCAnalysis.date_from == date_from,
            ABCAnalysis.date_to == date_to
        )
    )
    result = await db.execute(query)
    
    return result.scalars().all()

async def save_abc_results(
    db: AsyncSession,
    results: List[Dict],
    date_from: datetime,
    date_to: datetime
) -> List[ABCAnalysis]:
    """
    Сохранение посчитанного ABC за период

    Args:
        db (AsyncSession): БД
        results (List[Dict]): Результаты расчетов
        date_from (datetime): Начальная дата
        date_to (datetime): Конечная дата

    Returns:
        List[ABCAnalysis]: ABC по товарам за период
    """
    
    objects = [
        ABCAnalysis(
            subject=r["subject"],
            revenue=r["revenue"],
            category=r["category"],
            date_from=date_from,
            date_to=date_to
        )
        for r in results
    ]

    db.add_all(objects)
    await db.commit()
    
    for obj in objects:
        await db.refresh(obj)
    
    return objects
