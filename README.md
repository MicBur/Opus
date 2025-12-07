# 🚀 ATOMIC NECRO ENGINE 2025

**Autonomous Trading Bot mit 96+ Features**  
Cross-Exchange Arbitrage • RSI/BB/ATR Strategy • AI Learning • AES-256 Security

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Private-red.svg)]()
[![Status](https://img.shields.io/badge/Status-Production-green.svg)]()

---

## 📋 Inhaltsverzeichnis

- [Features](#-features)
- [Architektur](#-architektur)
- [Installation](#-installation)
- [Konfiguration](#-konfiguration)
- [Telegram Bot](#-telegram-bot)
- [Modi](#-modi)
- [Trading Strategie](#-trading-strategie)
- [Auto-Learning](#-auto-learning)
- [Sicherheit](#-sicherheit)
- [Performance](#-performance)

---

## ✨ Features

### 🎯 Core Trading (Features 5-22)
- **RSI Strategy**: RSI < 45 = Entry Signal, RSI > 70 = Exit
- **Bollinger Bands**: Preis < BB Lower = Kaufbestätigung
- **ATR-basiert**: Dynamische Take-Profit (1.8% - 18%)
- **Multi-Timeframe**: 1m für Entry, 5m für Trend
- **Position Sizing**: 2-8% pro Trade (dynamisch)
- **Max 8 Positionen**: Parallel trading
- **Volume Filter**: 2.5x Spike erforderlich
- **Stop Loss**: 1.5% Fixed + 0.8% Trailing
- **Safe Wallet**: 50% Gewinn automatisch gesichert
- **Daily Loss Limit**: -15% Max pro Tag

### 🤖 Telegram Bot (Features 31-35)
- `/start` - Starte Trading
- `/stop` - Stoppe Trading
- `/status` - Live Status (Balance, PnL, Positionen)
- `/stats` - Performance Statistiken
- `/tracker` - Coin Tracker Status
- `/accuracy` - Win Rate nach Coins
- `/simtrades` - Zeige Paper/Shadow Trades
- `/backtest` - Starte Backtest
- `/backtest_results` - Letzte Backtest-Ergebnisse
- `/panic` - Emergency Stop (alle Positionen schließen)
- `/safe` - Safe Wallet Balance
- `/agg <0-100>` - Aggressiveness einstellen
- `/livemode` - Aktiviere Live Trading
- Push-Benachrichtigungen für alle Events

### 🧠 AI Learning System (Features 50-83)
- **Autonomes Lernen**: Alle 24h automatische Optimierung
- **Performance Tracking**: Win Rate, Sharpe Ratio, PnL pro Coin
- **Dynamic Adjustment**:
  - Win Rate < 45% → Strategie verschärfen
  - Win Rate > 55% → Strategie lockern
- **Parameter Optimization**: RSI, Volume, Aggressiveness
- **Coin Rotation**: Schwache Coins raus, starke rein
- **Prime-Time Detection**: Beste Handelszeiten identifizieren
- **Risk Score**: Berechnung pro Coin
- **SQLite Logging**: Alle Trades persistent gespeichert

### 📊 Advanced Features (Features 60-96)
- **Flash Orders**: Minimale Slippage (0.55%)
- **Orderbook Imbalance**: Kaufdruck-Erkennung (>0.35)
- **Whale Alert**: Dump-Detection (>75k USDT)
- **Kalman Filter**: Multi-Timeframe Noise Reduction
- **Arbitrage Monitor**: Cross-Exchange (Binance, Bybit, Bitget)
- **Circuit Breaker**: -10% in 1h = Auto-Stop
- **Dynamic Hot List**: Top 25 Coins nach Volume & Volatility
- **Auto-Backtest**: Neue Coins automatisch testen
- **Coin Discovery**: Früherkennung profitabler Coins

### 🔒 Security (Features 40-45)
- **AES-256 Encryption**: API-Keys verschlüsselt
- **Master Password**: PBKDF2 Key-Derivation
- **Config Encryption**: Fernet-basiert
- **Self-Destruct**: Nach 3 Fehlversuchen
- **Salt-based**: Sichere Key-Generierung

### 🛡️ System (Features 38-39)
- **Auto-Restart**: Bei Crash automatisch neustarten
- **Watchdog**: System Monitoring (CPU, RAM, Disk)
- **systemd Service**: Permanent laufend
- **Log Rotation**: Automatische Log-Verwaltung

---

## 🏗️ Architektur

```
ATOMIC_NECRO_ENGINE_2025.py (Main)
│
├── modules/
│   ├── exchange.py           # Bitget API Integration
│   ├── strategy.py            # Trading Strategy (RSI/BB/ATR)
│   ├── learner.py             # AI Learning & Optimization
│   ├── telegram_bot.py        # Telegram Remote Control
│   ├── arbitrage.py           # Cross-Exchange Arbitrage
│   ├── coin_tracker.py        # Dynamic Coin Discovery
│   ├── backtester.py          # Strategy Backtesting
│   ├── kalman_filter.py       # Noise Reduction
│   ├── security.py            # Encryption & Security
│   ├── watchdog.py            # Auto-Restart & Monitoring
│   └── debug_logger.py        # Multi-Level Logging
│
├── db/
│   ├── learner.db             # Trade History & Learning
│   ├── coin_tracker.db        # Coin Performance & Backtest
│   └── atomic_necro.db        # Main Database
│
├── logs/                      # Rotated Logs
├── backtest_results/          # Backtest JSON Files
└── config.json                # Bot Configuration
```

---

## 🚀 Installation

### Voraussetzungen
- **Python 3.11+**
- **Raspberry Pi 3/4** oder Linux Server
- **8GB RAM** (minimum 4GB)
- **Internet-Verbindung**

### 1. Repository klonen
```bash
git clone https://github.com/GoldCash-Pool/Atomic-v2.0.git
cd Atomic-v2.0
```

### 2. Virtual Environment erstellen
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
.\venv\Scripts\Activate.ps1  # Windows
```

### 3. Dependencies installieren
```bash
pip install -r requirements.txt
```

### 4. Konfiguration erstellen
```bash
cp config.json.template config.json
nano config.json
```

Trage deine **Bitget API-Keys** und **Telegram Bot Token** ein:
```json
{
    "BITGET_API_KEY": "bg_xxx",
    "BITGET_API_SECRET": "xxx",
    "BITGET_PASSPHRASE": "xxx",
    "telegram_bot_token": "xxx",
    "telegram_chat_id": "xxx"
}
```

### 5. systemd Service einrichten (Linux)
```bash
sudo cp atomic-necro.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable atomic-necro
sudo systemctl start atomic-necro
```

### 6. Status prüfen
```bash
sudo systemctl status atomic-necro
journalctl -u atomic-necro -f
```

---

## ⚙️ Konfiguration

### Wichtige Parameter

```json
{
    "paper_mode": true,              // Virtuelles Geld
    "shadow_mode": true,             // Keine echten Orders
    "is_trading": false,             // Trading aktiv/inaktiv
    "aggressiveness": 90,            // 0-100 (Trading-Intensität)
    
    "volume_spike_threshold": 2.5,   // Volume Spike (2.5x)
    "rsi_entry_threshold": 30,       // RSI Entry Level
    "orderbook_imbalance_threshold": 0.35,  // Kaufdruck-Filter
    
    "minimum_filters_required": 3,   // Min. Filter für Entry
    "max_slippage_percent": 0.55,    // Max. Slippage
    "trade_cooldown_seconds": 300,   // Cooldown nach Trade
    
    "learning_interval_hours": 24,   // Auto-Optimization Interval
    "hot_list_size": 25,             // Trading Pairs
    "backtest_months": 6             // Backtest Zeitraum
}
```

---

## 📱 Telegram Bot

### Setup
1. Erstelle Bot bei [@BotFather](https://t.me/Botfather)
2. Hole Token: `/newbot`
3. Hole Chat-ID: Schreibe Bot, dann `/start`
4. Trage beides in `config.json` ein

### Commands

**Trading Control:**
- `/start` - Starte Trading Bot
- `/stop` - Stoppe Trading Bot
- `/panic` - Emergency Stop (alle Positionen)

**Status & Info:**
- `/status` - Balance, PnL, Positionen, Modus
- `/stats` - Performance Statistiken
- `/tracker` - Coin Tracker Übersicht
- `/accuracy` - Win Rate nach Symbols
- `/safe` - Safe Wallet Balance

**Backtesting:**
- `/backtest` - Starte Backtest für neue Coins
- `/backtest_results` - Zeige letzte Ergebnisse
- `/simtrades` - Paper/Shadow Trades der letzten 24h

**Settings:**
- `/agg 85` - Aggressiveness auf 85% setzen
- `/livemode` - Aktiviere Live Trading (Warnung!)
- `/help` - Zeige alle Commands

---

## 🎭 Modi

### 1. Paper Mode (`paper_mode: true`)
- Verwendet **virtuelles Geld**
- Keine Verbindung zur echten Balance
- Perfekt zum Testen der Strategie
- Lernt trotzdem und optimiert sich

### 2. Shadow Mode (`shadow_mode: true`)
- Beobachtet Markt
- Simuliert Trades im Hintergrund
- **Keine echten Orders**
- Sammelt Daten für Learning

### 3. Live Mode (`paper_mode: false, shadow_mode: false`)
- ⚠️ **ECHTES GELD!**
- Echte Orders auf Bitget
- Nur nach ausgiebigem Testing!
- **VORSICHT**: Verluste möglich

### Empfohlene Progression:
1. **Woche 1-2**: Paper + Shadow Mode (Strategie testen)
2. **Woche 3**: Nur Shadow Mode (Echte Balance sehen)
3. **Woche 4+**: Live Mode (mit kleinen Beträgen starten)

---

## 📈 Trading Strategie

### Entry Conditions (ALLE müssen erfüllt sein)
1. ✅ RSI < 45 (Oversold)
2. ✅ Volume Spike > 2.5x
3. ✅ Orderbook Imbalance > 0.35 (Kaufdruck)
4. ✅ Keine Whale Dumps (letzte 60s)
5. ✅ Multi-Timeframe Confirmation (5m)
6. ✅ Min. 3 Filter erfüllt

### Exit Conditions (eines reicht)
1. ❌ Take-Profit erreicht (1.8% - 18%, ATR-basiert)
2. ❌ Stop-Loss (-1.5%)
3. ❌ Trailing Stop (-0.8%)
4. ❌ RSI > 70 (Overbought)
5. ❌ Volume fällt < 80% Durchschnitt
6. ❌ Daily Loss Limit (-15%)

### Risk Management
- **Position Size**: 2-8% der Balance (dynamisch)
- **Max Positions**: 8 parallel
- **Max Daily Loss**: -15%
- **Safe Wallet**: 50% Gewinn automatisch gesichert
- **Circuit Breaker**: -10% in 1h = Auto-Stop

---

## 🧠 Auto-Learning

Der Bot optimiert sich **alle 24 Stunden** automatisch:

### Performance-basierte Anpassung

**Win Rate < 45% (Zu aggressiv):**
- RSI Threshold erhöhen (30 → 32 → 35)
- Volume Spike erhöhen (2.5x → 2.8x → 3.0x)
- Aggressiveness senken (90 → 85 → 80)

**Win Rate 45-55% (Optimal):**
- Feintuning von Stop-Loss
- Take-Profit Optimization
- Prime-Time Adjustment

**Win Rate > 55% (Zu konservativ):**
- RSI Threshold senken (30 → 28 → 25)
- Volume Spike senken (2.5x → 2.2x → 2.0x)
- Aggressiveness erhöhen (90 → 93 → 95)

### Was wird gelernt?
- ✅ Beste Coins (Performance Tracking)
- ✅ Beste Handelszeiten (Prime-Time Detection)
- ✅ Optimale Entry-Schwellen
- ✅ Risk-Scores pro Coin
- ✅ Portfolio Optimization

### Telegram Benachrichtigung
Alle 24h erhältst du eine Nachricht:
```
🤖 AUTO-OPTIMIERUNG (24h)

📊 Win Rate: 48.5%
📈 Trades analysiert: 87

🔧 Änderungen:
• RSI Entry: 30 → 32 (konservativer)
• Volume Spike: 2.5x → 2.8x
• Aggressiveness: 90 → 87
```

---

## 🔒 Sicherheit

### API-Keys verschlüsseln
```bash
python encrypt_config.py
# Erstellt config.enc mit AES-256 Encryption
```

### Master-Passwort setzen
```python
# Beim ersten Start
Passwort eingeben: ********
# PBKDF2 mit 100.000 Iterationen
```

### Selbstzerstörung
Nach **3 Fehlversuchen** werden alle Daten gelöscht:
- ❌ config.json
- ❌ config.enc
- ❌ API-Keys
- ❌ Databases

### Best Practices
1. ✅ Nutze **Read-Only API-Keys** für Testing
2. ✅ Aktiviere **IP-Whitelist** auf Bitget
3. ✅ Nutze **2FA** auf Exchange
4. ✅ Starte mit **Paper Mode**
5. ✅ Regelmäßige **Backups** der DB

---

## 📊 Performance

### Raspberry Pi 3 Limits
- **Max 8 Trading Pairs**: Mehr überfordert den Pi
- **WebSocket**: Stabile Verbindung erforderlich
- **Startup Time**: ~20 Sekunden
- **RAM Usage**: ~300-500 MB
- **CPU**: 20-40% durchschnittlich

### Optimierungen
- ✅ Kalman Filter für Noise Reduction
- ✅ Caching für Ticker-Daten (5s)
- ✅ Async I/O für alle API-Calls
- ✅ SQLite für persistente Daten
- ✅ Log Rotation (max 10 MB)

### Monitoring
```bash
# CPU & RAM
htop

# Bot Logs
journalctl -u atomic-necro -f

# Fehler suchen
journalctl -u atomic-necro | grep -i error

# Performance Stats
python show_stats.py
```

---

## 🐛 Troubleshooting

### Bot startet nicht
```bash
# Service Status
sudo systemctl status atomic-necro

# Logs prüfen
journalctl -u atomic-necro -n 50

# Python Path prüfen
which python3
```

### Telegram antwortet nicht
```bash
# Telegram Logs
journalctl -u atomic-necro | grep TELEGRAM

# Chat-ID prüfen
# Schreibe Bot "/start" und prüfe Log:
# "Received /start from chat_id: 123456789"
```

### WebSocket Probleme
```bash
# Reduziere Trading Pairs in config.json
"hot_list_size": 8  # Statt 25 für Pi3
```

### Keine Trades
```bash
# Entry-Bedingungen zu streng?
# Lockere in config.json:
"volume_spike_threshold": 2.0,  # Statt 2.5
"minimum_filters_required": 3   # Statt 4
```

---

## 📜 Changelog

### v2.0.0 (Dezember 2025)
- ✅ 96 Features implementiert
- ✅ Safe Wallet System (50% Gewinn gesichert)
- ✅ 24h Auto-Learning
- ✅ Optimierte Entry-Schwellen
- ✅ Telegram Debug-Logging für alle Commands
- ✅ Backtester Bug-Fixes
- ✅ Coin Tracker Top 5 Performance
- ✅ Paper + Shadow Mode
- ✅ Raspberry Pi 3 kompatibel

---

## 📝 License

**Private Project** - All Rights Reserved

---

## 🙏 Credits

Developed by **GoldCash-Pool**  
Python 3.13.5 • python-telegram-bot 21.6 • ccxt 4.4+

---

## ⚠️ Disclaimer

**Crypto Trading ist riskant!**

- ❌ Keine Garantie für Gewinne
- ❌ Verluste sind möglich
- ❌ Nur investieren was du verlieren kannst
- ✅ Starte mit Paper Mode
- ✅ Teste ausgiebig
- ✅ Verstehe die Strategie

**Der Bot ist ein Tool - keine Gelddruckmaschine!**

---

**Happy Trading! 🚀💰**
