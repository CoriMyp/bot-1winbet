from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
	Message, CallbackQuery
)

import asyncio
import config
from time import sleep

from main import Request

bot = Bot(config.TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(msg: Message):
	await msg.answer("Отправь сообщение в таком формате:\n" \
					 "```Формат <ссылка> —> <1|2|X> (<коеф>)```\n" \
					 "```Формат <ссылка> —> <O|U> <тотал> (<коеф>)```")


@dp.message()
async def msg_handler(msg: Message):
	bot_msg = await msg.answer("Запрос обрабатывается")

	info = msg.text.split('—>')
	r = Request(info[0].strip(), info[1].strip())


	await bot_msg.edit_text("Авторизация")
	r.authorization()

	await bot_msg.edit_text(f"Ставим ставку")
	r.set_bet()

	sleep(50)

	if not r.confirm_bet():
		await bot_msg.edit_text("Коефициент в корзине не соотвествует указаному :(")
		r.exit()
		return

	await bot_msg.edit_text(f"Ставка поставлена!")

	r.exit()


async def main():
	print("Bot started!")
	await dp.start_polling(bot)


if __name__ == '__main__':
	asyncio.run(main())