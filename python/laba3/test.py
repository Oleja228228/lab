#класс буфет, добавлнеи товаров , у товаров свои характеристики(цена,...) пользовательский ввод добвялть товары удалять, выбиратьи суммировать их цены выыодя и сохраняя чек а файл, прописать exception
class ProductError(Exception):
    pass


class ProductNotFound(ProductError):
    pass


class InvalidPrice(ProductError):
    pass


class EmptyBuffetError(ProductError):
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
        self.receipt_items = []

    def add_product(self, product: Product):
        self.items.append(product)

    def add_to_receipt(self, index: int):
        if index < 1 or index > len(self.items):
            raise ProductNotFound("Нет такого товара!")
        self.receipt_items.append(self.items[index - 1])

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

    def list_receipt(self):
        if not self.receipt_items:
            print("Чек пуст.")
            return

        print("Товары в чеке:")
        for i, p in enumerate(self.receipt_items, 1):
            print(f"{i}. {p}")

        total = sum(p.price for p in self.receipt_items)
        print(f"\nСумма чека: {total} руб.")

    def sum_selected(self, indexes):
        total = 0
        for i in indexes:
            if i < 1 or i > len(self.items):
                raise ProductNotFound(f"Товар с номером {i} не существует!")
            total += self.items[i - 1].price
        return total

    def save_receipt(self, filename="chek.txt"):
        if not self.receipt_items:
            raise EmptyBuffetError("Чек пуст — нечего сохранять!")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("=== ЧЕК ===\n")
            for p in self.receipt_items:
                f.write(f"{p.name} — {p.price} руб.\n")
            f.write(f"Итого: {sum(p.price for p in self.receipt_items)} руб.\n")

        print("Чек сохранён!")


def main():
    buf = Buffet()

    while True:
        print("""
=== МЕНЮ ===
1. Добавить товар в буфет
2. Удалить товар
3. Показать товары буфета
4. Добавить товар в чек
5. Показать чек
6. Сохранить чек
7. Сложить выбранные товары
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
                print("Удалено!")

            elif choice == "3":
                buf.list_products()

            elif choice == "4":
                buf.list_products()
                num = int(input("Введите номер товара для добавления в чек: "))
                buf.add_to_receipt(num)
                print("Добавлено в чек!")

            elif choice == "5":
                buf.list_receipt()

            elif choice == "6":
                buf.save_receipt()

            elif choice == "7":
                buf.list_products()
                nums = input("Введите номера товаров через пробел: ")
                indexes = list(map(int, nums.split()))
                total = buf.sum_selected(indexes)
                print("Сумма выбранных товаров:", total, "руб.")

            elif choice == "0":
                print("Выход...")
                break

            else:
                print("Неверный пункт меню!")

        except Exception as e:
            print("Ошибка:", e)


if __name__ == "__main__":
    main()
