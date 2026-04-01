# Stock Market Analysis Tool

A Python tool that pulls live stock data for any publicly traded company and 
performs financial analysis to help evaluate investment decisions.

## What it does
- Accepts any number of companies and ticker symbols as user input
- Pulls 1 year of live stock data using the Yahoo Finance API
- Calculates annual returns, daily volatility, and 50/200 day moving averages
- Generates automated buy, sell, or hold signals based on technical analysis
- Produces price trend charts for each company with moving average overlays
- Ranks all companies by annual return in a comparison bar chart
- Exports all metrics to a formatted Excel spreadsheet

## Tools Used
Python, pandas, yfinance, matplotlib, openpyxl

## How to Run
1. Install dependencies: pip install yfinance pandas matplotlib openpyxl
2. Run the script: python3 analysis.py


## Project 2 - Stock Price Prediction Model

A machine learning model that predicts whether a stock's price will go 
up or down the next trading day.

### What it does
- Pulls 5 years of historical data for any stock ticker
- Engineers 8 features including returns, moving averages, volatility, 
  momentum, and news sentiment
- Trains a Random Forest Classifier on 80% of the data
- Tests accuracy on the remaining 20%
- Predicts tomorrow's price direction
- Visualizes actual vs predicted direction over the test period
- Discovered ~50% accuracy, validating the Efficient Market Hypothesis

### Tools Used
Python, pandas, yfinance, scikit-learn, matplotlib, textblob