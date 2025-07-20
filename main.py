import yfinance as yf
import pandas as pd
import numpy_financial as npf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def fetch_data(ticker, currency_pair, years=5):
    """
    Fetches the last n years of historical data for a stock ticker and a currency pair.

    Args:
        ticker (str): The stock ticker symbol.
        currency_pair (str): The currency pair for conversion (e.g., 'EURUSD=X').
        years (int): The number of years of historical data to fetch.

    Returns:
        pandas.DataFrame: A DataFrame with the historical data for the stock and currency.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)

    stock_data = yf.Ticker(ticker).history(start=start_date, end=end_date)
    currency_data = yf.Ticker(currency_pair).history(start=start_date, end=end_date)

    return stock_data, currency_data

def process_data(stock_data, currency_data):
    """
    Processes the raw stock and currency data, converting the stock price to the target currency.

    Args:
        stock_data (pandas.DataFrame): The historical stock data.
        currency_data (pandas.DataFrame): The historical currency data.

    Returns:
        pandas.DataFrame: A DataFrame with the converted stock prices.
    """
    stock_data.index = stock_data.index.tz_localize(None)
    currency_data.index = currency_data.index.tz_localize(None)

    combined_data = pd.merge(stock_data['Close'], currency_data['Close'], left_index=True, right_index=True, how='inner')
    combined_data.rename(columns={'Close_x': 'Stock_USD', 'Close_y': 'Currency_Rate'}, inplace=True)

    combined_data['Stock_EUR'] = combined_data['Stock_USD'] / combined_data['Currency_Rate']

    return combined_data

def calculate_irr(data):
    """
    Calculates the Internal Rate of Return (IRR) of the investment.

    Args:
        data (pandas.DataFrame): The DataFrame with the converted stock prices.

    Returns:
        float: The calculated IRR.
    """
    cash_flows = [-data['Stock_EUR'].iloc[0]] + [0] * (len(data) - 2) + [data['Stock_EUR'].iloc[-1]]
    irr = npf.irr(cash_flows)
    return irr

def plot_data(data, ticker):
    """
    Plots the stock price in the target currency and saves the graph to a file.

    Args:
        data (pandas.DataFrame): The DataFrame with the converted stock prices.
        ticker (str): The stock ticker symbol.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['Stock_EUR'])
    plt.title(f'{ticker} Price in EUR (Last 5 Years)')
    plt.xlabel('Date')
    plt.ylabel('Price (EUR)')
    plt.grid(True)
    plt.savefig(f'{ticker.lower()}_eur_price.png')
    print(f"\nGraph saved to {ticker.lower()}_eur_price.png")

def main():
    """
    Main function to run the application.
    """
    ticker = "VYMI"
    currency_pair = "EURUSD=X"
    years = 5

    stock_data, currency_data = fetch_data(ticker, currency_pair, years)
    processed_data = process_data(stock_data, currency_data)
    irr = calculate_irr(processed_data)

    print(f"5-Year IRR for {ticker} in EUR: {irr:.2%}")

    plot_data(processed_data, ticker)

if __name__ == "__main__":
    main()
