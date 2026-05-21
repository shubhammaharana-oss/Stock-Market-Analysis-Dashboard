import requests
import pandas as pd
API_KEY = "KW3ZII7QRH1ZA3WN"
symbol = "IBM"
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=compact&apikey={API_KEY}"
response = requests.get(url)
data = response.json()
if "Time Series (Daily)" not in data:
    print("Error:", data)
else:
    time_series = data["Time Series (Daily)"]

    df = pd.DataFrame.from_dict(time_series, orient='index')

    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Date'}, inplace=True)

    df.rename(columns={
        '1. open': 'Open',
        '2. high': 'High',
        '3. low': 'Low',
        '4. close': 'Close',
        '5. volume': 'Volume'
    }, inplace=True)

    df['Date'] = pd.to_datetime(df['Date'])
    df[['Open','High','Low','Close','Volume']] = df[['Open','High','Low','Close','Volume']].astype(float)

    df = df.sort_values('Date')

    print(df.head())
    print(data)
    from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:shubham@localhost/STOCK_DB")

df['MA_20'] = df['Close'].rolling(20).mean()
df['Daily Return'] = df['Close'].pct_change()

df.to_sql("stock_data", engine, if_exists="replace", index=False)

print("Data stored successfully!")