import time

from auth import token_bot, user_id
from aiogram import Bot, Dispatcher, executor, types
from main import get_ticker, max_min_price_for_the_last_24_hr
import asyncio

bot = Bot(token=token_bot)
dp = Dispatcher(bot)


async def check_time_frame(symbol, interval, diff_coefficient, max_coefficient, min_coefficient):
    ticker = get_ticker(symbol, interval)
    current_price = ticker['current_price']
    difference = ticker['difference']
    max_min = max_min_price_for_the_last_24_hr(symbol)
    max_price_for_24hr = max_min['max_price']
    min_price_for_24hr = max_min['min_price']

    if current_price == min_price_for_24hr or current_price <= min_price_for_24hr + min_coefficient:
        await bot.send_message(user_id, f'MIN PRICE!!!' '\n' f'{symbol}:f{current_price}')
    if current_price >= max_price_for_24hr - max_coefficient or current_price == max_price_for_24hr:
        await bot.send_message(user_id, f'MAX PRICE!!!' '\n' f'{symbol}:{current_price}', )
    if difference >= diff_coefficient or difference <= diff_coefficient:
        await bot.send_message(user_id, f'{current_price}' f'DIFF = {difference}')


async def check_eth():
    symbol = "ETHUSDT"
    diff_coefficient = 10
    max_coefficient = 5
    min_coefficient = 5
    interval_15m = "15m"
    interval_1h = "1h"
    interval_4h = "15m"
    await check_time_frame(symbol, interval_15m, diff_coefficient, max_coefficient, min_coefficient)
    await check_time_frame(symbol, interval_1h, diff_coefficient, max_coefficient, min_coefficient)
    await check_time_frame(symbol, interval_4h, diff_coefficient, max_coefficient, min_coefficient)


async def check_usdt():
    symbol = "USDTRUB"
    diff_coefficient = 0.1
    max_coefficient = 1
    min_coefficient = 1
    interval_15m = "15m"
    interval_1h = "1h"
    interval_4h = "15m"
    await check_time_frame(symbol, interval_15m, diff_coefficient, max_coefficient, min_coefficient)
    await check_time_frame(symbol, interval_1h, diff_coefficient, max_coefficient, min_coefficient)
    await check_time_frame(symbol, interval_4h, diff_coefficient, max_coefficient, min_coefficient)


async def main():
    while True:
        await check_eth()
        await check_usdt()
        await asyncio.sleep(10)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    executor.start_polling(dp)
