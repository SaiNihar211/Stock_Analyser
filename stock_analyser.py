import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


ticker_symbol = input("Enter Stock Ticker Symbol (e.g., TSLA, AAPL, MSFT): ").upper()


ticker = yf.Ticker(ticker_symbol)


stock = ticker.history(period="1y")

if stock.empty:
    print(" No data found for the entered ticker. Please check the symbol and try again!")
else:
    # Fetch and display company information
    company_info = ticker.info
    print("\n Company Details:")
    print(f"🔹 Name: {company_info.get('longName', 'N/A')}")
    print(f"🔹 Sector: {company_info.get('sector', 'N/A')}")
    print(f"🔹 Market Cap: {company_info.get('marketCap', 'N/A')}")

    #  Calculate daily returns and volatility
    stock['Daily_Return'] = stock['Close'].pct_change()
    stock.dropna(inplace=True)
    stock['Volatility'] = stock['Daily_Return'].rolling(window=20).std()

    # Fetch dividends & stock splits
    dividends = ticker.dividends
    splits = ticker.splits
    print("\n Dividends:\n", dividends.tail())
    print("\n Stock Splits:\n", splits.tail())

    print("\n Stock Data Preview:\n", stock.head())

    #  Plot closing price trend
    plt.figure(figsize=(12,6))
    plt.plot(stock['Close'], label=f"{ticker_symbol} Closing Price", color="blue")
    plt.title(f"{ticker_symbol} Stock Price Trend (Last 1 Year)")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.legend()
    plt.grid()
    plt.show()

    #  Calculate moving averages
    stock['50_MA'] = stock['Close'].rolling(window=50).mean()
    stock['200_MA'] = stock['Close'].rolling(window=200).mean()

    # Plot moving averages
    plt.figure(figsize=(12,6))
    plt.plot(stock['Close'], label="Closing Price", color="blue")
    plt.plot(stock['50_MA'], label="50-Day MA", color="red", linestyle="dashed")
    plt.plot(stock['200_MA'], label="200-Day MA", color="green", linestyle="dashed")
    plt.title(f"{ticker_symbol} Stock Price with Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid()
    plt.show()

    #  Plot volatility
    plt.figure(figsize=(12,6))
    plt.plot(stock.index, stock['Volatility'], label='20-day Volatility', color='red')
    plt.title(f"{ticker_symbol} Stock Volatility Over Time")
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.legend()
    plt.show()

    # Calculate RSI
    delta = stock['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    stock['RSI'] = 100 - (100 / (1 + rs))

    # Calculate Bollinger Bands
    stock['Middle_Band'] = stock['Close'].rolling(window=20).mean()
    std_dev = stock['Close'].rolling(window=20).std().squeeze()

    stock['Upper_Band'] = stock['Middle_Band'] + (std_dev * 2)
    stock['Lower_Band'] = stock['Middle_Band'] - (std_dev * 2)

    #  Candlestick chart with moving averages
    fig = go.Figure(data=[go.Candlestick(x=stock.index,
                                         open=stock['Open'],
                                         high=stock['High'],
                                         low=stock['Low'],
                                         close=stock['Close'],
                                         name="Stock Price")])

    fig.add_trace(go.Scatter(x=stock.index, y=stock['50_MA'], mode='lines', name='SMA 50', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=stock.index, y=stock['200_MA'], mode='lines', name='SMA 200', line=dict(color='red')))

    fig.update_layout(title=f"{ticker_symbol} Stock Candlestick Chart with Moving Averages",
                      xaxis_title="Date",
                      yaxis_title="Price",
                      template="plotly_dark")

    fig.show()
