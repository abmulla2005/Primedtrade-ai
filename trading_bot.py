
from binance.client import Client
from binance.enums import *
import logging
import os

# Create log directory
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/trading_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)

        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        try:
            self.client.ping()
            logging.info("Connected to Binance Testnet.")
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

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_STOP_MARKET,
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


def main():
    print("\n🚀 Binance Futures Trading Bot (Testnet) 🚀")
    api_key = input("🔑 Enter your Binance API Key: ").strip()
    api_secret = input("🔒 Enter your Binance API Secret: ").strip()

    bot = BasicBot(api_key, api_secret)

    while True:
        print("\nChoose an option:")
        print("1. Place Market Order")
        print("2. Place Limit Order")
        print("3. Place Stop-Limit Order")
        print("4. Exit")

        choice = input("👉 Enter choice (1/2/3/4): ").strip()

        if choice not in ['1', '2', '3', '4']:
            print("❌ Invalid choice. Try again.")
            continue

        if choice == '4':
            print("👋 Exiting bot. Goodbye!")
            break

        symbol = input("💱 Enter trading pair (e.g., BTCUSDT): ").strip().upper()
        side = input("📈 Side (BUY/SELL): ").strip().upper()
        quantity = float(input("🔢 Quantity: "))

        if choice == '1':
            result = bot.place_order(symbol, SIDE_BUY if side == "BUY" else SIDE_SELL, ORDER_TYPE_MARKET, quantity)

        elif choice == '2':
            price = input("💲 Enter Limit Price: ").strip()
            result = bot.place_order(symbol, SIDE_BUY if side == "BUY" else SIDE_SELL, ORDER_TYPE_LIMIT, quantity, price)

        elif choice == '3':
            stop_price = input("⛔ Stop Price: ").strip()
            limit_price = input("💲 Limit Price: ").strip()
            result = bot.place_stop_limit_order(symbol, SIDE_BUY if side == "BUY" else SIDE_SELL, quantity, stop_price, limit_price)

        print("📊 Order Result:", result)


if __name__ == "__main__":
    main()
