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


class SalesApp:
    def __init__(self, master):
        self.master = master
        master.title('Sales and Price Charts')

        # Label
        self.label = ttk.Label(master,
                               text="Enter Product Name:"
                                    "(Itemx which x in [0-19])")
        self.label.pack()

        # Entry
        self.entry = ttk.Entry(master)
        self.entry.pack()

        # Button
        self.submit_button = ttk.Button(master, text="Submit",
                                        command=self.plot_data)
        self.submit_button.pack()

        self.sales_data = self.load_data(FILE_ADDRESS)
        self.add_price_field()

    @staticmethod
    @log_decorator
    def load_data(file_name: str = FILE_ADDRESS):
        try:
            data_frame = pd.read_json(file_name)
            return data_frame
        except FileNotFoundError:
            logging.error("sales_data.json file not found.")
            messagebox.showerror(title="Error",
                                 message="Data file not found.")
            return None
        except Exception as e:
            logging.error(msg=f"Error: {e}")
            messagebox.showerror(title="Error",
                                 message=f"{e}. Please try again.")
            return None

    def add_price_field(self):
        field = self.sales_data["total_price"].div(self.sales_data["count"])
        self.sales_data["price"] = field

    @log_decorator
    def plot_data(self):
        product_name = self.entry.get()
        try:
            query_str = f"title == '{product_name}'"
            product_orders = self.sales_data.query(query_str)
            if product_orders.empty:
                raise KeyError

            months = product_orders["month"].drop_duplicates().sort_values()
            item_month_prices = self.mean_prices_per_month(product_orders,
                                                           months=months,
                                                           )

            item_sales_per_month = self.sales_per_month(product_orders,
                                                        months=months,
                                                        )
            self.plot_figs(x_data=months,
                           y_data=item_sales_per_month,
                           x_label="Month",
                           y_label="Sales",
                           title=f"Sales per month for {product_name}",
                           color='tab:red'
                           )

            self.plot_figs(x_data=months,
                           y_data=item_month_prices,
                           x_label="Month",
                           y_label="Price",
                           title=f"Price per month for {product_name}",
                           color='tab:blue'
                           )

        except KeyError:
            logging.error(f"Product {product_name} not found.")
            messagebox.showerror(title="Error",
                                 message=f"{product_name} is incorrect.")

        except Exception as e:
            logging.error(msg=f"Error: {e}")
            messagebox.showerror(title="Error",
                                 message=f"{e}. Please try again.")

    @staticmethod
    @log_decorator
    def plot_figs(x_data,
                  y_data,
                  x_label: str,
                  y_label: str,
                  title: str,
                  color: str):
        fig, ax = plt.subplots()
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label, color=color)
        ax.set_title(title)
        ax.plot(x_data, y_data)
        ax.tick_params(axis='y')
        fig.tight_layout()
        plt.show()

    @staticmethod
    @log_decorator
    def mean_prices_per_month(product_orders_in, months: list):
        mean_prices = list()
        for month in months:
            query_str = f"month == {month}"
            mean_price = product_orders_in.query(query_str)["price"].mean()
            mean_prices.append(mean_price)
        return pd.DataFrame(mean_prices)

    @staticmethod
    @log_decorator
    def sales_per_month(product_orders_in, months: list):
        total_sales = list()
        for month in months:
            query_str = f"month == {month}"
            total_sale = product_orders_in.query(query_str)["count"].sum()
            total_sales.append(total_sale)
        return pd.DataFrame(total_sales)


def main():
    root = tk.Tk()
    SalesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
