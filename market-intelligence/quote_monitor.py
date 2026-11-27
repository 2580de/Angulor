"""CLI for displaying read-only delayed NSE quotes."""
import sys
from quote_client import get_quotes, MarketDataError

def main():
    symbols = sys.argv[1:] or ["SCOM.KE", "EQTY.KE", "KCB.KE"]
    try:
        rows = get_quotes(symbols)
    except (MarketDataError, ValueError) as exc:
        print(f"Market data error: {exc}", file=sys.stderr)
        return 2
    print("ANGULOR NSE QUOTE MONITOR — research only; quotes may be delayed")
    for q in rows:
        print(f"\n{q['symbol']} | {q.get('name') or 'Unknown company'}")
        print(f"Price: {q.get('price')} {q.get('currency')}")
        print(f"Observed at: {q.get('asOf') or 'timestamp unavailable'}")
        print(f"Age: {q.get('ageSeconds') if q.get('ageSeconds') is not None else 'unknown'} sec | Feed delay: {q.get('delayMinutes') if q.get('delayMinutes') is not None else 'unknown'} min")
        print(f"Stale: {q.get('stale') if q.get('stale') is not None else 'unknown'} | Mode: {q.get('delayMode') or 'unknown'} | Source: {q.get('provider')}")
        print("WARNING: Treat as delayed research data; not a real-time execution price.")
if __name__ == "__main__":
    main()
