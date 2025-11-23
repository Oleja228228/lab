#класс буфет, добавлнеи товаров , у товаров свои характеристики(цена,...) пользовательский ввод добвялть товары удалять, выбиратьи суммировать их цены выыодя и сохраняя чек а файл, прописать exception
class ProductError(Exception):
    pass


class ProductNotFound(ProductError):
    pass


class InvalidPrice(ProductError):
    pass


class Product:
    def __init__(self, name: str, price: float):
        if price < 0:
            raise InvalidPrice("Цена не может быть отрицательной!")

        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} — {self.price} руб."


class Buffet:
    def __init__(self):
        self.items = []

    def add_product(self, product: Product):
        self.items.append(product)

    def remove_product(self, name: str):
        for i, p in enumerate(self.items):
            if p.name == name:
                del self.items[i]
                return
        raise ProductNotFound(f"Товар '{name}' не найден!")

    def list_products(self):
        if not self.items:
            print("Буфет пуст.")
            return
        print("Список товаров:")
        for i, p in enumerate(self.items, 1):
            print(f"{i}. {p}")

    def total_price(self):
        return sum(p.price for p in self.items)

    def total_selected(self, indexes):
        total = 0
        for i in indexes:
            if i < 1 or i > len(self.items):
                raise ProductNotFound(f"Товар с номером {i} не существует!")
            total += self.items[i - 1].price
        return total

    def save_receipt(self, filename="chek.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=== ЧЕК ===\n")
            for p in self.items:
                f.write(f"{p.name} — {p.price} руб.\n")
            f.write(f"Итого: {self.total_price()} руб.\n")


def main():
    buf = Buffet()

    while True:
        print("""
=== МЕНЮ ===
1. Добавить товар
2. Удалить товар
3. Показать товары
4. Показать сумму
5. Сохранить чек
0. Выход
""")
        choice = input("Ваш выбор: ")

        try:
            if choice == "1":
                name = input("Название товара: ")
                price = float(input("Цена: "))
                buf.add_product(Product(name, price))
                print("Товар добавлен!")

            elif choice == "2":
                name = input("Название товара для удаления: ")
                buf.remove_product(name)
                print("Товар удалён.")

            elif choice == "3":
                buf.list_products()

            elif choice == "4":
                print("""
1. Сумма всех товаров
2. Сумма выбранных товаров
""")
                sub = input("Выбор: ")

                if sub == "1":
                    print("Сумма всех товаров:", buf.total_price(), "руб.")

                elif sub == "2":
                    buf.list_products()
                    nums = input("Введите номера товаров через пробел: ")
                    indexes = list(map(int, nums.split()))
                    total = buf.total_selected(indexes)
                    print("Сумма выбранных товаров:", total, "руб.")

                else:
                    print("Неверный выбор!")

            elif choice == "5":
                buf.save_receipt()
                print("Чек сохранён в chek.txt")

            elif choice == "0":
                print("Выход...")
                break

            else:
                print("Неизвестный пункт меню!")

        except Exception as e:
            print("Ошибка:", e)


if __name__ == "__main__":
    main()
