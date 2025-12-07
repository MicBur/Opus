import sqlite3
import os
from modules.debug_logger import logger

class Database:
    def __init__(self, db_path="db/atomic_necro.db"):
        self.db_path = db_path
        self.ensure_db_dir()
        self.init_db()

    def ensure_db_dir(self):
        directory = os.path.dirname(self.db_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Trades Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    side TEXT NOT NULL,
                    amount REAL,
                    entry_price REAL,
                    exit_price REAL,
                    pnl REAL,
                    pnl_percent REAL,
                    timestamp REAL,
                    mode TEXT
                )
            ''')

            # Learning Logs Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    win_rate REAL,
                    total_trades INTEGER,
                    changes TEXT
                )
            ''')

            conn.commit()
            conn.close()
            logger.info("Database initialized successfully.")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")

    def log_trade(self, trade_data):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO trades (symbol, side, amount, entry_price, exit_price, pnl, pnl_percent, timestamp, mode)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                trade_data['symbol'],
                trade_data['side'],
                trade_data['amount'],
                trade_data['entry_price'],
                trade_data['price'], # exit_price
                trade_data['pnl'],
                trade_data['pnl_percent'],
                trade_data['timestamp'],
                trade_data.get('mode', 'paper')
            ))
            conn.commit()
            conn.close()
            logger.debug(f"Trade logged to DB: {trade_data['symbol']}")
        except Exception as e:
            logger.error(f"Failed to log trade: {e}")

    def get_trades_since(self, timestamp):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM trades WHERE timestamp > ?', (timestamp,))
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            conn.close()

            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            logger.error(f"Failed to fetch trades: {e}")
            return []

    def log_learning(self, timestamp, win_rate, total_trades, changes):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO learning_logs (timestamp, win_rate, total_trades, changes)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, win_rate, total_trades, str(changes)))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to log learning event: {e}")

# Global instance
db = Database()
