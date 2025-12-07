from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from modules.debug_logger import logger
from modules.security import security
from modules.exchange import exchange_client
import asyncio
import threading

class TelegramBot:
    def __init__(self):
        self.token = security.get("telegram_bot_token")
        self.chat_id = security.get("telegram_chat_id")
        self.app = None

        if self.token == "YOUR_BOT_TOKEN":
            logger.warning("Telegram Bot Token not set. Bot will not start.")
            return

        self.app = ApplicationBuilder().token(self.token).build()
        self.register_handlers()

    def register_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("balance", self.balance_command))
        self.app.add_handler(CommandHandler("panic", self.panic_command))
        self.app.add_handler(CommandHandler("help", self.help_command))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🚀 Atomic Necro Engine is running!")

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        positions = exchange_client.get_positions()
        msg = f"📊 Status Report\n\nActive Positions: {len(positions)}\n"
        for sym, pos in positions.items():
            msg += f"- {sym}: {pos['amount']:.4f} @ {pos['entry_price']:.2f}\n"
        await update.message.reply_text(msg)

    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        balance = exchange_client.get_balance()
        usdt = balance.get('USDT', 0)
        await update.message.reply_text(f"💰 Balance: {usdt:.2f} USDT")

    async def panic_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("⚠️ PANIC MODE ACTIVATED! Closing all positions...")
        positions = exchange_client.get_positions()
        for sym in list(positions.keys()):
             exchange_client.create_market_sell_order(sym)
        await update.message.reply_text("✅ All positions closed.")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "/start - Start Bot\n/status - Show Status\n/balance - Show Balance\n/panic - Close All"
        )

    def run(self):
        if self.app:
            logger.info("Starting Telegram Bot Polling...")
            self.app.run_polling()

# Wrapper to run in a separate thread if needed, or main loop can import it.
# For now, this is a standalone module that can be integrated.
