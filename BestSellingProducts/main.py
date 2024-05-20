import matplotlib.pyplot as plt
import logging
import pandas as pd
import argparse


FILE_ADDRESS = "../../1/1/sample.json"
# Setup logging
logging.basicConfig(level=logging.INFO)


def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"{func.__name__} was called")
        return func(*args, **kwargs)

    return wrapper


class SalesReport:
    def __init__(self, file_name: str = FILE_ADDRESS):
        self.sales_data = self.load_data(file_name)

    @staticmethod
    @log_decorator
    def load_data(file_name: str = "sample.json"):
        try:
            data_frame = pd.read_json(file_name)
            return data_frame
        except FileNotFoundError:
            logging.error("sales_data.json file not found.")
            return None

    @log_decorator
    def find_most_sales_item(self) -> list:
        items = self.sales_data["title"].drop_duplicates().sort_values()
        df_items = pd.DataFrame(index=items,
                                columns=["total_sales"])
        for item in items:
            query_str = f"title == '{item}'"
            total_sale = self.sales_data.query(query_str)["count"].sum()
            df_items.loc[item] = total_sale
        df_items = df_items.sort_values(by="total_sales", ascending=False)
        return df_items.index[:5]

    @log_decorator
    def plot_sales_per_month(self, most_sales_item: list, axis):
        for item in most_sales_item:
            query_str = f"title == '{item}'"
            product_orders = self.sales_data.query(query_str)
            if product_orders.empty:
                raise KeyError
            months = product_orders["month"].drop_duplicates().sort_values()

            item_sales_per_month = self.sales_per_month(product_orders,
                                                        months=months,
                                                        )
            axis[0].plot(months, item_sales_per_month, label=item)

            # Naming the x-axis, y-axis and the whole graph
        axis[0].set_xlabel("Month")
        axis[0].set_ylabel("total_sale_count")
        axis[0].set_title("Total sale count per month for items")
        # Adding legend, which helps us recognize the curve according to
        # it's color
        axis[0].legend()

    @log_decorator
    def plot_purchase_per_month(self, most_sales_item: list, axis):
        for item in most_sales_item:
            query_str = f"title == '{item}'"
            product_orders = self.sales_data.query(query_str)
            if product_orders.empty:
                raise KeyError
            months = product_orders[
                "month"].drop_duplicates().sort_values()
            item_sales_per_month = self.purchase_per_month(product_orders,
                                                           months=months,
                                                           )
            axis[1].plot(months, item_sales_per_month, label=item)

            # Naming the x-axis, y-axis and the whole graph
        axis[1].set_xlabel("Month")
        axis[1].set_ylabel("Purchase")
        axis[1].set_title("Purchase per month for items")
        # Adding legend, which helps us recognize the curve according to
        # it's color
        axis[1].legend()

    @staticmethod
    @log_decorator
    def arg_input_parser() -> int:
        parser = argparse.ArgumentParser(
            description="Sales data visualisation"
        )
        parser.add_argument("-r",
                            "--report",
                            help="Report",
                            action='store_true',
                            )
        args = parser.parse_args()
        flag_value = args.report
        return flag_value

    @staticmethod
    @log_decorator
    def sales_per_month(product_orders_in, months: list):
        total_sales = list()
        for month in months:
            query_str = f"month == {month}"
            total_sale = product_orders_in.query(query_str)["count"].sum()
            total_sales.append(total_sale)
        return pd.DataFrame(total_sales)

    @staticmethod
    @log_decorator
    def purchase_per_month(product_orders_in, months: list):
        total_sales = list()
        for month in months:
            query_str = f"month == {month}"
            total_sale = product_orders_in.query(query_str)[
                "total_price"
            ].sum()
            total_sales.append(total_sale)
        return pd.DataFrame(total_sales)


def main():
    sale_report = SalesReport(file_name=FILE_ADDRESS)
    if sale_report.arg_input_parser():
        most_sale_items = sale_report.find_most_sales_item()
        figure, axis = plt.subplots(nrows=1, ncols=2)
        sale_report.plot_sales_per_month(most_sale_items, axis)
        sale_report.plot_purchase_per_month(most_sale_items, axis)
        # To load the display window
        plt.show()
    else:
        logging.info("No arguments entered")


if __name__ == "__main__":
    main()
