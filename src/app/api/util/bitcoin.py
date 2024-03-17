import aiohttp


async def get_current_conversion_rate():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://api-cryptopia.adca.sh/v1/prices/ticker?symbol=BTC%2FEUR") as response:
            if response.status != 200:
                raise Exception(f"API request failed with status {response.status}")

            data = await response.json()
            try:
                btc_eur_rate = float(
                    data["data"][0]["value"])
            except (IndexError, KeyError):
                raise ValueError("BTC/EUR rate not found in response")

            return btc_eur_rate


async def convert_eur_to_btc(amount: float):
    conversion_rate = await get_current_conversion_rate()
    return abs(amount / conversion_rate)


async def convert_btc_to_eur(amount: float):
    conversion_rate = await get_current_conversion_rate()
    return abs(amount * conversion_rate)
