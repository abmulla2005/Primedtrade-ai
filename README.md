# Binance Futures Trading Bot (Testnet)

A basic command-line trading bot for Binance Futures (Testnet), built with Python and the `python-binance` library.  
This bot allows you to place Market, Limit, and Stop-Limit orders interactively via the terminal.

## 🚀 Features

- Connects to Binance **Futures Testnet**
- Place **Market Orders**
- Place **Limit Orders**
- Place **Stop-Limit Orders**
- Logging to `logs/trading_bot.log`

## 📦 Requirements

- Python 3.7+
- `python-binance` library

## 🔧 Installation

1. Clone this repository or copy the code.
2. Install dependencies:

```bash
pip install python-binance
Run the bot:

bash
Copy
Edit
python trading_bot.py
Make sure you replace trading_bot.py with the actual filename.

🔑 Binance Testnet API Keys
To use this bot, you need Binance Futures Testnet API keys:

Sign up for the Testnet at: https://testnet.binancefuture.com/

Go to API Management to create a new API key

Enable Futures Trading

📄 How to Use
When you run the bot, it will prompt you to:

Enter your API Key and Secret

Choose an order type:

Market Order

Limit Order

Stop-Limit Order

Enter required order details

The bot will place the order and log the result
