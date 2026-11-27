# Angulor — NSE Market Intelligence Integration

This folder is an additive research module; it does not modify the existing Intelligent Mind files.

## Live data status
- Nairobi Securities Exchange symbols use exchange-qualified symbols such as `SCOM.KE`.
- The MyStocks partner Market Data API is used for quote retrieval. Its documented African equity feed is **15-minute delayed**, not tick-by-tick real-time. The API refresh target is 900 seconds during coverage hours. Each quote's `asOf`/freshness must be checked.
- The module is read-only. It does not place trades, connect to a broker, or claim predictions.

## Setup
1. Obtain a permitted API key from the provider.
2. Set environment variable `MYSTOCKS_API_KEY` (never commit keys).
3. Set `MYSTOCKS_BASE_URL` if using another approved environment. Default sandbox URL is `https://mystocks.africa/api/sandbox/v1/partner`.
4. Run `python quote_monitor.py SCOM.KE EQTY.KE KCB.KE`.

No API key is included. No scraped NSE site or unofficial live feed is used.

## Safety / data requirements
- Show provider, exchange observation timestamp, data delay, and stale flag for every quote.
- Fail closed when API key is missing, HTTP errors occur, a symbol cannot be resolved, or the response cannot be parsed.
- Treat delayed quotes as research only. Verify data licensing/redistribution terms before public display.
- For real-time (zero-delay) market data, request an approved NSE/vendor feed entitlement and implement that vendor's documented feed. This module cannot make a delayed source real-time.

## Watchlist
Starter examples: `SCOM.KE`, `EQTY.KE`, `KCB.KE`. Confirm canonical symbols with the provider's stock directory before relying on them.
