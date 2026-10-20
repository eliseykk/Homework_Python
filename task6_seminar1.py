import csv
import random
from datetime import date, timedelta
from math import isfinite
from pathlib import Path


def generate_sales(path, count=5000, seed=None):
    if type(count) != int or count < 5000:
        raise ValueError("Нужно создать минимум 5000 продаж")
    generator = random.Random(seed)
    products = ["Book", "Pen", "Notebook", "Pencil", "Folder"]
    prices = {"Book": 500, "Pen": 80, "Notebook": 150, "Pencil": 40, "Folder": 120}
    first_date = date(2026, 1, 1)

    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "product", "quantity", "price"])
        for i in range(count):
            sale_date = first_date + timedelta(days=generator.randint(0, 30))
            product = generator.choice(products)
            quantity = generator.randint(1, 15)
            writer.writerow([sale_date.isoformat(), product, quantity, prices[product]])

            # Дополнительные ошибочные записи не уменьшают число правильных продаж.
            if i % 50 == 0:
                error_type = generator.randint(0, 4)
                if error_type == 0:
                    writer.writerow(["wrong_date", product, quantity, prices[product]])
                elif error_type == 1:
                    writer.writerow([sale_date.isoformat(), product, "abc", prices[product]])
                elif error_type == 2:
                    writer.writerow([sale_date.isoformat(), product, quantity, "wrong_price"])
                elif error_type == 3:
                    writer.writerow([sale_date.isoformat(), "", quantity, prices[product]])
                else:
                    writer.writerow([sale_date.isoformat(), product, -1, prices[product]])


def analyze_sales(path):
    total_sales = 0
    count = 0
    incorrect_count = 0
    products = {}
    days = {}

    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fields = ["date", "product", "quantity", "price"]
        if reader.fieldnames is None:
            raise ValueError("В файле нет заголовка CSV")
        for field in fields:
            if field not in reader.fieldnames:
                raise ValueError(f"В файле нет столбца {field}")

        for row in reader:
            try:
                if None in row:
                    raise ValueError("Лишние поля")
                sale_date = date.fromisoformat(row["date"]).isoformat()
                product = row["product"].strip()
                quantity = int(row["quantity"])
                price = float(row["price"])
                if not product or quantity <= 0 or price < 0 or not isfinite(price):
                    raise ValueError("Неверные данные продажи")
                revenue = quantity * price
                if not isfinite(revenue):
                    raise ValueError("Слишком большая сумма")
            except (ValueError, TypeError, AttributeError, OverflowError):
                incorrect_count += 1
                continue

            total_sales += revenue
            count += 1
            if product not in products:
                products[product] = {"quantity": 0, "revenue": 0}
            products[product]["quantity"] += quantity
            products[product]["revenue"] += revenue
            if sale_date not in days:
                days[sale_date] = 0
            days[sale_date] += revenue

    best_quantity_product = None
    best_revenue_product = None
    max_quantity = -1
    max_revenue = -1
    for product, stats in products.items():
        if stats["quantity"] > max_quantity:
            max_quantity = stats["quantity"]
            best_quantity_product = product
        if stats["revenue"] > max_revenue:
            max_revenue = stats["revenue"]
            best_revenue_product = product

    best_day = None
    max_day_revenue = -1
    for day, revenue in days.items():
        if revenue > max_day_revenue:
            max_day_revenue = revenue
            best_day = day

    average_purchase = 0
    if count != 0:
        average_purchase = total_sales / count
    return {
        "total_sales": total_sales,
        "best_quantity_product": best_quantity_product,
        "best_revenue_product": best_revenue_product,
        "average_purchase": average_purchase,
        "best_day": best_day,
        "valid_count": count,
        "incorrect_count": incorrect_count,
    }


if __name__ == "__main__":
    path = Path(__file__).resolve().parent / "sales.csv"
    try:
        if not path.exists():
            generate_sales(path, seed=42)
        stats = analyze_sales(path)
    except (OSError, UnicodeDecodeError, csv.Error, ValueError) as error:
        print(f"Ошибка обработки CSV: {error}")
    else:
        print(f"Корректных продаж: {stats['valid_count']}")
        print(f"Пропущено записей: {stats['incorrect_count']}")
        if stats["valid_count"] == 0:
            print("Нет корректных продаж для расчёта статистики")
        else:
            print(f"Общая сумма продаж: {stats['total_sales']:.2f}")
            print(f"Самый продаваемый товар: {stats['best_quantity_product']}")
            print(f"Товар с максимальной выручкой: {stats['best_revenue_product']}")
            print(f"Средняя стоимость покупки: {stats['average_purchase']:.2f}")
            print(f"День с максимальной выручкой: {stats['best_day']}")
