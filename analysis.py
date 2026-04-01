import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


#user input for companies to analyze
companies = {}
print("Stock Market Analysis Tool")
print("-" * 30)
num = int(input("How many companies do you want to analyze? "))
for i in range(num):
    name = input(f"Enter company name {i+1}: ")
    ticker = input(f"Enter ticker symbol for {name}: ")
    companies[name] = ticker
print("-" * 30)
print("Fetching data and running analysis...")
print()

# pull data for each company, if you want to change the timeframe, change 1y to 3mo

for name, ticker in companies.items():
    stock = yf.Ticker(ticker)
    history = stock.history(period="1y")


    start_price = history["Close"].iloc[0]
    end_price = history["Close"].iloc[-1]
    annual_return = ((end_price - start_price) / start_price)*100
    volatility = history["Close"].pct_change().std() *100
    ma_50 = history["Close"].rolling(window=50).mean().iloc[-1]
    ma_200 = history["Close"].rolling(window=200).mean().iloc[-1]
    if end_price > ma_50 and end_price > ma_200:
        signal = "BUY"
    elif end_price < ma_50 and end_price < ma_200:
        signal = "SELL"
    else:
        signal = "HOLD"


    print(f"{name} ({ticker})")
    print(f" Start Price:   ${start_price:.2f}")
    print(f" End Price:    ${end_price:.2f}")
    print(f" Return: {annual_return:.2f}%")
    print(f" Volatility:   {volatility:.2f}%")
    print(f" 50 Day MA:   ${ma_50:.2f}")
    print(f" 200 Day MA:   ${ma_200:.2f}")
    print(f" Signal:   {signal}")
    print()


#chart 1, price trend with moving averages for each company
for name, ticker in companies.items():
    stock = yf.ticker.Ticker(ticker)
    history = stock.history(period="1y")

    ma_50 = history["Close"].rolling(window=50).mean()
    ma_200 = history["Close"].rolling(window=200).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(history.index, history["Close"], label ="Price", color="blue")
    plt.plot(history.index, ma_50, label="50 Day MA", color="orange")
    plt.plot(history.index, ma_200, label="200 Day MA", color="red")
    plt.title(f"{name} ({ticker}) - 1 Year Price Trend")
    plt.xlabel("Date")
    plt.xlabel("Price (USD)")
    plt.legend()
    plt.tight_layout()
    plt.show()

#chart 2, comparison bar chart of annual returns

names = list(companies.keys())
returns = []

for name, ticker in companies.items():
    stock = yf.Ticker(ticker)
    history = stock.history(period="1y")
    start_price = history["Close"].iloc[0]
    end_price = history["Close"].iloc[-1]
    annual_return = ((end_price - start_price) / start_price) * 100
    returns.append(annual_return)

colors = ["green" if r > 0 else "red" for r in returns]

plt.figure(figsize=(14, 7))
plt.bar(names, returns, color=colors)
plt.title("1 Year Annual Returns by Company")
plt.xlabel("Company")
plt.ylabel("Return (%)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# Excel Export
data = []

for name, ticker in companies.items():
    stock = yf.Ticker(ticker)
    history = stock.history(period="1y")
    
    start_price = history["Close"].iloc[0]
    end_price = history["Close"].iloc[-1]
    annual_return = ((end_price - start_price) / start_price) * 100
    volatility = history["Close"].pct_change().std() * 100
    ma_50 = history["Close"].rolling(window=50).mean().iloc[-1]
    ma_200 = history["Close"].rolling(window=200).mean().iloc[-1]
    
    if end_price > ma_50 and end_price > ma_200:
        signal = "BUY"
    elif end_price < ma_50 and end_price < ma_200:
        signal = "SELL"
    else:
        signal = "HOLD"
    
    data.append({
        "Company": name,
        "Ticker": ticker,
        "Start Price": round(start_price, 2),
        "End Price": round(end_price, 2),
        "Annual Return (%)": round(annual_return, 2),
        "Volatility (%)": round(volatility, 2),
        "50 Day MA": round(ma_50, 2),
        "200 Day MA": round(ma_200, 2),
        "Signal": signal
    })

df = pd.DataFrame(data)
df.to_excel("stock_analysis.xlsx", index=False)
print("Excel file saved to stock-analyzer folder")