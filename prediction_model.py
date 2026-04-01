from textblob import TextBlob
import urllib.request
import json
import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Get stock ticker from user
ticker = input("Enter stock ticker symbol: ")
print(f"Fetching 5 years of data for {ticker}...")

# Pull 5 years of data
stock = yf.Ticker(ticker)
df = stock.history(period="5y")

# Calculate features
df["Return"] = df["Close"].pct_change()
df["MA_50"] = df["Close"].rolling(window=50).mean()
df["MA_200"] = df["Close"].rolling(window=200).mean()
df["Volatility"] = df["Return"].rolling(window=20).std()


df["Return_2"] = df["Return"].shift(1)
df["Return_3"] = df["Return"].shift(2)
df["Volume_Change"] = df["Volume"].pct_change()
df["Momentum"] = df["Close"] - df["Close"].shift(10)

# Get news sentiment for the stock
def get_sentiment(ticker):
    try:
        url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(request, timeout=5)
        content = response.read().decode("utf-8")
        blob = TextBlob(content)
        return blob.sentiment.polarity
    except:
        return 0

print("Fetching news sentiment...")
sentiment = get_sentiment(ticker)
df["Sentiment"] = sentiment
print(f"Current news sentiment score: {sentiment:.4f}")


# Create target - 1 if price goes up tomorrow, 0 if it goes down
df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

# Drop rows with missing values
df = df.dropna()

print(f"Data prepared - {len(df)} trading days loaded")
print(df[["Close", "Return", "MA_50", "MA_200", "Volatility", "Target"]].tail())


# Define features and target
features = ["Return", "MA_50", "MA_200", "Volatility", "Return_2", "Return_3", "Volume_Change", "Momentum", "Sentiment"]
X = df[features]
y = df["Target"]

# Split data - 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

print(f"Training on {len(X_train)} days of data")
print(f"Testing on {len(X_test)} days of data")


# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test the model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Model Accuracy: {accuracy * 100:.2f}%")


# Predict today
latest = df[features].iloc[-1].values.reshape(1, -1)
prediction = model.predict(latest)

if prediction[0] == 1:
    print(f"Prediction for tomorrow: BUY")
else:
    print(f"Prediction for tomorrow: SELL")


# Chart - Actual vs Predicted
import matplotlib.pyplot as plt

test_dates = df.index[-len(X_test):]
actual = y_test.values
predicted = predictions

plt.figure(figsize=(14, 6))
plt.plot(test_dates, actual, label="Actual", color="blue", alpha=0.6)
plt.plot(test_dates, predicted, label="Predicted", color="orange", alpha=0.6)
plt.title(f"{ticker} - Actual vs Predicted Direction")
plt.xlabel("Date")
plt.ylabel("0 = Down, 1 = Up")
plt.legend()
plt.tight_layout()
plt.show()