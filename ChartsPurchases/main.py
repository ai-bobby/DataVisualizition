import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import logging
import pandas as pd


FILE_ADDRESS = "../../1/1/sample.json"
# Setup logging
logging.basicConfig(level=logging.INFO)


def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"{func.__name__} was called")
        return func(*args, **kwargs)

    return wrapper


class CustomerApp:
    def __init__(self, master):
        self.master = master
        master.title('Customer Purchase Analysis')

        # Label
        self.label = ttk.Label(master, text="Enter Customer Code (1-10):")
        self.label.pack()

        # Entry
        self.entry = ttk.Entry(master)
        self.entry.pack()

        # Button
        self.submit_button = ttk.Button(master, text="Submit",
                                        command=self.analyze_data)
        self.submit_button.pack()

        self.customer_data = self.load_data(FILE_ADDRESS)

    @staticmethod
    @log_decorator
    def load_data(file_name: str = FILE_ADDRESS):
        try:
            data_frame = pd.read_json(file_name)
            return data_frame
        except FileNotFoundError:
            logging.error(f"{file_name} file not found.")
            messagebox.showerror(title="Error", message="Data file not found.")
            return None
        except Exception as e:
            logging.error(msg=f"Error: {e}")
            messagebox.showerror(title="Error",
                                 message=f"{e}. Please try again.")
            return None

    @log_decorator
    def analyze_data(self):
        customer_code = int(self.entry.get())
        try:
            query_str = f"customer_id == {customer_code}"
            customer_orders = self.customer_data.query(query_str)
            if customer_orders.empty:
                raise KeyError
            months = customer_orders["month"].drop_duplicates().sort_values()
            self.plot_purchases_per_month(customer_orders, months=months)

            query_str = f"customer_id == {customer_code}"
            customer_orders = self.customer_data.query(query_str)
            self.plot_amount_per_month(customer_orders, months=months)

            items = customer_orders["title"].drop_duplicates().sort_values()
            customer_orders = self.customer_data.query(query_str)
            self.plot_product_num_per_month(customer_orders, items=items)

        except KeyError:

            logging.error(f"Customer code {customer_code} not found.")

            messagebox.showerror(title="Error",
                                 message="Customer code "
                                 f"{customer_code} is incorrect.")

        except Exception as e:
            logging.error(msg=f"Error: {e}")
            messagebox.showerror(title="Error",
                                 message=f"{e}. Please try again.")

    @log_decorator
    def plot_purchases_per_month(self, customer_orders, months: list):
        order_per_month = self.order_per_month(customer_orders,
                                               months=months,
                                               )

        self.plot_bar_graph(x_data=months,
                            y_data=order_per_month,
                            x_label='Month',
                            y_label='Number of Purchases',
                            title='Number of Purchases Per Month',
                            color='red'
                            )

    @log_decorator
    def plot_amount_per_month(self, customer_orders, months: list):
        total_purchase_per_month = self.purchase_per_month(customer_orders,
                                                           months=months,
                                                           )
        self.plot_bar_graph(x_data=months,
                            y_data=total_purchase_per_month,
                            x_label='Month',
                            y_label='Amount Spent',
                            title='Total Amount Spent Per Month',
                            color='green'
                            )

    @log_decorator
    def plot_product_num_per_month(self, customer_orders, items: list):
        order_item_per_month = self.order_per_item(customer_orders,
                                                   items=items
                                                   )

        self.plot_bar_graph(x_data=items,
                            y_data=order_item_per_month,
                            x_label='Item',
                            y_label='Number of Purchases',
                            title='Number of Each Product Purchased',
                            color='orange'
                            )

    @staticmethod
    @log_decorator
    def plot_bar_graph(x_data,
                       y_data,
                       x_label: str,
                       y_label: str,
                       title: str,
                       color: str):
        plot_df = y_data
        plot_df.columns = [y_label]
        plot_df.index = x_data
        plot_df.plot(kind='bar', color=color)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

    @staticmethod
    @log_decorator
    def order_per_month(customer_orders, months: list):
        orders = list()
        for month in months:
            query_str = f"month == {month}"
            order = customer_orders.query(query_str)["count"].sum()
            orders.append(order)
        return pd.DataFrame(orders)

    @staticmethod
    @log_decorator
    def purchase_per_month(customer_orders, months: list):
        total_purchases = list()
        for month in months:
            query_str = f"month == {month}"
            print(customer_orders.query(query_str))
            print(customer_orders.query(query_str)["total_price"])
            total_p = customer_orders.query(query_str)["total_price"].sum()
            total_purchases.append(total_p)
        return pd.DataFrame(total_purchases)

    @staticmethod
    @log_decorator
    def order_per_item(customer_orders, items: list):
        total_purchases = list()
        for item in items:
            query_str = f"title == '{item}'"
            total_p = customer_orders.query(query_str)["total_price"].sum()
            total_purchases.append(total_p)
        return pd.DataFrame(total_purchases)


def main():
    root = tk.Tk()
    CustomerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
