import sys
import sqlite3
import os
import pandas as pd
import quandl

DATABASE = "stocks.db"
API_FILE = "api_key.txt"
END_DATE = "2021-01-31"


def get_stock_data(stocks, end_date="2100-01-01"):
    """
    Retrieve the daily stock information for stocks
    """

    # Make sure we passed in correct stock information
    assert stocks, "ERROR: No stock ticker provided to retrieve stock information"
    assert isinstance(stocks, (list, str)), \
        f"ERROR: Stocks must be of type {type(list)} or {type(str)} - not type {type(stocks)}"

    # Get the data from the API
    try:
        return quandl.get_table("SHARADAR/SEP", ticker=stocks,
                                date={"lte": end_date}, paginate=True,
                                qopts={"columns": ['ticker', 'date', 'open', 'close']})

    except quandl.errors.quandl_error.InvalidRequestError as err:
        print(f"ERROR: {err.quandl_message}")
        sys.exit(1)

def create_database():
    """
    Create the database to store stock data
    """

    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('''CREATE TABLE stocks (
                    ticker text, 
                    date text,
                    open real,
                    close real)''')
    con.commit()
    con.close()


if __name__ == "__main__":

    # Set quandl api key    
    quandl.read_key(filename=API_FILE)

    # Read in stock data
    try:
        stock_info = pd.read_csv("50ipos.csv", header=0)
    except FileNotFoundError as err:
        print(f"ERROR: File {err.filename} not found")
        sys.exit(1)

    # Process the symbols to get ready to be passed into quandl
    symbols = stock_info["stock_symbol"].tolist()

    # Get the stock data from the API call
    data = get_stock_data(symbols, end_date=END_DATE)

    # Create the database if it doesn't exist
    if not os.path.isfile(DATABASE):
        create_database()

    # Add stock data to database
    conn = sqlite3.connect(DATABASE)
    data.to_sql("stocks", conn, if_exists="replace")
