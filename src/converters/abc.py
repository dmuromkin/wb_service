from src.schemas.abc import ABCResultSchema
from src.models.abc import ABCAnalysis

def model_to_abc_schema(model: ABCAnalysis) -> ABCResultSchema:
    """
    Конвертер данных из БД в модель ABCResultSchema
    
    Args:
        model (ABCAnalysis): модель данных в БД

    Returns:
        ABCResultSchema: модель для возврата данных в endpoint
    """
    return ABCResultSchema(
        id=model.id,
        subject=model.subject,
        revenue=model.revenue,
        category=model.category,
        date_from=model.date_from,
        date_to=model.date_to,
    )