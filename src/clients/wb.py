from fastapi import HTTPException
import httpx
from src.config import Settings

async def fetch_orders_from_wb(date_from: str):
    """
    Получение заказов Wildberries начиная с указанной даты

    Args:
        date_from (str): начальная дата

    Raises:
        HTTPException: 401: Некорректный токен API.
        HTTPException: 429: Превышен лимит запросов к Wildberries.
        HTTPException: 408: Таймаут запроса к Wildberries API.
        HTTPException: 502: Прочие ошибки внешнего сервиса.
    """
    
    url = "https://statistics-api.wildberries.ru/api/v1/supplier/orders"
    headers = {"Authorization": Settings.API_KEY}
    params = {"dateFrom": date_from}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params, headers=headers)
        
        if response.status_code == 401:
            detail = response.json().get("detail", "Unauthorized")
            raise HTTPException(status_code=401, detail=f"Ошибка авторизации: {detail}")
        
        if response.status_code == 429:
            detail = response.json().get("detail", "Request limit exceeded")
            raise HTTPException(status_code=429, detail=f"Wildberries API: превышен лимит запросов. Детали: {detail}")
        
    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="Превышено время ожидания Wildberries API. Повторите запрос позже")
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка Wildberries API: {e.response.status_code}")

    response.raise_for_status()
    
    return response.json()