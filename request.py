import asyncio

import httpx

API_URL = "https://api.binance.com/api/v3/ticker/price"


async def main():
    client = httpx.AsyncClient()
    response = await client.get(API_URL, params={"symbol": "BTCUSD"})
    data = response.json()
    print(data["symbol"])
    print(data["price"])


asyncio.run(main())
