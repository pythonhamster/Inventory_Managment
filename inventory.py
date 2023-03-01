import csv
import os
import datetime


class RiskError(Exception):
    def __init__(self, message):
        self.message = message


class DataError(Exception):
    def __init__(self, message):
        self.message = message


def validator(word):
    wordlist = word.upper().split(" ")
    with open("invalid.txt", "r") as f:
        contents = f.read().split("\n")
        for word in wordlist:
            if word in contents:
                raise RiskError("Input Risk")
    return word.lower()


def open_file():
    with open("inventory.csv", "r") as f:
        reader = csv.DictReader(f)
        complete_products = []
        product_names = []
        for product in reader:
            complete_products.append(product)
            product_names.append(product["item"])
    return product_names, complete_products


def write_file(products):
    with open("inventory.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["item", "price", "quantity"])
        writer.writeheader()
        writer.writerows(products)


def logger(event_type):
    if os.path.getsize("log.csv") == 0:
        with open("log.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=["event type", "time"])
            writer.writeheader()
            writer.writerow({"event type": event_type, "time": datetime.datetime.now()})
        return
    with open("log.csv", "a") as f:
        f.seek(2)
        writer = csv.DictWriter(f, fieldnames=["event type", "time"])
        writer.writerow({"event type": event_type, "time": datetime.datetime.now()})


def search():
    product_names, complete_products = open_file()
    if not product_names or not complete_products:
        raise DataError("Data not found")
    product = validator(input("what product do you want: "))
    if product in product_names:
        for full_item in complete_products:
            if full_item["item"] == product:
                print(
                    f"Product: {full_item['item']} | Price: ${full_item['price']} | Quantity: {full_item['quantity']}")
    else:
        print("Product not found")
    logger("search")


def add():
    product_names, complete_products = open_file()
    product = validator(input("what product do you want to add: "))
    if product not in product_names:
        price = float(validator(input("what is the price: ")))
        quantity = int(validator(input("what is the quantity: ")))
        complete_products.append({"item": product, "price": price, "quantity": quantity})
        write_file(complete_products)
        print("Success!")
    else:
        print("Product already exists")
    logger("add")


def view():
    product_names, complete_products = open_file()
    if not product_names or not complete_products:
        raise DataError("Data not found")
    print(complete_products)
    logger("view")


def update():
    product_names, complete_products = open_file()
    product = validator(input("What is the product you want to update?: "))
    if product in product_names:
        price = validator(input("Enter the new price: "))
        quantity = validator(input("Enter the new quantity: "))
        for index, full_product in enumerate(complete_products):
            if full_product["item"] == product:
                complete_products[index] = {"item": product, "price": price, "quantity": quantity}
        write_file(complete_products)
        print("Success!")
    else:
        print("Your product was not found")
    logger("update")


def delete():
    product_names, complete_products = open_file()
    product = validator(input("What is the product you want to delete?: "))
    if product in product_names:
        for index, full_product in enumerate(complete_products):
            if full_product["item"] == product:
                del complete_products[index]
        write_file(complete_products)
        print("Success!")
    else:
        print("Your product was not found")
    logger("delete")


def main():
    for _ in range(15):
        try:
            options = {1: add, 2: view, 3: update, 4: delete, 5: search, 6: quit}
            print("\nSelect one")
            for key, value in options.items():
                if value != quit:
                    print(f"{key}. {value.__name__}")
                else:
                    print(f"{key}. {value.name}")
            choice = int(validator(input(">>>: ")))
            options[choice]()
        except (ValueError, FileNotFoundError, DataError, RiskError) as e:
            print(e)


main()