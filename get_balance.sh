#!/bin/bash

# Extract balance from the latest log line
BALANCE_FILE="/tmp/youtube_stream/balance.txt"
LOG_FILE="$HOME/.openclaw/workspace/kraken_bot/bot.log"

# Get latest balance from log
LATEST_LINE=$(tail -1 "$LOG_FILE" 2>/dev/null)
EUR_BALANCE=$(echo "$LATEST_LINE" | grep -oP 'Bal:\s*\K[0-9.]+(?=EUR)' || echo "0.00")

# Try to get token balances from kraken bot
cd "$HOME/.openclaw/workspace/kraken_bot" 2>/dev/null
if [ -f "kraken_interface.py" ]; then
    # Get balances using Python
    BALANCES=$(python3 << 'EOF' 2>/dev/null
import sys
sys.path.insert(0, '.')
try:
    from kraken_interface import KrakenAPI
    api = KrakenAPI()
    balance = api.get_account_balance()
    if balance:
        print(f"EUR: {float(balance.get('ZEUR', 0)):.2f}")
        print(f"BTC: {float(balance.get('XXBT', 0)):.6f}")
        print(f"ETH: {float(balance.get('XETH', 0)):.4f}")
        print(f"SOL: {float(balance.get('SOL', 0)):.2f}")
        print(f"ADA: {float(balance.get('ADA', 0)):.1f}")
        print(f"DOT: {float(balance.get('DOT', 0)):.2f}")
except:
    pass
EOF
)
    if [ ! -z "$BALANCES" ]; then
        echo "$BALANCES" > "$BALANCE_FILE"
    else
        # Fallback to log balance
        echo "EUR: $EUR_BALANCE" > "$BALANCE_FILE"
    fi
else
    # Fallback to log balance
    echo "EUR: $EUR_BALANCE" > "$BALANCE_FILE"
fi
