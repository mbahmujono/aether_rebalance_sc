"""
Simple proxy that:
1. Caches the CoinMarketCap symbol→ID map (12 h TTL)
2. Exposes POST /api/price-conversion
   payload = { "tokens": [ { "symbol": "ETH", "balance": 0.02 }, ... ] }
   response = { "data": [ { "symbol": "ETH", "balance": 0.02, "usdValue": 73.42 }, ... ] }
Run with:
  export CMC_API_KEY=xxxxx
  python app.py
"""

import os, time, requests
from flask import Flask, request, jsonify
from flask_cors import CORS

CMC_KEY = os.getenv("CMC_API_KEY")
if not CMC_KEY:
    raise RuntimeError("Set CMC_API_KEY env var")

CMC_BASE   = "https://pro-api.coinmarketcap.com"
SYMBOL_TTL = 60 * 60 * 12            # 12 h

session = requests.Session()
session.headers.update({
    "X-CMC_PRO_API_KEY": CMC_KEY,
    "Accept": "application/json",
})

_symbol_map: dict[str, int] = {}
_symbol_ts: float = 0.0


def refresh_symbol_map() -> None:
    """Fetch & cache the symbol-ID map if stale."""
    global _symbol_map, _symbol_ts
    if time.time() - _symbol_ts < SYMBOL_TTL and _symbol_map:
        return
    r = session.get(f"{CMC_BASE}/v1/cryptocurrency/map")
    r.raise_for_status()
    _symbol_map = {row["symbol"].upper(): row["id"] for row in r.json()["data"]}
    _symbol_ts  = time.time()


def convert_price(token_id: int, amount: float) -> float | None:
    """Return USD price for given amount (None on failure)."""
    try:
        r = session.get(
            f"{CMC_BASE}/v2/tools/price-conversion",
            params={"id": token_id, "amount": amount, "convert": "USD"},
            timeout=10,
        )
        r.raise_for_status()
        print(f"CMC conversion response: {r.json()["data"]["quote"]["USD"]["price"]}")
        return r.json()["data"]["quote"]["USD"]["price"]
    except Exception as exc:
        app.logger.error("CMC conversion failed: %s", exc)
        return None


app = Flask(__name__)
CORS(app, supports_credentials=True)          # allow localhost:5173 etc.


@app.post("/api/price-conversion")
def price_conversion():
    payload = request.get_json(force=True) or {}
    tokens  = payload.get("tokens", [])
    refresh_symbol_map()

    out = []
    for tok in tokens:
        sym = str(tok.get("symbol", "")).upper()
        print(f"Processing token: {sym}")
        bal = float(tok.get("balance", 0))
        usd = None
        if "eth" in sym.lower():
            tid = 1027
        elif "usd" in sym.lower():
            tid = _symbol_map.get("USDC")
        else:
            tid = _symbol_map.get(sym)
        if tid is not None and bal:
            usd = convert_price(tid, bal)
        out.append({"symbol": sym, "balance": bal, "usdValue": usd})
    return jsonify({"data": out})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    print("Starting CoinMarketCap price conversion proxy...")