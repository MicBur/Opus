import pandas as pd
import numpy as np
from modules.debug_logger import logger
from modules.security import security

# Check if we have ta-lib or similar. If not, implement basic indicators with pandas.
# I will implement basic indicators with pandas to be safe and avoid extra deps issues if `pandas_ta` isn't available.

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Better RSI calculation (Wilder's Smoothing) often used in crypto
    # But simple rolling mean is a start. Let's try to do it slightly better.
    # Actually, let's stick to standard Pandas implementation if possible.
    # A simple EMA based RSI is standard.

    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=period - 1, adjust=False).mean()
    ema_down = down.ewm(com=period - 1, adjust=False).mean()
    rs = ema_up / ema_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger_bands(series, period=20, std_dev=2):
    sma = series.rolling(window=period).mean()
    std = series.rolling(window=period).std()
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    return upper_band, lower_band

def calculate_atr(high, low, close, period=14):
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean() # Simple Moving Average of TR
    return atr

class Strategy:
    def __init__(self):
        self.rsi_threshold = security.get("rsi_entry_threshold", 30)
        self.vol_spike_threshold = security.get("volume_spike_threshold", 2.5)

    def analyze(self, ohlcv_data):
        """
        Analyzes OHLCV data and returns a signal.
        ohlcv_data: list of [timestamp, open, high, low, close, volume]
        """
        if not ohlcv_data or len(ohlcv_data) < 50:
            return {'action': 'hold', 'reason': 'insufficient_data'}

        df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        # Calculate Indicators
        df['rsi'] = calculate_rsi(df['close'])
        df['bb_upper'], df['bb_lower'] = calculate_bollinger_bands(df['close'])
        df['atr'] = calculate_atr(df['high'], df['low'], df['close'])

        # Volume Spike
        df['vol_ma'] = df['volume'].rolling(window=20).mean()
        df['vol_spike'] = df['volume'] / df['vol_ma']

        # Get latest candle (or previous closed candle)
        current = df.iloc[-1]

        # Logic from README
        # Entry: RSI < 45 (or config), Volume Spike > 2.5x, Price < BB Lower (Confirmation)

        rsi_condition = current['rsi'] < self.rsi_threshold
        bb_condition = current['close'] < current['bb_lower']
        vol_condition = current['vol_spike'] > self.vol_spike_threshold

        # We need a score or multiple filters
        score = 0
        reasons = []

        if rsi_condition:
            score += 1
            reasons.append("RSI Oversold")
        if bb_condition:
            score += 1
            reasons.append("Below BB Lower")
        if vol_condition:
            score += 1
            reasons.append("Volume Spike")

        min_filters = security.get("minimum_filters_required", 3)

        if score >= min_filters:
            logger.info(f"Entry Signal: {reasons}")
            return {
                'action': 'buy',
                'price': current['close'],
                'atr': current['atr'],
                'reasons': reasons
            }

        # Exit Logic (simplified check for now, usually handled by position manager)
        if current['rsi'] > 70:
             return {'action': 'sell', 'reason': 'RSI Overbought'}

        return {'action': 'hold', 'data': current.to_dict()}

strategy_engine = Strategy()
