import sqlite3
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

pd.set_option('display.max_rows', None)
DATABASE = "stocks.db"

def get_data(table="stocks"):
    """
    Retrieve the data from the database
    """

    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql(f"SELECT ticker, date, close FROM {table}", conn)
    return df

def monthly_prices(data, rev=False):
    """
    Utility function to get the monthly prices
    """

    if rev:
        data = data[::-1]

    datalist = []
    prev_month = None
    for row in data.iterrows():

        if not prev_month:
            prev_month = int(row[1][1].split('-')[1])
            datalist.append([row[1][0], row[1][1].split(" ")[0], row[1][2]])
        else:
            new_month = int(row[1][1].split('-')[1])
            if new_month == (prev_month + 1) or (prev_month == 12 and new_month == 1):
                datalist.append([row[1][0], row[1][1].split(" ")[0], row[1][2]])
                prev_month = new_month

    return datalist

def get_monthly_data(data, rua_data):
    """
    Get the closing price for each stock at the beginning of each month
    """

    symbols = data['ticker'].unique()
    datalist = []           # Temporarily store stock data as a list

    for symbol in symbols:
        local_data = data.loc[data['ticker'] == symbol]     # Get stock price for this symbol

        datalist += monthly_prices(local_data, rev=True)

    rua = rua_data[['Date', 'Close']]
    rua['ticker'] = "RUA"
    rua = rua.dropna()

    # Make sure the columns are in correct order
    first_column = rua.pop('ticker') 
    rua.insert(0, 'ticker', first_column) 

    datalist += monthly_prices(rua)
    monthly = pd.DataFrame(datalist, columns=['ticker', 'date', 'close'])

    return monthly

def calculate_net_perc_change(data):
    """
    Calculate the net percentage change per month for each stock and plot them
    """

    symbols = data['ticker'].unique()
    temp_data = []

    for symbol in symbols:
        local_data = data.loc[data['ticker'] == symbol]

        orig_price = None
        for row in local_data.iterrows():

            if not orig_price:
                orig_price = row[1][-1]
            else:
                new_price = row[1][-1]
                perc_diff = ((new_price - orig_price) / orig_price) * 100
                temp_data.append([row[1][0], row[1][1], perc_diff])
                orig_price = new_price

    return pd.DataFrame(temp_data, columns=['ticker', 'date', 'perc_change'])

def plot_perc_change(change):
    """
    Plots the percentage change per month for each stock
    """

    # First handle RUA
    rua_dates = []
    rua_perc_change = []
    rua_data = change.loc[change['ticker'] == "RUA"]

    for row in rua_data.iterrows():
        rua_dates.append(datetime.strptime(row[1][1], "%Y-%m-%d").date())
        rua_perc_change.append(row[1][2])

    i = 0
    figs = []
    for symbol in change['ticker'].unique():
        if symbol != "RUA":

            # Create the figure if need be
            if i % 9 == 0:
                i = 0
                fig = plt.figure(figsize=(22, 8))
                grid = plt.GridSpec(3, 3, wspace = .25, hspace = 0.75)
                figs.append(fig)


            local_data = change.loc[change['ticker'] == symbol]

            # Retrieve data for processing
            dates = []
            perc_change = []
            for row in local_data.iterrows():
                dates.append(datetime.strptime(row[1][1], "%Y-%m-%d").date())
                perc_change.append(row[1][2])

            idx = rua_dates.index(dates[0])

            # Plotting details
            ax = plt.subplot(grid[i])
            plt.plot(dates, perc_change, 'g', label=symbol)
            plt.plot(dates, rua_perc_change[idx+1:], '-r', linewidth=1.0, label="RUA")
            plt.title(f"{symbol}")
            plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
            plt.axhline(0, color='black', linewidth=0.75)
            plt.grid(b=True)
            plt.legend()
            fmt = '{x:,.0f}%'
            tick = mtick.StrMethodFormatter(fmt)
            ax.yaxis.set_major_formatter(tick) 

            i += 1

    # Save the figures
    for i, fig in enumerate(figs):
        fig.savefig(f"plots/percentage_change_page_{i}.png")

if __name__ == "__main__":

    # Get data from database and from RUA
    stock_data = get_data()
    market_data = pd.read_csv("data/RUA.csv")

    # Following code to get monthly net change percentage for Stocks
    monthly_data = get_monthly_data(stock_data, market_data)

    # Calculate monthly percentage change
    perc_change = calculate_net_perc_change(monthly_data)

    # Plot monthly percentage change
    plot_perc_change(perc_change)
