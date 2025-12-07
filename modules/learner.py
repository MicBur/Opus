import time
from modules.debug_logger import logger
from modules.database import db
from modules.security import security

class Learner:
    def __init__(self):
        logger.info("AI Learner Module Initialized")
        self.interval_hours = security.get("learning_interval_hours", 24)
        self.last_run = 0

    def should_run(self):
        # Allow running if 24h passed since last run
        current_time = time.time()
        if current_time - self.last_run > (self.interval_hours * 3600):
            return True
        return False

    def optimize(self):
        logger.info("🤖 AUTO-OPTIMIERUNG: Analysing Performance...")
        current_time = time.time()

        # Get trades from last 24h (or interval)
        lookback = current_time - (self.interval_hours * 3600)
        trades = db.get_trades_since(lookback)

        if not trades:
            logger.info("No trades in the last 24h. Skipping optimization.")
            self.last_run = current_time
            return

        # Calculate Win Rate
        wins = [t for t in trades if t['pnl'] > 0]
        total = len(trades)
        win_rate = (len(wins) / total) * 100

        logger.info(f"📊 Win Rate: {win_rate:.2f}% ({len(wins)}/{total})")

        changes = []

        # Logic from README
        # Win Rate < 45% (Too aggressive) -> Tighten strategy
        if win_rate < 45:
            logger.info("Win Rate too low (<45%). Tightening strategy.")

            # RSI: Increase (e.g., 30 -> 32)
            current_rsi = security.get("rsi_entry_threshold", 30)
            new_rsi = min(current_rsi + 2, 40) # Cap at 40
            security.update_config("rsi_entry_threshold", new_rsi)
            changes.append(f"RSI: {current_rsi} -> {new_rsi}")

            # Volume: Increase (e.g., 2.5 -> 2.8)
            current_vol = security.get("volume_spike_threshold", 2.5)
            new_vol = round(current_vol + 0.3, 1)
            security.update_config("volume_spike_threshold", new_vol)
            changes.append(f"Volume: {current_vol}x -> {new_vol}x")

            # Aggressiveness: Decrease (e.g., 90 -> 85)
            current_agg = security.get("aggressiveness", 90)
            new_agg = max(current_agg - 5, 50)
            security.update_config("aggressiveness", new_agg)
            changes.append(f"Aggressiveness: {current_agg} -> {new_agg}")

        # Win Rate > 55% (Too conservative) -> Loosen strategy
        elif win_rate > 55:
            logger.info("Win Rate high (>55%). Loosening strategy.")

            # RSI: Decrease (e.g., 30 -> 28)
            current_rsi = security.get("rsi_entry_threshold", 30)
            new_rsi = max(current_rsi - 2, 20)
            security.update_config("rsi_entry_threshold", new_rsi)
            changes.append(f"RSI: {current_rsi} -> {new_rsi}")

            # Volume: Decrease (e.g., 2.5 -> 2.2)
            current_vol = security.get("volume_spike_threshold", 2.5)
            new_vol = round(max(current_vol - 0.3, 1.5), 1)
            security.update_config("volume_spike_threshold", new_vol)
            changes.append(f"Volume: {current_vol}x -> {new_vol}x")

            # Aggressiveness: Increase
            current_agg = security.get("aggressiveness", 90)
            new_agg = min(current_agg + 5, 100)
            security.update_config("aggressiveness", new_agg)
            changes.append(f"Aggressiveness: {current_agg} -> {new_agg}")

        else:
            logger.info("Win Rate optimal (45-55%). No major changes.")
            changes.append("None (Optimal)")

        # Log to DB
        db.log_learning(current_time, win_rate, total, changes)
        self.last_run = current_time

        if changes and changes[0] != "None (Optimal)":
             logger.info(f"🔧 Optimization Applied: {', '.join(changes)}")

# Global instance
learner = Learner()
