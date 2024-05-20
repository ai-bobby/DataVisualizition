"""this function provide a json file that contains sales data of a mall"""
from abc import ABC, abstractmethod
from icecream import ic
import json
import logging
import random


logging.basicConfig(level=logging.INFO)


def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"{func.__name__} was called")
        return func(*args, **kwargs)

    return wrapper


class BaseModel(ABC):
    def __init__(self):
        self.is_active = False

    def __str__(self):
        raise NotImplementedError('Please implement this method')

    @abstractmethod
    @log_decorator
    def to_json(self):
        pass

    @abstractmethod
    @log_decorator
    def to_dictionary(self):
        pass


class ShopItemInfo(BaseModel):
    def __init__(self, data):
        super().__init__()
        self.is_active = True
        self.sold_info = dict()
        item_info = self.parse_item_info(data)
        (self.title, self.description, self.price,
         self.quantity, self.month) = item_info
        self.sold_count = 0

    def __str__(self):
        return (f'title = {self.title}, '
                f'is_active = {self.is_active}, '
                f'description = {self.description}, '
                f'price = {self.price}, '
                f'month = {self.month}, '
                f'quantity = {self.quantity}, '
                f'sold_count = {self.sold_count} ')

    @staticmethod
    @log_decorator
    def parse_item_info(data: dict):
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        month = data.get('month')
        quantity = data.get('quantity')
        return title, description, price, quantity, month

    @log_decorator
    def buy_item(self,
                 count: int,
                 ):
        if self.sold_count < self.quantity:
            self.sold_count += count
            self.quantity -= count

    @log_decorator
    def to_json(self):
        pass

    @log_decorator
    def to_dictionary(self):
        pass


class StoreOrder(BaseModel):
    def __init__(self, data):
        super().__init__()
        self.is_active = True
        order_info = self.parse_order_info(data)
        (self.customer_id, self.title, self.month,
         self.count, self.total_price) = order_info

    @staticmethod
    @log_decorator
    def parse_order_info(data: dict):
        customer_id = data.get('customer_id')
        title = data.get('title')
        month = data.get('month')
        count = data.get('count')
        total_price = data.get('total_price')
        return customer_id, title, month, count, total_price

    @log_decorator
    def to_dictionary(self):
        return {
            'customer_id': self.customer_id,
            'title': self.title,
            'month': self.month,
            'count': self.count,
            'total_price': self.total_price
        }

    @log_decorator
    def to_json(self):
        return json.dumps(self.to_dictionary())

    @log_decorator
    def __str__(self):
        return str(self.to_dictionary())


@log_decorator
def generate_shop_items(items_count: int) -> list:
    prices = [i for i in range(10, 200, 10)]
    titles = [f"Item{i}" for i in range(20)]
    descriptions = [f"Lorem {i}" for i in range(20)]
    shop_items = list()
    for i in range(items_count):
        item_info_dict = dict()
        item_info_dict['title'] = random.choice(titles)
        item_info_dict['description'] = random.choice(descriptions)
        item_info_dict['price'] = random.choice(prices)
        item_info_dict['quantity'] = random.randint(10000, 100000)
        item_info_dict['month'] = random.randint(1, 12)
        shop_item_info = ShopItemInfo(data=item_info_dict)
        shop_items.append(shop_item_info)
    return shop_items


@log_decorator
def erase_json_file_data(path: str):
    with open(path, "w") as outfile:
        data = dict()
        data["customer_id"] = dict()
        data["title"] = dict()
        data["month"] = dict()
        data["count"] = dict()
        data["total_price"] = dict()

        json.dump(data, outfile, ensure_ascii=False, indent=4)


@log_decorator
def write_json(new_data: dict, index: int, filename: str = 'sample.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["customer_id"][index] = new_data["customer_id"]
        file_data["title"][index] = new_data["title"]
        file_data["month"][index] = new_data["month"]
        file_data["count"][index] = new_data["count"]
        file_data["total_price"][index] = new_data["total_price"]
        file.seek(0)
        json.dump(file_data, file, indent=4)


@log_decorator
def generate_store_orders(orders_count: int, shop_items: list) -> dict:
    store_orders = dict()
    for i in range(orders_count):
        bought_item = random.choice(shop_items)
        order_data = dict()
        order_data['customer_id']: int = random.randint(1, 10)
        order_data['title']: int = bought_item.title
        order_data['month']: int = bought_item.month
        order_data['count']: int = random.randint(1, 10)
        order_data['total_price']: int = (bought_item.price *
                                          order_data['count'])
        bought_item.buy_item(count=order_data['count'])
        store_order = StoreOrder(data=order_data)
        store_orders[i] = store_order
    return store_orders


@log_decorator
def display_orders(store_orders: dict):
    for i in store_orders.keys():
        store_order = store_orders[i]
        ic(store_order.__str__())
        write_json(new_data=store_order.to_dictionary(),
                   index=i,
                   filename='sample.json')
    ic(len(store_orders))


@log_decorator
def display_items(shop_items: list):
    for shop_item in shop_items:
        ic(shop_item.__str__())
    ic(len(shop_items))


def main():
    erase_json_file_data(path='sample.json')
    shop_items = generate_shop_items(items_count=1000)
    orders_count = random.randint(1500, 2000)
    store_orders = generate_store_orders(orders_count=orders_count,
                                         shop_items=shop_items)
    display_items(shop_items=shop_items)
    display_orders(store_orders=store_orders)


if __name__ == "__main__":
    main()
