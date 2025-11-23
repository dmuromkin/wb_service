from collections import defaultdict
from typing import List, Dict

def calculate_abc(orders: List[dict]) -> List[Dict]:
    """
    Ф-ция расчета АВС по списку заказов

    Args:
        orders (List[dict]): список заказов

    Returns:
        List[Dict]: Расчитанный ABC для товаров
    """
    
    sales_count_by_subject_price = defaultdict(lambda: defaultdict(int))

    for order in orders:
        if order.get("isCancel"):
            continue

        subject = order["subject"]
        price = order["priceWithDisc"]

        sales_count_by_subject_price[subject][price] += 1

    # Расчет выручки по товарам
    revenue_by_subject = {
        subject: sum(price * qty for price, qty in prices.items())
        for subject, prices in sales_count_by_subject_price.items()
    }

    # Расчет общей выручки
    total_revenue = sum(revenue_by_subject.values())
    # Сортировка по убыванию выручки
    sorted_subjects = sorted(revenue_by_subject.items(), key=lambda x: x[1], reverse=True)

    cumulative = 0
    results = []

    for subject, revenue in sorted_subjects:
        cumulative += revenue
        share = cumulative / total_revenue if total_revenue else 0

        # Присвоение ABC-категории
        if share <= 0.8:
            category = "A"
        elif share <= 0.95:
            category = "B"
        else:
            category = "C"

        results.append({
            "subject": subject,
            "revenue": revenue,
            "category": category
        })

    return results
