"""Read-only MyStocks Africa market-data quote client for NSE Kenya."""
from __future__ import annotations
import json
import os
import urllib.parse
import urllib.request
import urllib.error


DEFAULT_BASE = "https://mystocks.africa/api/sandbox/v1/partner"

class MarketDataError(RuntimeError):
    pass


def get_quotes(symbols, api_key=None, base_url=None, timeout=15):
    symbols = [s.strip().upper() for s in symbols if s and s.strip()]
    if not symbols:
        raise ValueError("Provide at least one symbol, e.g. SCOM.KE")
    if len(symbols) > 50:
        raise ValueError("The documented batch endpoint accepts up to 50 symbols")
    key = api_key or os.getenv("MYSTOCKS_API_KEY")
    if not key:
        raise MarketDataError("Missing API key. Set MYSTOCKS_API_KEY; never put keys in source code.")
    base = (base_url or os.getenv("MYSTOCKS_BASE_URL") or DEFAULT_BASE).rstrip("/")
    query = urllib.parse.urlencode({"symbols": ",".join(symbols)})
    url = f"{base}/market/quotes?{query}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}", "Accept": "application/json", "User-Agent": "AngulorMarketResearch/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise MarketDataError(f"Market data HTTP {exc.code}; check key, access, and endpoint") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise MarketDataError(f"Market data request failed: {exc}") from exc
    rows = payload.get("data") if isinstance(payload, dict) else None
    if isinstance(rows, dict):
        rows = rows.get("quotes") or rows.get("stocks")
    if rows is None and isinstance(payload, dict):
        rows = payload.get("quotes") or payload.get("stocks")
    if not isinstance(rows, list):
        raise MarketDataError("Unexpected quote response structure; inspect provider API schema before adapting.")
    wanted = set(symbols)
    output = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        symbol = str(row.get("symbol") or row.get("ticker") or "").upper()
        if wanted and symbol not in wanted:
            continue
        quality = row.get("dataQuality") or {}
        freshness = row.get("dataFreshnessSeconds", quality.get("ageSeconds", row.get("ageSeconds"))))
        asof = row.get("asOf") or quality.get("asOf") or row.get("lastPriceUpdate")
        delay = row.get("delayMinutes", quality.get("delayMinutes"))
        stale = row.get("stale", quality.get("stale")))
        price = row.get("lastPrice", row.get("price", row.get("close"))))
        output.append({"symbol": symbol, "name": row.get("name"), "price": price,
                      "currency": row.get("currency", "KES"), "asOf": asof,
                      "ageSeconds": freshness, "delayMinutes": delay,
                      "delayMode": row.get("delayMode", quality.get("delayMode")),
                      "stale": stale, "provider": quality.get("provider", "MyStocks")})
    if not output:
        raise MarketDataError("No requested symbols found in quote response; verify provider symbols.")
    return output
