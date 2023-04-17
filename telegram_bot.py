import time
from auth import token_bot, user_id
from aiogram import Bot, Dispatcher, executor, types
from main import get_ticker, max_min_price_for_the_last_24_hr
import asyncio

bot = Bot(token=token_bot)
dp = Dispatcher(bot)

messages_id_data = [] # store messages id

async def check_time_frame(symbol, interval, diff_coefficient, max_coefficient, min_coefficient):
	ticker = get_ticker(symbol, interval)
	current_price = ticker['current_price']
	difference = ticker['difference']
	max_min = max_min_price_for_the_last_24_hr(symbol)
	max_price_for_24hr = max_min['max_price']
	min_price_for_24hr = max_min['min_price']


	if current_price == min_price_for_24hr or current_price <= min_price_for_24hr + min_coefficient:
		msg = await bot.send_message(user_id, f'MIN PRICE {symbol}!!!' '\n' f'{symbol}: {current_price}')
		msg_id = msg["message_id"]
		messages_id_data.append(msg_id)
	if current_price >= max_price_for_24hr - max_coefficient or current_price == max_price_for_24hr:
		msg = await bot.send_message(user_id, f'MAX PRICE {symbol}!!!' '\n' f'{current_price}')
		msg_id = msg["message_id"]
		messages_id_data.append(msg_id)
	if abs(difference) >= diff_coefficient:
		msg = await bot.send_message(user_id, f'{symbol}: {current_price}' '\n' f'DIFF: {difference} {interval}')
		msg_id = msg["message_id"]
		messages_id_data.append(msg_id)


async def check_intervals(symbol, intervals, diff_coefficient, max_coefficient, min_coefficient):
	for interval in intervals:
		await check_time_frame(symbol, interval, diff_coefficient, max_coefficient, min_coefficient)


async def clear_chat(): # Deletes all messages from the chat except the last 6
	if messages_id_data:
		for id in messages_id_data[:-6]:
			await bot.delete_message(user_id, id)
			messages_id_data.remove(id)



async def main():
	usdt_rub = {
		"symbol":"USDTRUB",
		"diff_coefficient":0.5, # price diffrent betwen open and close kline
		"max_coefficient":0.3, # max_price_for_24hr - max_coefficient
		"min_coefficient":0.3, # min_price_for_24hr + min_coefficient
		"intervals":["15m", "1h", "4h"]
	}
	eth_usdt = {
		"symbol":"ETHUSDT",
		"diff_coefficient":10,
		"max_coefficient":20,
		"min_coefficient":30,
		"intervals":["15m", "1h", "4h"],

	}

	while True:
		await(bot.get_chat(user_id))
		await check_intervals(**usdt_rub)
		await check_intervals(**eth_usdt)
		await clear_chat() 
		await asyncio.sleep(225)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(main())
	executor.start_polling(dp)
