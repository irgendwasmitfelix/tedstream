#!/usr/bin/env python3
import sys
import krakenex
sys.path.insert(0, '/home/felix/tradingbot')
import os
from dotenv import load_dotenv

# Load environment
load_dotenv('/home/felix/tradingbot/.env')
api_key = os.getenv('KRAKEN_API_KEY')
api_secret = os.getenv('KRAKEN_API_SECRET')

# Single direct attempt — no retry/backoff (script is called on a schedule anyway)
try:
    api = krakenex.API(api_key, api_secret)
    response = api.query_private('Balance')
    errors = response.get('error', [])
    if errors:
        print(f"API Error: {errors}", file=sys.stderr)
        sys.exit(1)
    balance = response.get('result', {})

    # Get equity including open margin positions (unrealized PnL only, not margin collateral)
    try:
        tb = api.query_private('TradeBalance')
        tb_result = tb.get('result', {})
        unrealized_pnl = float(tb_result.get('n', 0))  # n = unrealized net P&L on open positions
    except Exception:
        unrealized_pnl = 0.0

    # Get EUR balance
    eur = float(balance.get('ZEUR', 0))
    total_value_eur = eur
    
    # Get current prices for each pair
    pairs_to_check = {
        'XXBT': 'XXBTZEUR',  # BTC pair name is different!
        'XETH': 'ETHEUR', 
        'SOL': 'SOLEUR',
        'ADA': 'ADAEUR',
        'DOT': 'DOTEUR',
        'XXRP': 'XRPEUR',
        'LINK': 'LINKEUR'
    }
    
    prices = {}
    for asset, pair in pairs_to_check.items():
        try:
            data = api.query_public('Ticker', {'pair': pair})
            result = data.get('result', {})
            for key in result.keys():
                if 'c' in result[key]:
                    prices[asset] = float(result[key]['c'][0])
                    break
        except Exception:
            prices[asset] = 0
    
    print(f"EUR: {eur:.2f}")
    
    # Check each crypto and calculate EUR value (High precision for Open Positions)
    btc = float(balance.get('XXBT', 0))
    btc_value = btc * prices.get('XXBT', 0)
    total_value_eur += btc_value
    print(f"BTC: {btc:.8f} - {btc_value:.2f}EUR")

    eth = float(balance.get('XETH', 0))
    eth_value = eth * prices.get('XETH', 0)
    total_value_eur += eth_value
    print(f"ETH: {eth:.8f} - {eth_value:.2f}EUR")

    sol = float(balance.get('SOL', 0))
    sol_value = sol * prices.get('SOL', 0)
    total_value_eur += sol_value
    print(f"SOL: {sol:.8f} - {sol_value:.2f}EUR")

    ada = float(balance.get('ADA', 0))
    ada_value = ada * prices.get('ADA', 0)
    total_value_eur += ada_value
    print(f"ADA: {ada:.8f} - {ada_value:.2f}EUR")

    dot = float(balance.get('DOT', 0))
    dot_value = dot * prices.get('DOT', 0)
    total_value_eur += dot_value
    print(f"DOT: {dot:.8f} - {dot_value:.2f}EUR")

    xrp = float(balance.get('XXRP', 0))
    xrp_value = xrp * prices.get('XXRP', 0)
    total_value_eur += xrp_value
    print(f"XRP: {xrp:.8f} - {xrp_value:.2f}EUR")

    link = float(balance.get('LINK', 0))
    link_value = link * prices.get('LINK', 0)
    total_value_eur += link_value
    print(f"LINK: {link:.8f} - {link_value:.2f}EUR")
        
    print("")
    # Total = spot EUR + unrealized P&L from open margin positions
    total_display = total_value_eur + unrealized_pnl
    print(f"TOTAL: {total_display:.2f} EUR")

    # Open margin positions (SHORT/LONG) — not reflected in spot balance
    try:
        import time; time.sleep(0.5)
        op = api.query_private('OpenPositions')
        positions = op.get('result', {})
        if positions:
            print("")
            for pos_id, p in positions.items():
                raw_pair = p.get('pair', '')
                # Clean pair name for display: XXBTZEUR→BTC, XETHZEUR→ETH, SOLEUR→SOL etc.
                display = raw_pair.replace('XXBT', 'BTC').replace('XETH', 'ETH').replace('XXRP', 'XRP').replace('ZEUR', '').replace('EUR', '')
                direction = 'LONG' if p.get('type') == 'buy' else 'SHORT'
                vol = float(p.get('vol', 0))
                cost = float(p.get('cost', 0))
                asset_key = raw_pair.replace('ZEUR', '').replace('EUR', '') if raw_pair.replace('ZEUR', '').replace('EUR', '') in prices else None
                if asset_key:
                    current_val = vol * prices[asset_key]
                    pnl = (cost - current_val) if direction == 'SHORT' else (current_val - cost)
                else:
                    pnl = 0.0
                arrow = '▲' if pnl >= 0 else '▼'
                print(f"POSITION:{display} {direction} {vol:.4f} | {arrow} {pnl:+.2f} EUR")
    except Exception:
        pass

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
