from datetime import date, timedelta
from math import isfinite


class Product:
    def __init__(self, name, price, quantity):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название товара не должно быть пустым")
        if not isfinite(price) or price < 0:
            raise ValueError("Цена должна быть конечной и неотрицательной")
        if type(quantity) != int or quantity < 0:
            raise ValueError("Количество должно быть целым неотрицательным числом")
        self.name = name.strip()
        self.price = price
        self.quantity = quantity

    def final_price(self):
        return self.price


class Book(Product):
    def __init__(self, name, price, quantity, author, discount=0):
        super().__init__(name, price, quantity)
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Нужно указать автора")
        if not isfinite(discount) or not 0 <= discount <= 100:
            raise ValueError("Скидка должна быть от 0 до 100 процентов")
        self.author = author
        self.discount = discount

    def final_price(self):
        return round(self.price * (1 - self.discount / 100), 2)


class Electronic(Product):
    def __init__(self, name, price, quantity, warranty_months, warranty_price=0):
        super().__init__(name, price, quantity)
        if type(warranty_months) != int or warranty_months < 0:
            raise ValueError("Срок гарантии должен быть целым неотрицательным числом")
        if not isfinite(warranty_price) or warranty_price < 0:
            raise ValueError("Цена дополнительной гарантии не может быть отрицательной")
        self.warranty_months = warranty_months
        self.warranty_price = warranty_price

    def final_price(self):
        return round(self.price + self.warranty_price, 2)


class Food(Product):
    def __init__(self, name, price, quantity, expiration_date):
        super().__init__(name, price, quantity)
        if isinstance(expiration_date, str):
            expiration_date = date.fromisoformat(expiration_date)
        if not isinstance(expiration_date, date):
            raise ValueError("Нужно указать дату окончания срока годности")
        self.expiration_date = expiration_date

    def final_price(self):
        if self.expiration_date < date.today():
            raise ValueError("Срок годности товара истёк")
        return self.price


class Store:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Нужно передать товар Product или его наследника")
        if self.find_product(product.name) is not None:
            raise ValueError("Товар с таким названием уже есть")
        self.products.append(product)

    def find_product(self, name):
        for product in self.products:
            if product.name.casefold() == name.strip().casefold():
                return product
        return None

    def sell_product(self, name, quantity):
        if type(quantity) != int or quantity <= 0:
            raise ValueError("Количество для продажи должно быть положительным целым")
        product = self.find_product(name)
        if product is None:
            raise ValueError("Товар не найден")
        if quantity > product.quantity:
            raise ValueError("Недостаточно товара на складе")
        total_price = round(product.final_price() * quantity, 2)
        product.quantity -= quantity
        return total_price


if __name__ == "__main__":
    store = Store()
    store.add_product(Book("Python", 1000, 5, "Автор учебника", discount=10))
    store.add_product(Electronic("Phone", 30000, 2, 12, warranty_price=1000))
    store.add_product(Food("Milk", 100, 10, date.today() + timedelta(days=7)))

    # Один метод вызывается у объектов разных классов.
    for product in store.products:
        print(f"{product.name}: цена {product.final_price()}, остаток {product.quantity}")
    try:
        total_price = store.sell_product("Python", 2)
        print(f"Сумма покупки: {total_price:.2f}")
        print("Осталось книг:", store.find_product("Python").quantity)
        store.sell_product("Phone", 10)
    except ValueError as error:
        print(f"Ошибка продажи: {error}")
