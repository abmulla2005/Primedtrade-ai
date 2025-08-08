
# !pip install python-binance

from binance.client import Client
from binance.enums import *
import logging
import time
import os

# Setup Logging
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename='logs/trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        try:
            self.client.ping()
            logging.info("Connected to Binance Testnet successfully.")
        except Exception as e:
            logging.error(f"Connection failed: {e}")
            raise

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == ORDER_TYPE_MARKET:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type == ORDER_TYPE_LIMIT:
                if price is None:
                    raise ValueError("Price must be specified for limit orders.")
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_LIMIT,
                    quantity=quantity,
                    price=price,
                    timeInForce=TIME_IN_FORCE_GTC
                )
            else:
                raise ValueError("Unsupported order type")

            logging.info(f"Order placed: {order}")
            return order
        except Exception as e:
            logging.error(f"Order failed: {e}")
            return None

    def stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_STOP,
                quantity=quantity,
                stopPrice=stop_price,
                price=limit_price,
                timeInForce=TIME_IN_FORCE_GTC
            )
            logging.info(f"Stop-Limit Order placed: {order}")
            return order
        except Exception as e:
            logging.error(f"Stop-Limit Order failed: {e}")
            return None


def get_user_input():
    print("\n--- Binance Futures Trading Bot ---")
    api_key = input("Enter your Binance Testnet API Key: ")
    api_secret = input("Enter your Binance Testnet API Secret: ")

    bot = BasicBot(api_key, api_secret)

    while True:
        print("\n1. Place Market Order\n2. Place Limit Order\n3. Place Stop-Limit Order\n4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            symbol = input("Symbol (e.g., BTCUSDT): ").upper()
            side = input("Side (BUY/SELL): ").upper()
            quantity = float(input("Quantity: "))
            result = bot.place_order(symbol, SIDE_BUY if side == "BUY" else SIDE_SELL, ORDER_TYPE_MARKET, quantity)
            print("Order Result:", result)

        elif choice == '2':
            symbol = input("Symbol (e.g., BTCUSDT): ").upper()
            side = input("Side (BUY/SELL): ").upper()
            quantity = float(input("Quantity: "))
            price = input("Limit Price: ")
            result = bot.place_order(symbol, SIDE_BUY if side == "BUY" else SIDE_SELL, ORDER_TYPE_LIMIT, quantity, price)
            print("Order Result:", result)

        elif choice == '3':
            symbol = input("Symbol (e.g., BTCUSDT): ").upper()
            side = input("Side (BUY/SELL): ").upper()
            quantity = float(input("Quantity: "))
            stop_price = input("Stop Price: ")
            limit_price = input("Limit Price: ")
            result = bot.stop_limit_order(symbol, SIDE_BUY if side == "BUY" else SIDE_SELL, quantity, stop_price, limit_price)
            print("Order Result:", result)

        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    get_user_input()

