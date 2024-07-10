from binance.client import Client
import pandas as pd
import mplfinance as mpf

# API key and secret (replace with your actual API key and secret)
api_key = 'your_api_key'
secret = 'your_secret_key'

# Initialize the Binance client
client = Client(api_key, secret)

# Function to fetch all tickers and convert to DataFrame
def get_tickers(client):
    tickers = client.get_all_tickers()
    ticker_df = pd.DataFrame(tickers)
    ticker_df.set_index('symbol', inplace=True)
    return ticker_df

# Function to fetch market depth and convert to DataFrame
def get_market_depth(client, symbol):
    depth = client.get_order_book(symbol=symbol)
    depth_df = pd.DataFrame(depth['bids'], columns=['price', 'quantity'])
    depth_df['price'] = depth_df['price'].astype(float)
    depth_df['quantity'] = depth_df['quantity'].astype(float)
    return depth_df

# Function to fetch historical data and convert to DataFrame
def get_historical_data(client, symbol, interval, start_date):
    historical = client.get_historical_klines(symbol, interval, start_date)
    hist_df = pd.DataFrame(historical, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_asset_volume', 'number_of_trades', 
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    hist_df['open_time'] = pd.to_datetime(hist_df['open_time'], unit='ms')
    hist_df.set_index('open_time', inplace=True)
    numeric_columns = ['open', 'high', 'low', 'close', 'volume']
    hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric)
    return hist_df

# Function to visualize historical data
def visualize_data(hist_df):
    mpf.plot(hist_df.tail(100), type='candle', style='charles', volume=True, 
             title='Bitcoin (BTC) Last 100 Days', mav=(10, 20, 30))

# Main function to link everything together
def main():
    # Fetch and display tickers
    tickers = get_tickers(client)
    print(tickers.loc['BTCUSDT'])

    # Fetch and display market depth for Bitcoin
    market_depth = get_market_depth(client, 'BTCUSDT')
    print(market_depth.head())

    # Fetch and display historical data for Bitcoin
    hist_data = get_historical_data(client, 'BTCUSDT', Client.KLINE_INTERVAL_1DAY, '1 Jan 2017')
    print(hist_data.head())

    # Visualize the historical data for Bitcoin
    visualize_data(hist_data)

# Run the main function
if __name__ == "__main__":
    main()
