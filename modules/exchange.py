import ccxt
import time
from modules.debug_logger import logger
from modules.security import security
from modules.database import db

class PaperWallet:
    def __init__(self, initial_balance=10000):
        self.balance = {"USDT": initial_balance}
        self.positions = {}  # {symbol: {'amount': float, 'entry_price': float, 'side': 'buy'}}
        self.trades = []

    def get_balance(self, currency="USDT"):
        return self.balance.get(currency, 0.0)

    def update_balance(self, amount, currency="USDT"):
        self.balance[currency] = self.balance.get(currency, 0.0) + amount

    def open_position(self, symbol, side, amount, price):
        cost = amount * price
        if self.balance["USDT"] < cost:
            logger.warning("Paper Wallet: Insufficient funds.")
            return False

        self.balance["USDT"] -= cost
        if symbol not in self.positions:
            self.positions[symbol] = {'amount': 0.0, 'entry_price': 0.0, 'side': side}

        # Weighted average entry price
        current_amount = self.positions[symbol]['amount']
        current_entry = self.positions[symbol]['entry_price']
        total_amount = current_amount + amount
        if total_amount > 0:
            new_entry = ((current_amount * current_entry) + (amount * price)) / total_amount
            self.positions[symbol]['entry_price'] = new_entry
            self.positions[symbol]['amount'] = total_amount

        self.trades.append({
            'symbol': symbol, 'side': side, 'amount': amount, 'price': price, 'timestamp': time.time(), 'type': 'open'
        })
        logger.info(f"Paper Trade OPEN: {side} {amount} {symbol} @ {price}")
        return True

    def close_position(self, symbol, price):
        if symbol not in self.positions or self.positions[symbol]['amount'] <= 0:
            logger.warning(f"Paper Wallet: No position to close for {symbol}")
            return False

        pos = self.positions[symbol]
        amount = pos['amount']
        revenue = amount * price

        # Calculate PnL
        cost = amount * pos['entry_price']
        pnl = revenue - cost
        pnl_percent = (pnl / cost) * 100

        self.balance["USDT"] += revenue

        trade_record = {
            'symbol': symbol, 'side': 'sell' if pos['side'] == 'buy' else 'buy',
            'amount': amount, 'entry_price': pos['entry_price'], 'price': price, 'timestamp': time.time(),
            'type': 'close', 'pnl': pnl, 'pnl_percent': pnl_percent, 'mode': 'paper'
        }
        self.trades.append(trade_record)

        # Log to DB
        db.log_trade(trade_record)

        del self.positions[symbol]
        logger.info(f"Paper Trade CLOSE: {symbol} @ {price}. PnL: {pnl:.2f} USDT ({pnl_percent:.2f}%)")
        return trade_record

class BitgetExchange:
    def __init__(self):
        self.api_key = security.get("BITGET_API_KEY")
        self.secret = security.get("BITGET_API_SECRET")
        self.password = security.get("BITGET_PASSPHRASE")
        self.paper_mode = security.get("paper_mode", True)

        # Initialize CCXT
        self.exchange = ccxt.bitget({
            'apiKey': self.api_key,
            'secret': self.secret,
            'password': self.password,
            'enableRateLimit': True,
        })

        # Paper Wallet
        self.paper_wallet = PaperWallet()

        if self.paper_mode:
            logger.info("Exchange initialized in PAPER MODE")
        else:
            logger.warning("Exchange initialized in LIVE MODE - REAL MONEY AT RISK")

    def fetch_ohlcv(self, symbol, timeframe='5m', limit=100):
        try:
            return self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        except Exception as e:
            logger.error(f"Error fetching OHLCV for {symbol}: {e}")
            return []

    def fetch_ticker(self, symbol):
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol}: {e}")
            return None

    def get_current_price(self, symbol):
        ticker = self.fetch_ticker(symbol)
        if ticker:
            return ticker['last']
        return None

    def create_market_buy_order(self, symbol, amount):
        price = self.get_current_price(symbol)
        if not price:
            return None

        if self.paper_mode:
            if self.paper_wallet.open_position(symbol, 'buy', amount, price):
                return {'id': 'paper_' + str(int(time.time())), 'price': price, 'amount': amount, 'status': 'closed'}
            return None
        else:
            try:
                # Actual API call (Be careful!)
                # return self.exchange.create_market_buy_order(symbol, amount)
                logger.error("Live trading not fully implemented for safety.")
                return None
            except Exception as e:
                logger.error(f"Order failed: {e}")
                return None

    def create_market_sell_order(self, symbol, amount=None):
        # In this simplified version, we just close the full position
        price = self.get_current_price(symbol)
        if not price:
            return None

        if self.paper_mode:
            return self.paper_wallet.close_position(symbol, price)
        else:
            logger.error("Live trading not fully implemented for safety.")
            return None

    def get_balance(self):
        if self.paper_mode:
            return self.paper_wallet.balance
        else:
            try:
                return self.exchange.fetch_balance()
            except Exception as e:
                logger.error(f"Error fetching balance: {e}")
                return {}

    def get_positions(self):
        if self.paper_mode:
            return self.paper_wallet.positions
        else:
            # Implement fetching live positions
            return []

exchange_client = BitgetExchange()
