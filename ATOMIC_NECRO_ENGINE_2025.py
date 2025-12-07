import time
import asyncio
import signal
import sys
from modules.debug_logger import logger
from modules.security import security
from modules.exchange import exchange_client
from modules.strategy import strategy_engine
from modules.learner import learner
# from modules.telegram_bot import telegram_bot # Will implement later

class AtomicNecroEngine:
    def __init__(self):
        self.running = True
        self.trading_pairs = ["BTC/USDT", "ETH/USDT", "XRP/USDT", "SOL/USDT"] # Start small
        if security.get("hot_list_size") > 0:
             # Ideally fetch hot list dynamically
             pass
        self.sleep_interval = 60 # 1 minute loop

    async def start(self):
        logger.info("Atomic Necro Engine 2025 STARTED")
        logger.info(f"Mode: {'PAPER' if security.get('paper_mode') else 'LIVE'}")

        # Main Loop
        while self.running:
            try:
                await self.run_cycle()
                await asyncio.sleep(self.sleep_interval)
            except KeyboardInterrupt:
                self.stop()
            except Exception as e:
                logger.error(f"Main Loop Error: {e}")
                await asyncio.sleep(10)

    async def run_cycle(self):
        logger.info("--- Starting Trading Cycle ---")

        # 1. Update Market Data & Analyze
        for symbol in self.trading_pairs:
            await self.process_symbol(symbol)

        # 2. Portfolio Management (Check exits)
        await self.manage_positions()

        # 3. Learning (Check if 24h passed)
        if learner.should_run():
            learner.optimize()

    async def process_symbol(self, symbol):
        # Fetch Data
        ohlcv = exchange_client.fetch_ohlcv(symbol, timeframe='5m', limit=100)
        if not ohlcv:
            return

        # Run Strategy
        signal = strategy_engine.analyze(ohlcv)

        # Execute
        if signal['action'] == 'buy':
            logger.info(f"BUY SIGNAL for {symbol}: {signal['reasons']}")

            # Check if we already have a position
            positions = exchange_client.get_positions()
            if symbol in positions:
                logger.info(f"Skipping BUY: Position already exists for {symbol}")
                return

            # Calculate Position Size (e.g., 5% of balance)
            balance = exchange_client.get_balance().get('USDT', 0)
            amount_usdt = balance * 0.05
            price = signal['price']
            amount_coin = amount_usdt / price

            exchange_client.create_market_buy_order(symbol, amount_coin)

    async def manage_positions(self):
        positions = exchange_client.get_positions()
        if not positions:
            return

        for symbol, pos in list(positions.items()): # Create copy to modify during iteration
            # Check Exit Conditions
            ohlcv = exchange_client.fetch_ohlcv(symbol, timeframe='5m', limit=50)
            if not ohlcv: continue

            current_price = ohlcv[-1][4] # Close price
            entry_price = pos['entry_price']

            # PnL
            pnl_pct = ((current_price - entry_price) / entry_price) * 100

            exit_reason = None

            # Stop Loss (Fixed 1.5%)
            if pnl_pct <= -1.5:
                exit_reason = "Stop Loss (-1.5%)"

            # Take Profit (Simple 2% for now, or Strategy signal)
            elif pnl_pct >= 2.0:
                 exit_reason = "Take Profit (+2.0%)"

            # Strategy Exit (RSI > 70)
            else:
                 signal = strategy_engine.analyze(ohlcv)
                 if signal['action'] == 'sell':
                     exit_reason = signal['reason']

            if exit_reason:
                logger.info(f"Exiting {symbol}: {exit_reason} (PnL: {pnl_pct:.2f}%)")
                exchange_client.create_market_sell_order(symbol)

    def stop(self):
        self.running = False
        logger.info("Stopping Engine...")

if __name__ == "__main__":
    engine = AtomicNecroEngine()
    try:
        asyncio.run(engine.start())
    except KeyboardInterrupt:
        pass
